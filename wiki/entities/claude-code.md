---
title: Claude Code
created: 2026-06-15
updated: 2026-06-15
type: entity
tags: [product, tool, loop-engineering, agent-orchestration]
sources: [raw/articles/loop-wtf-is-a-loop-2026.md, raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: high
---

# Claude Code

## 概述

Anthropic 推出的 AI 编程智能体工具，由 [[boris-cherny]] 于 2024 年 9 月作为副项目创建。据报道支撑着 GitHub 上接近 4% 的公开 commit。^[raw/articles/loop-wtf-is-a-loop-2026.md]

## Loop Engineering 六大模块的实现

| 模块 | Claude Code 实现 |
|---|---|
| [[automation]] | `/loop`、cron、hooks、GitHub Actions |
| [[worktree]] | `git worktree`、`--worktree` 标志、子 Agent 上 `isolation: worktree` |
| [[skill]] | `.claude/agents/` + `SKILL.md` |
| [[connector]] | [[mcp]] 协议 |
| [[sub-agent]] | `.claude/agents/` 目录定义 Agent 团队 |
| Memory | 状态文件、Linear 看板 |

## 关键命令

- **`/loop`**：按固定间隔运行 Prompt 或命令，底层是 cron^[raw/articles/loop-fable5-strictest-father-2026.md]
- **`/goal`**：一直跑到条件为真才停；每轮结束后由独立小模型判断是否完成（不是给自己评分的那个）^[raw/articles/loop-fable5-strictest-father-2026.md]

## 与 Codex 的对比

Claude Code 和 [[codex]] 在五个核心模块上的设计高度一致，只是名字和入口有所不同。两者都支持 [[mcp]] 协议。^[raw/articles/loop-fable5-strictest-father-2026.md]

详见 [[claude-code-vs-codex]]。

## 相关概念

- Claude Managed Agents（CMA）：提供 Agent 运行环境和托管沙盒，适合长期运行任务^[raw/articles/loop-fable5-strictest-father-2026.md]
- Outcomes：CMA 功能，自动生成评分子 Agent^[raw/articles/loop-fable5-strictest-father-2026.md]

## 相关页面

- [[boris-cherny]] — 创建者
- [[loop-engineering]] — 其推动的范式
- [[claude-code-settings]] — 四层 Scope 优先级与 `--settings` 合并规则
- [[codex]] — 竞品对比
