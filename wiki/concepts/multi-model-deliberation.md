---
title: 多模型审议 (Multi-model Deliberation)
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [multi-model, agent-orchestration, paradigm, prompt-engineering]
sources: [raw/Fusion.md]
confidence: medium
contested: true
---

# 多模型审议 (Multi-model Deliberation)

## 定义

**多模型审议**是一种让多个 LLM 并行作答、由裁判模型产出结构化对比、最终由外层模型基于分析合成终稿的编排模式。它是 [[loop-engineering]] 体系下"多 Agent 编排"的代表性范式，对应 2026.6 代际的落地形态。^[raw/Fusion.md]

> 当前最成熟的服务端实现是 [[openrouter-fusion]]。

## 核心范式：比较而非合并

传统集成方法（投票、加权平均、文本堆叠）会导致"最平庸化平均"——稀释独特洞察、强行抹平矛盾。审议范式放弃直接合并，采用三段式：

```
Panel（盲评）→ Judge（结构化裁判）→ Outer（合成终稿）
```

^[raw/Fusion.md]

### 为什么"比较"优于"合并"

| 维度 | 投票/拼接 | 审议 |
|---|---|---|
| 分歧处理 | 被抹平（少数派被压） | 显式暴露给最终决策者 |
| 独特见解 | 容易被平均掉 | 独立保留（unique_insights 维度） |
| 可审计性 | 难追溯 | 每个观点可归属到来源模型 |
| 抗从众 | 弱（汇总后无法区分） | 强（盲评阶段刻意切断锚定） |

^[raw/Fusion.md]

## 与 Sub-agent 的关系

[[sub-agent]] 和多模型审议分别代表 [[loop-engineering]] 体系中**两种互补的分工模式**：

| 维度 | Sub-agent | 多模型审议 |
|---|---|---|
| 分工方向 | **纵向**（执行 vs 验证） | **横向**（互盲平行作答） |
| 模型来源 | 通常同一供应商 | 通常跨供应商（OpenRouter Fusion 默认 Quality 面板含 Claude/GPT/Gemini） |
| 核心假设 | 实现者自评不可靠 → 用第二视角纠偏 | 单一视角有盲区 → 用多视角互补 |
| 失败模式 | 验证子 Agent 跟着实现者跑偏 | 面板成员互相从众（由盲评机制阻断） |

二者**不是互斥**，完全可以嵌套：[[openrouter-fusion]] 的外层模型本身就可以调度 sub-agent 去做执行/验证分工，外层模型再用审议范式决定"请哪几个专家回答"。^[raw/Fusion.md]

## 五大结构化维度

裁判模型的输出 JSON 固定包含五个独立维度，每个对应明确的决策含义：

1. **consensus**（共识）— 全部/多数一致观点。高置信度，优先采纳。
2. **contradictions**（矛盾）— 模型间立场冲突的话题，附各自论据。**不抹平**，辩证呈现。
3. **partial_coverage**（部分覆盖）— 仅部分模型提及。提示信息不完整。
4. **unique_insights**（独特见解）— 仅单一模型提出的高价值观点。保留少数派。
5. **blind_spots**（盲区）— 所有模型都未涉及的重要领域。外层模型自行补充或承认未知。

^[raw/Fusion.md]

> 这种"五维结构"的精妙之处：**把"分析"和"作答"分开**，外层模型只承担"基于分析撰写终稿"这一职责，分析质量由裁判模型独立保证。

## 实施核心要点

### 盲评 (Blind Panel)
所有面板成员接收**完全相同的 Prompt** 且**互不可见**。这是避免锚定效应与从众效应的硬约束——一旦让模型看到彼此输出，"审议"就会退化成"对话/争吵"。^[raw/Fusion.md]

### 强制 JSON 输出
裁判阶段必须 `response_format: json_object` + 缺字段校验。这是保证结构化的硬技术约束——让模型"自由发挥"会迅速退化为自然语言总结，五维结构化为空谈。^[raw/Fusion.md]

### 递归保护
审议管道很容易陷入"审议的审议"递归，账单爆炸。标准做法是 HTTP 头注入深度计数（如 `x-openrouter-fusion-depth`），一旦 ≥ 1 立即熔断为单模型普通回答。^[raw/Fusion.md]

### 优雅降级
任何单点失败都不应阻塞整体流程：
- 部分面板失败 → 返回 `failed_models`，继续推进
- 裁判失败 → 外层直接从原始回答撰写
- 所有面板失败 → 返回 `failure_reason`，由调用方处理

^[raw/Fusion.md]

## 性能特征

| 指标 | 数据 | 可信度 |
|---|---|---|
| 成本 | 默认 3 模型面板 ≈ 单次调用 4–5 倍 | 官方文档量化 |
| 延迟 | 社区说法 2–3 倍 | **未经官方证实** |
| 面板上限 | 1–8 模型 | **社区说法，未经官方证实** |

总延迟 ≈ **最慢面板成员 + 裁判 + 外层合成**（fan-out 并行），而非各模型之和。^[raw/Fusion.md]

## 适用与不适用

**适合**：
- 研究型问题（需要多角度、深覆盖）
- 跨领域批判（每个领域由擅长模型负责）
- 容错成本高的场景（金融建议、医疗、法律研究）
- 单一最强模型都回答不好的难题

**不适合**：
- 简单事实查询（成本不划算）
- 强实时性场景（面板调度增加基础延迟）
- 隐私敏感数据（扇出到多个第三方供应商）

^[raw/Fusion.md]

## 常见误用

| 误用 | 后果 |
|---|---|
| 把面板调成"全 Claude 多版本" | 失去跨供应商视角，退化为昂贵单模型 |
| 让裁判模型"自由总结"而非强制 JSON | 五维结构化为空谈，分歧被抹平 |
| 不设递归保护就嵌套审议 | 成本失控，单次请求可烧光月度预算 |
| 忽略 `blind_spots` 维度 | 外层模型照搬共识，看似完整实则有重大遗漏 |

## 相关页面

- [[openrouter-fusion]] — 多模型审议范式的服务端实现
- [[sub-agent]] — 纵向分工（执行/验证），与本文横向分工互补
- [[loop-engineering]] — 五大代际中"多 Agent 编排 Loop"对应此范式
- [[claude-code]] / [[codex]] — 走单模型深耕路线的对照实现

## 引用

- [OpenRouter Fusion 官方文档](https://openrouter.ai/docs/features/fusion)
- 原始分析笔记：`raw/Fusion.md`
- 性能基准：[DRACO（Deep Research Benchmark）](https://github.com/HKUDS/DRACO)
