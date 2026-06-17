# Fusion Skill 设计

- **日期**: 2026-06-16
- **状态**: 设计稿，待审查
- **关联**: `raw/Fusion.md`、`concepts/multi-model-deliberation.md`、`cmd.rc`、`omp`(Oh My Pi v16.0.1)

---

## 1. 一句话定位

把 OpenRouter Fusion 的"并行盲评 → 结构化裁判 → 主编合成"审议管道，做成一个 Claude Code skill；**panel 用 `omp` 调真·多模型**，裁判与合成由当前会话 Claude 承担。

## 2. 为什么做

- `raw/Fusion.md` 已论证"比较而非合并"优于传统 ensemble，且**自我融合仍有效**（+6.7 分）——结构化审议本身创造价值。
- `omp` 天然命中 Fusion 全部硬需求：`-p`（无头）、`--system-prompt`（盲评）、`--mode json`（结构化）、`--no-skills`（纯净+防递归）。
- 本地有多个可用模型（glm-5.2 / minimax-m3 / deepseek / gpt-5.5 等），具备跨供应商审议条件。

## 3. 架构：三段式

```
用户显式调用 Fusion skill（带问题）
        │
        ▼
[① Panel]  run_fusion.py 用 omp 并行 fan-out 3 个模型（盲评，互不可见）
        │   omp -p --no-tools --no-skills --no-session \
        │        --system-prompt @prompts/panel.md --model X "<问题>"
        ▼
[② Judge]  当前会话 Claude 读全部 panel 原答 → 产出五维 JSON
        │   （默认=外层模型，符合 Fusion 原版；想换强模型就临时用 omp 调）
        ▼
[③ Synthesis] 当前会话 Claude 基于五维 JSON 写终稿 + 折叠附录
```

## 4. 组件

| 文件 | 职责 |
|---|---|
| `skills/fusion/SKILL.md` | 触发条件 + 流程指令（调脚本 → 读结果 → 裁判 → 合成） |
| `skills/fusion/run_fusion.py` | asyncio 编排：并行 fan-out panel（调 omp）、收集、过滤失败、落盘 JSON |
| `skills/fusion/prompts/panel.md` | 面板成员盲评系统提示（中立、不提及其他模型/panel） |
| `skills/fusion/prompts/judge.md` | 裁判五维 JSON 指南（强制五键，参考 raw/Fusion.md） |

软链接：`skills/fusion/ → ~/.claude/skills/fusion`（沿用现有 skill 约定，如 technical-analysis）。

## 5. 默认值（写死，非 CLI 参数）

| 项 | 默认 | 如何覆盖 |
|---|---|---|
| Panel 成员 | deepseek-v4-pro / minimax-m3 / mimo-v2.5-pro | 用户直接对 Claude 说"这次用 X,Y,Z" |
| 裁判模型 | 当前会话 Claude（外层模型） | 用户说"用 gpt-5.5 当裁判" → Claude 临时用 omp 调 |
| web 搜索 | `--no-tools`（纯作答，省/快） | 用户说要联网则去掉 `--no-tools` |
| 输出形态 | 终稿 + 折叠附录（五维 / 各原答 / 模型 / 耗时） | — |
| 触发 | 用户显式调用 | — |

> **不设 `--models`/`--judge` CLI 参数**：skill 是自然语言流程，参数只是脚本内部实现。用户用自然语言提需求，执行 Claude 决定怎么调脚本。

## 6. 错误处理与降级（照搬 fusion.md 矩阵）

- 单个 panel 成员失败/超时 → 记入 `failed`，用成功的继续。
- panel 全失败 → 返回 `failure_reason`，Claude 如实报告，**不编**。
- 裁判 JSON 缺键/解析失败 → Claude 标注"裁判降级"，直接从 panel 原答合成（不走五维）。

## 7. 递归保护

panel 的 omp 调用统一带 `--no-skills --no-extensions --no-rules`，不会再加载本 Fusion skill → 审议深度恒为 1，无需 HTTP header。

## 8. 成本与留痕

- 每次运行真实花费（3 模型 panel），SKILL.md 顶部标成本警示。
- `run_fusion.py` 落盘 `tmp/fusion_<时间戳>.json`（panel 原答 / 五维 / failed / 耗时），符合"脚本留痕"。

## 9. 测试（精准、不全量）

1. 一个简单问题跑通 3 模型 fan-out，验证并行收集正确。
2. 验证裁判 JSON 五键（consensus/contradictions/partial_coverage/unique_insights/blind_spots）齐全。
3. 故意指定一个不存在的模型，验证 `failed` 降级路径。
4. 只跑与改动直接相关的验证，**禁止全量/batch**。

## 10. 待确认 / 风险

- **默认模型可达性**：deepseek-v4-pro / minimax-m3 / mimo-v2.5-pro 均已用 omp 验证无头调用可行（2026-06-16/17）。glm-5.2 因稳定性问题（输出在 64KB 边界解码崩）已从默认 panel 替换为 deepseek-v4-pro，仍可 `--models` 临时指定。
- **执行 skill 的会话 Claude（默认 glm-5.2）能否可靠完成 judge+synthesis**：已通过"编排下沉脚本、判断留 Claude"缓解；judge 质量不足时回退"judge 用 omp 调强模型"。
- **omp 模糊匹配稳定性**：`--model` 简称可能歧义，实现时优先全称 ID。

## 11. 不做（YAGNI）

- 不做 omp `bench` 包装（风险高）。
- 不做"自适应 panel 规模"（按难度 2–5 个）。
- 不做 CLI 参数接口（`--models`/`--judge`）。
- 不做服务端/HTTP 化。
