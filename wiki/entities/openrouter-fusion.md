---
title: OpenRouter Fusion
created: 2026-06-16
updated: 2026-06-16
type: entity
tags: [product, tool, multi-model, agent-orchestration]
sources: [raw/Fusion.md]
confidence: medium
contested: true
---

# OpenRouter Fusion

## 概述

OpenRouter 在其模型路由平台上推出的 **Fusion** 功能（截至 2026-06 仍处 beta）——一个**服务端的多模型审议管道（multi-model deliberation pipeline）**，并非单一模型。它把同一份 Prompt 并行发给多个外部模型，再用一个裁判模型把它们对比成结构化 JSON，最后由外层模型基于分析撰写最终答案。核心设计哲学是"**比较（compare），而非合并（merge）**"。^[raw/Fusion.md]

> **可信度提示**：本页部分数字（成本倍数、面板上限 8、延迟 2–3 倍）来自社区文章而非官方文档，已在原文标注；本 wiki 在 frontmatter 中标 `contested: true` 以提示读者区分官方机制与推断。^[raw/Fusion.md]

## 三个等价入口

| 入口 | 控制粒度 | 适用场景 |
|---|---|---|
| 模型别名 `openrouter/fusion` | 最低（自动注入插件） | 快速替换单模型调用 |
| 插件 `plugins` 字段 | 中（可配置面板/评审） | 保留原模型但增加融合能力 |
| 服务端工具 `openrouter:fusion` | 最高（外层模型自主调用） | Agent 编排场景 |

三个入口最终汇聚到同一条管道：Panel（盲评）→ Judge（结构化裁判）→ Outer（合成终稿）。^[raw/Fusion.md]

## 核心机制

### 盲评 Panel
每个面板成员接收**完全相同的 Prompt**，但**互不可见**。默认启用 `web_search` / `web_fetch`，可基于实时信息作答。^[raw/Fusion.md]

盲评是设计的核心——刻意避免模型间的"从众效应"与权威锚定。这与 [[sub-agent]] 中"执行 vs 验证"的纵向分离形成**横向对照**：Sub-agent 是同一组织内、不同角色的分工；Fusion 是跨供应商、平行角色的独立性保留。

### 结构化 Judge
裁判模型输出严格 JSON，固定五个维度：

| 维度 | 含义 | 下游处理 |
|---|---|---|
| `consensus` | 全部/多数一致观点 | 高置信度，优先采纳 |
| `contradictions` | 模型间立场冲突 | 不抹平，暴露给外层模型评判 |
| `partial_coverage` | 仅部分模型提及 | 提示信息可能不完整 |
| `unique_insights` | 单一模型提出的高价值观点 | 保留少数派，避免群体思维 |
| `blind_spots` | 所有模型都未涉及的领域 | 外层模型自行补充或承认未知 |

^[raw/Fusion.md]

`response_format: json_object` + 缺字段校验是裁判阶段的硬约束——这是保证"结构化"而非"自然语言总结"的关键。

### 外层合成
外层模型**自行撰写**最终答案（不是拼接）。收到 JSON 后，按 consensus（高置信）→ contradictions（辩证呈现）→ unique_insights → blind_spots（承认未知）的顺序组织 Markdown。这保证语气统一、逻辑连贯。^[raw/Fusion.md]

## 触发与路由

- **自主触发（默认）**：外层模型读取工具描述，自行判断任务是否受益于多视角（研究型、跨领域批判、容错成本高的场景）。简单问题直接回答，**零额外延迟**。
- **强制触发**：`tool_choice: "required"`，每次请求都融合。

面板构成预设：
- **Quality（默认）**：顶级模型组合（Claude Opus、GPT、Gemini Pro），追求深度
- **Budget**：更快更便宜的模型，追求速度
- **Custom**：`analysis_models` 指定面板，`model` 指定裁判（默认即外层模型）

^[raw/Fusion.md]

## 韧性设计

### 递归保护
HTTP 头 `x-openrouter-fusion-depth` 强制审议深度恒为 1 层。内层调用一旦检测到该头，便拒绝二次注入 fusion 工具，防止无限递归与费用失控。^[raw/Fusion.md]

### 优雅降级
| 状态 | 行为 |
|---|---|
| `status: "ok"` + 完整 analysis | 正常融合 |
| 部分面板失败 | 返回 `failed_models` + 成功模型继续推进 |
| 裁判失败（无 analysis） | 降级：外层直接从原始回答撰写 |
| `status: "error"` | 所有面板失败，返回 `failure_reason` |

^[raw/Fusion.md]

### 性能优化
- **并行 fan-out**：总延迟 ≈ 最慢面板成员 + 裁判 + 外层合成，而非各模型之和
- **`max_tool_calls` 预算**：限制每个成员的搜索/抓取迭代次数（典型默认 8，范围 1–16）
- **`max_completion_tokens`**：为推理型模型设置输出上限
- **SSE 流式输出**：面板阶段必须先完成，但终稿生成可流式推送
- **成本透明**：计费 = 面板成员 + 裁判 + 外层模型总和；Activity 页面逐项可见

^[raw/Fusion.md]

## 实证依据

在 DRACO（100 个深度研究任务）基准上，融合面板得分约 **69%**，最强单一模型约 **65%**。**[数值来源：第三方分析，需以官方为准]**^[raw/Fusion.md]

更关键的发现是**自我融合**实验——同一模型与自己组成面板仍有约 6.7 分提升。这说明收益不仅来自模型多样性，"结构化审议+合成"这一步**本身**就在创造价值。^[raw/Fusion.md]

## 关键设计原则

| 原则 | 说明 |
|---|---|
| **比较而非合并** | 保留多元视角，把分歧暴露给最终决策者 |
| **盲评独立** | 面板成员互不可见，避免从众与锚定 |
| **模型自治** | 外层模型自主决定是否触发，保持日常低延迟 |
| **结构化降级** | 裁判失败不阻塞流程 |
| **递归遏制** | 深度头限定单层审议 |
| **成本透明** | 按所有底层调用之和计费，可审计 |

^[raw/Fusion.md]

## 代价与权衡

- **成本**：默认 3 模型面板约为单次调用的 **4–5 倍**（数字经官方文档量化）^[raw/Fusion.md]
- **延迟**：官方未公布具体倍数，社区说法"2–3 倍"属未经证实的传闻^[raw/Fusion.md]
- **隐私/安全**：单 Prompt 扇出到多个第三方供应商，数据日志与攻击面同步扩大——这是 beta 阶段值得权衡的代价^[raw/Fusion.md]

## 相关页面

- [[multi-model-deliberation]] — 概念抽象：Fusion 是该范式的服务端实现
- [[sub-agent]] — 纵向分工（执行/验证）；Fusion 是横向分工（互盲审议）
- [[loop-engineering]] — 五大代际中"多 Agent 编排 Loop"的代表性形态
- [[claude-code]] / [[codex]] — 同代际的 Loop 工具，但走的是单模型深耕路线

## 引用

- [OpenRouter Fusion 官方文档](https://openrouter.ai/docs/features/fusion)
- 原始分析笔记：`raw/Fusion.md`
