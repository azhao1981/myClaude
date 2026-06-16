---
title: Boris Cherny
created: 2026-06-15
updated: 2026-06-15
type: entity
tags: [person, loop-engineering, claude-code]
sources: [raw/articles/loop-wtf-is-a-loop-2026.md, raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: high
---

# Boris Cherny

## 概述

[[claude-code]] 的创建者（Claude Code 之父），Anthropic 工程师。2024 年 9 月将 Claude Code 作为副项目创建，据报道该工具现在支撑着 GitHub 上接近 4% 的公开 commit。^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 核心观点

Boris 描述了工程师经历的三次认知转变：^[raw/articles/loop-fable5-strictest-father-2026.md]

1. **一年半前**：不需要直接写源代码，只需要跟 Agent 说话，让 Agent 来写代码
2. **正在发生**：不再直接跟 Agent 对话，而是跟 Loop 交互，由 Loop 调度 Agent
3. **个人实践**：从手写代码 → 同时跑 5-10 个会话逐个写 Prompt → 完全不写 Prompt，写 Loop

> "我不再手动给 Claude 写 Prompt 了。我运行 Loop，由 Loop 来给 Claude 写 Prompt，决定做什么。我的工作是写 Loop。"^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 实践数据

> "过去 30 天里，我对 Claude Code 的所有贡献，100% 由 Claude Code 自己写的。我提交了 259 个 PR。"^[raw/articles/loop-wtf-is-a-loop-2026.md]

他在 2025 年 11 月删掉了自己的 IDE，再也没有打开过。^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 五条 Loop 实践建议

关于让 Opus 自主运行数小时甚至数天：^[raw/articles/loop-wtf-is-a-loop-2026.md]

1. 用 auto mode 设置权限，Claude 不需要每次审批
2. 用 dynamic workflows 编排成百上千个 Agent
3. 用 /goal 或 /loop 推动持续运行直到完成
4. 把 Claude Code 放在云端，可以关上电脑
5. **确保 Claude 有办法端到端地自我验证产出**（最关键的一条）

## 标准入门模板

```
/loop babysit all my PRs. Auto-fix build issues, and when comments come in, use a worktree agent to fix them.
```

## 相关页面

- [[loop-engineering]] — 他推动的范式
- [[claude-code]] — 他创建的工具
- [[prompt-vs-loop-engineering]] — 范式对比
- [[claude-code-settings]] — 他设计的 settings 四层 Scope 体系
