---
title: Sub-agent
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [sub-agent, loop-engineering, agent-orchestration]
sources: [raw/articles/loop-wtf-is-a-loop-2026.md, raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: high
---

# Sub-agent（子 Agent）

## 定义

**Sub-agent** 是 [[loop-engineering]] 中最重要的结构设计——**把写代码的（maker）和检查代码的（checker）分开。**^[raw/articles/loop-engineering-new-paradigm-2026.md]

## 核心原理

写代码的模型给自己的代码打分，会打得太好看。用不同指令、有时还用不同模型的第二个 Agent，会抓到第一个说服自己接受了的问题。^[raw/articles/loop-fable5-strictest-father-2026.md]

> /goal 在底层做的，本质上也是这个拆分：Loop 是否完成，由一个新鲜的模型来判断，不是那个做了工作的。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 实现方式

### Codex
- 按需生成子 Agent，同时运行后汇总结果^[raw/articles/loop-fable5-strictest-father-2026.md]
- 在 `.codex/agents/` 里用 TOML 文件定义，每个有名字、描述、指令、可选模型和推理力度
- 可以让安全审查 Agent 用强模型跑高强度推理，让探索 Agent 用快速的只读模式跑

### Claude Code
- 在 `.claude/agents/ 里设置子 Agent，组成 Agent 团队传递工作^[raw/articles/loop-fable5-strictest-father-2026.md]

### 常见分工
一个探索，一个实现，一个对照规格验证。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 使用原则

子 Agent 会消耗更多 token，因为每个都有自己的模型调用和工具使用。^[raw/articles/loop-fable5-strictest-father-2026.md]

- **不是越多越好**：每个 Agent 都消耗 token 和增加协调成本^[raw/articles/loop-engineering-new-paradigm-2026.md]
- **在高风险环节使用**：架构变更、权限逻辑、数据迁移、支付链路、发布前审查^[raw/articles/loop-engineering-new-paradigm-2026.md]
- **把 token 花在真正值得第二次确认的地方**^[raw/articles/loop-fable5-strictest-father-2026.md]

## 实验验证

Anthropic 内部工程师 Lance Martin 的实验发现：^[raw/articles/loop-fable5-strictest-father-2026.md]

- 模型给自己输出打分效果差
- 用独立的验证子 Agent 比自我评价效果更好，因为打分在独立的上下文窗口里完成
- CMA 的 Outcomes 功能会自动生成评分子 Agent

## 相关页面

- [[loop-engineering]] — Sub-agent 是其核心构件
- [[claude-code]] / [[codex]] — 实现载体
