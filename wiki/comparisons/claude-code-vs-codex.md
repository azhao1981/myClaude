---
title: Claude Code vs Codex
created: 2026-06-15
updated: 2026-06-15
type: comparison
tags: [comparison, claude-code, codex, loop-engineering]
sources: [raw/articles/loop-fable5-strictest-father-2026.md]
confidence: high
---

# Claude Code vs Codex

## 概述

[[claude-code]]（Anthropic）和 [[codex]]（OpenAI）是 [[loop-engineering]] 两大主流工具，在五个核心模块上的设计高度一致，只是名字和入口有所不同。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 模块对比

| 模块 | Claude Code | Codex |
|---|---|---|
| [[automation]] | `/loop`、cron、hooks、GitHub Actions | Automations 标签页；`/goal` 支持暂停和恢复 |
| [[worktree]] | `git worktree`、`--worktree` 标志 | 内置 worktree 支持 |
| [[skill]] | `.claude/agents/` + `SKILL.md` | `.codex/agents/` + `SKILL.md`，用 `$` 或 `/skills` 调用 |
| [[connector]] | [[mcp]] | [[mcp]] |
| [[sub-agent]] | `.claude/agents/` 组成团队 | `.codex/agents/` TOML 定义，可选模型和推理力度 |

## /goal 命令差异

两者都有 `/goal` 命令（跑到条件为真才停），但 Codex 额外支持暂停和恢复。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 共同点

- 都支持 [[mcp]] 协议，Connector 跨工具兼容^[raw/articles/loop-fable5-strictest-father-2026.md]
- 都用 `SKILL.md` 格式定义 [[skill]]^[raw/articles/loop-fable5-strictest-father-2026.md]
- 常见的子 Agent 分工模式相同：一个探索，一个实现，一个对照规格验证^[raw/articles/loop-fable5-strictest-father-2026.md]

## 相关页面

- [[claude-code]] / [[codex]] — 各自实体页
- [[loop-engineering]] — 共同支持的范式
- [[prompt-vs-loop-engineering]] — 更广泛的范式对比
