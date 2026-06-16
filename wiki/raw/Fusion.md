---
source_url: https://openrouter.ai/docs/features/fusion
ingested: 2026-06-16
sha256: fbd0363bc3805694d73f79c19bca8e4ab226d6e6cceda917c89e08225cb73e08
---

# OpenRouter Fusion 实现原理深度技术分析

OpenRouter Fusion 并不是一个单独的模型，而是一个**服务器端的多模型审议管道（multi-model deliberation pipeline）**。它的核心设计哲学可以用一句话概括：**比较（compare），而非合并（merge）**。它不是对多个模型的输出做投票或文本拼接，而是模拟了一个"专家小组 → 评审 → 主编"的协作流程。

> 说明：本文区分了官方文档已确认的机制与社区/工程层面的合理推断。文中明确标注的具体数字（如延迟倍数、面板上限为 8）属于推断或未经官方证实的传闻，请谨慎对待。

---

## 一、整体架构总览

Fusion 提供三个等价入口，最终都汇聚到同一条管道：

| 入口方式 | 控制粒度 | 适用场景 |
|---------|---------|---------|
| 模型别名 `openrouter/fusion` | 最低（自动注入插件） | 快速替换单模型调用 |
| 插件 `plugins` 字段 | 中（可配置面板/评审） | 保留原模型但增加融合能力 |
| 服务端工具 `openrouter:fusion` | 最高（外层模型自主调用） | 与其他工具链组合的 Agent 场景 |

核心流程如下：

```
              [ 用户 Prompt ]
                    │
            [ 外层模型 Outer ] ── 决定是否触发 fusion
                    │ 调用 openrouter:fusion
       ┌────────────┼────────────┐
       ▼            ▼            ▼
  [专家模型A]   [专家模型B]   [专家模型C]   ← Panel 并行，各自带 web_search/fetch
       └────────────┼────────────┘
                    ▼
          [ 裁判模型 Judge ] ── 对比分析，输出结构化 JSON
                    │
                    ▼
       [ 外层模型撰写最终 Markdown 答案 ]
```

---

## 二、四大核心组件

### 1. Prompt 融合策略：结构化审议而非文本平均

传统集成方法（投票、加权平均、文本堆叠）容易导致"最平庸化平均"——稀释独特洞察、强行抹平矛盾。Fusion 放弃了直接合并，采用 **"并行盲评 → 结构化裁判 → 全局合成"** 三段式：

**① Panel 阶段（盲评）**：每个面板模型接收**相同的原始 Prompt**，但彼此不可见，独立作答。这种"盲阶段"设计刻意避免了模型间的"从众效应"和权威锚定。每个成员默认启用 `web_search` 和 `web_fetch`，可基于实时信息作答。

**② Judge 阶段（比较而非合并）**：裁判模型接收全部面板输出后，输出严格的 JSON，包含五个独立维度：

| 维度 | 含义 | 下游处理 |
|------|------|---------|
| `consensus`（共识） | 全部/多数模型一致认同的观点 | 标记为高置信度，优先采纳 |
| `contradictions`（矛盾） | 模型间立场冲突的话题，附各自论据 | 不抹平，暴露给最终决策者评判 |
| `partial_coverage`（部分覆盖） | 仅部分模型提及的子话题 | 提示信息可能不完整 |
| `unique_insights`（独特见解） | 仅单一模型提出的高价值观点 | 保留少数派，避免群体思维 |
| `blind_spots`（盲区） | 所有模型都未涉及的重要领域 | 外层模型需自行补充或承认未知 |

**③ 合成阶段**：外层模型接收 JSON 分析作为输入，**自行撰写**最终答案——而非机械执行。这保证了最终输出语气统一、逻辑连贯，而不是多段拼接。

> 这种设计的精妙之处：分歧不被投票抹杀，而是显式暴露；独立见解被保留，防止多数派压制少数派的正确观点；每个观点可追溯到来源模型，因而可审计。

### 2. 模型路由逻辑

**触发机制**有两种：
- **自主触发（默认）**：外层模型读取工具描述，自行判断任务是否真正受益于多视角（研究型、跨领域批判、对比分析、容错成本高的场景）。简单问题直接回答，**零额外延迟**。
- **强制触发**：设置 `tool_choice: "required"`，每次请求都执行融合。

**面板构成**通过预设或显式列表控制：
- **Quality 预设（默认）**：调度顶级模型组合（如 Claude Opus、GPT、Gemini Pro），追求深度。
- **Budget 预设**：调度更快更便宜的模型，快速获取多样视角。
- **Custom**：通过 `analysis_models` 指定面板成员，通过 `model` 指定裁判（默认即外层模型）。

> 注意：多份资料提到"面板支持 1–8 个模型"，但官方文档仅确认默认 3 模型面板且成本随面板规模线性增长，**"8" 这个上限未经官方证实**。

**递归保护**：系统注入 `x-openrouter-fusion-depth` HTTP 头。一旦内层调用检测到该头，便拒绝二次注入 fusion 工具，强制审议深度恒为 1 层，防止无限递归与费用失控。

### 3. 性能优化

- **并行 fan-out**：面板所有模型同时发起请求。总延迟 ≈ **最慢面板成员 + 裁判 + 外层合成**，而非各模型之和。
- **选择性触发**：日常简单问题不进入融合流程，几乎不增加延迟。
- **工具调用预算** `max_tool_calls`（典型默认 8，范围约 1–16）：限制每个成员的搜索/抓取迭代次数，防止无限检索拖垮延迟。
- **Token/推理预算** `max_completion_tokens`：为推理型模型设置输出上限，防止 reasoning 模式吃光 token。
- **流式输出**：支持 SSE。面板阶段必须先完成，但最终答案生成可流式推送，改善体验。
- **优雅降级**（关键韧性设计）：

| 状态 | 行为 |
|------|------|
| `status: "ok"` + 完整 analysis | 正常融合 |
| 部分面板失败 | 返回 `failed_models` + 成功模型的 responses，继续推进 |
| 裁判失败（无 analysis） | 降级：外层模型直接从原始回答撰写答案 |
| `status: "error"` | 所有面板失败，返回 `failure_reason`（如 `all_panels_failed` / `rate_limited` / `insufficient_credits`） |

> 关于"延迟增加 2–3 倍"的说法：官方文档量化了**成本**（默认 3 模型面板约为单次调用的 4–5 倍），但**并未公布具体延迟倍数**，此类数字应视为传闻。

### 4. UI/UX 集成

- **Fusion Lab 配置界面**（`openrouter.ai/fusion`）：提供 Quality / Budget / Custom 三档切换、可视化增删面板成员、裁判 Auto 或手动指定。
- **渐进式状态呈现**：由于审议耗时长于单模型，不应只显示一个加载圈。理想的 UX 把流程拆成多阶段（部署面板 → 专家检索 → 裁判审议 → 输出终稿），并为每个面板成员开辟独立的流式进度卡片。
- **辩论可视化**：基于 JSON 渲染专门组件——共识用绿色高亮卡，矛盾用并列对照面板（左右展示不同模型立场），独特见解用可折叠抽屉查看原始回答。
- **可观测性**：Activity 页面记录实际调用了哪些模型及各自 token 消耗，便于成本审计。计费 = 面板成员 + 裁判 + 外层模型的**总和**。

---

## 三、为什么这套架构有效（一个常被忽略的关键点）

Fusion 的设计有实证支撑：在 DRACO（100 个深度研究任务）基准上，融合面板得分约 **69%**，而最强单一模型约 **65%**。更有启发性的是**自我融合**实验——同一个模型与自己组成面板时仍有约 6.7 分的提升。这说明：**收益不仅来自模型多样性，"结构化审议+合成"这一步本身就在创造价值**。

同时也应保持批判：所谓"超越前沿模型"是基准特定、面板相关的结论，且伴随更高的成本与延迟。此外，把单个 Prompt 扇出给多个第三方供应商，也意味着数据日志和隐私攻击面的扩大——这是该功能（目前仍处 beta）值得权衡的代价。

---

## 四、可行实现方案

### 逻辑流程

```
[API 请求] → [检查 fusion-depth 头]
                 ├─ depth ≥ 1 → 熔断，单模型普通回答
                 └─ depth = 0 → 进入 Fusion 管道
                                  │
                          [路由器：是否需要融合？]
                                  │ 需要
                          [并行调度器：fan-out N 个面板模型，各带 search/fetch]
                                  │
                          [收集成功响应 / 过滤失败（优雅降级）]
                                  │
                          [裁判模型 → 结构化 JSON]
                              ├─ 解析成功 → 作为合成基础
                              └─ 解析失败 → 降级用原始文本
                                  │
                          [外层模型撰写最终 Markdown]
```

### 后端伪代码（Python / asyncio）

```python
import asyncio, json
from typing import List, Dict, Optional

class FusionEngine:
    def __init__(self, api):
        self.api = api  # 封装对各模型 API 的调用

    async def run(self, prompt: str, cfg, depth: int = 0) -> Dict:
        # 1. 递归保护
        if depth >= 1:
            return await self.api.chat(cfg.outer_model,
                [{"role": "user", "content": prompt}])

        # 2. 是否需要融合（默认由外层模型判断；可强制）
        if not cfg.force and not await self._should_fuse(prompt, cfg.outer_model):
            return await self.api.chat(cfg.outer_model,
                [{"role": "user", "content": prompt}])

        # 3. 并行调度面板（关键：fan-out + 深度头 + 工具）
        tasks = [self._call_panel(m, prompt, cfg.max_tool_calls, depth + 1)
                 for m in cfg.panel_models]
        raw = await asyncio.gather(*tasks, return_exceptions=True)

        # 4. 优雅降级：过滤失败/超时成员
        responses, failed = [], []
        for m, r in zip(cfg.panel_models, raw):
            (responses if isinstance(r, dict) and r.get("ok") else failed).append(
                r if isinstance(r, dict) else {"model": m, "error": str(r)})
        if not responses:
            return {"status": "error", "failure_reason": "all_panels_failed",
                    "failed_models": failed}

        # 5. 裁判：结构化对比 → JSON
        analysis = await self._judge(cfg.judge_model or cfg.outer_model,
                                     prompt, responses, depth + 1)

        # 6. 外层合成（analysis 为 None 时走降级路径）
        final = await self._synthesize(cfg.outer_model, prompt,
                                       analysis, responses, depth + 1)
        return {"status": "ok", "content": final["content"],
                "analysis": analysis,
                "failed_models": failed or None}

    async def _call_panel(self, model, prompt, max_tool_calls, depth):
        return await self.api.chat(model,
            messages=[{"role": "system", "content": PANEL_SYSTEM_PROMPT},
                      {"role": "user", "content": prompt}],
            tools=["web_search", "web_fetch"],
            max_tool_calls=max_tool_calls,
            headers={"x-fusion-depth": str(depth)})

    async def _judge(self, model, prompt, responses, depth):
        panel_text = "\n\n".join(
            f"=== Model: {r['model']} ===\n{r['content']}" for r in responses)
        res = await self.api.chat(model,
            messages=[{"role": "system", "content": JUDGE_PROMPT},
                      {"role": "user",
                       content := f"User Query:\n{prompt}\n\nPanel:\n{panel_text}"}],
            response_format={"type": "json_object"},
            tools=["web_search", "web_fetch"],
            headers={"x-fusion-depth": str(depth)})
        try:
            data = json.loads(res["content"])
            req = ["consensus", "contradictions", "partial_coverage",
                   "unique_insights", "blind_spots"]
            return data if all(k in data for k in req) else None
        except Exception:
            return None  # Judge 降级

    async def _synthesize(self, model, prompt, analysis, responses, depth):
        panel_text = "\n\n".join(
            f"=== {r['model']} ===\n{r['content']}" for r in responses)
        if analysis:
            user = (f"User Query:\n{prompt}\n\nStructured Analysis:\n"
                    f"{json.dumps(analysis, ensure_ascii=False, indent=2)}")
        else:  # 降级：裁判失效，直接给原始文本
            user = (f"User Query:\n{prompt}\n\n(Judge unavailable)\n"
                    f"Panel Responses:\n{panel_text}")
        return await self.api.chat(model,
            messages=[{"role": "system", "content": SYNTHESIS_PROMPT},
                      {"role": "user", "content": user}],
            headers={"x-fusion-depth": str(depth)})
```

### Prompt 设计示例

**① 面板成员系统提示（保持一致、中立、盲评）**

```text
You are an expert research assistant. Answer the user's question thoroughly
and accurately. You have access to web_search and web_fetch — use them when
the question needs up-to-date or specialized knowledge.

Rules:
- Answer as the sole expert. Do NOT reference other AI models or any panel.
- Cite sources when using external information.
- If uncertain, state your confidence level explicitly.
```

**② 裁判提示（核心——强制比较，强制 JSON）**

```text
You are a strict analytical Judge. Compare and contrast the panel responses
to the same user query. Do NOT merge them into one narrative. Produce a
rigorous structured analysis.

Output a SINGLE valid JSON object with EXACTLY these keys (use [] if empty):

{
  "consensus": [        // points all/most models agree on (high confidence)
    {"claim": "...", "supported_by": ["model_id", ...]}
  ],
  "contradictions": [   // topics where models conflict
    {"topic": "...",
     "stances": [{"model": "...", "stance": "assertion + rationale"}],
     "assessment": "which side has stronger evidence, or truly ambiguous"}
  ],
  "partial_coverage": [
    {"models": ["..."], "point": "covered only by some, why it matters"}
  ],
  "unique_insights": [
    {"model": "...", "insight": "valuable point raised by exactly one model"}
  ],
  "blind_spots": [      // important topics NONE addressed
    "..."
  ]
}

Rules:
- Treat as consensus only when 2+ models independently agree.
- For contradictions, weigh evidence QUALITY, not popularity.
- Attribute each stance to the specific model. Keep claims atomic.
- Return ONLY the JSON. No prose, no markdown fences.
```

**③ 外层合成提示（基于 JSON 撰写终稿）**

```text
You are the lead synthesis author. A panel of models analyzed the user's
query, and a judge produced the structured analysis below. Write the
definitive final answer.

Guidelines:
1. Ground the answer in the consensus items (high confidence, zero hallucination).
2. Present contradictions dialectically — explain WHY experts diverge and under
   what conditions each holds; weigh the evidence rather than averaging.
3. Weave in unique insights and partial coverage for nuance.
4. Actively address blind spots: fill the gap with your own knowledge, or
   explicitly acknowledge the limitation.
5. Single coherent voice. Do NOT mention "Expert 1", "the panel", or JSON keys
   in the user-facing text. Present it as one masterful analysis.
6. Output clean Markdown with headers, lists, and comparison tables where helpful.
```

---

## 五、可借鉴的核心设计原则

| 原则 | 说明 |
|------|------|
| **比较而非合并** | 保留多元视角，把分歧暴露给最终决策者 |
| **盲评独立** | 面板成员互不可见，避免从众与锚定 |
| **模型自治** | 外层模型自主决定是否触发，保持日常低延迟 |
| **结构化降级** | 裁判失败不阻塞流程，原始回答仍可利用 |
| **递归遏制** | 深度头限定单层审议，防止失控与天价账单 |
| **工具赋能** | 面板与裁判均可实时检索，突破知识截止期 |
| **成本透明** | 按所有底层调用之和计费，明细可审计 |

本质上，Fusion 把多模型协作从"粗糙的投票/拼接"提升到了"结构化审议"——通过**并行盲评 + 结构化裁判 JSON + 外层再创造**这条可复现路径，配合严格的工具/token 预算与流式优化，在对答案质量、覆盖面和可靠性要求高的场景中创造价值。但要清醒认识到它的代价：成本数倍增长、延迟增加，以及多供应商扇出带来的隐私与安全攻击面扩大。