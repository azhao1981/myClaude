---
title: OpenAI Codex
created: 2026-06-15
updated: 2026-06-15
type: entity
tags: [product, tool, loop-engineering, agent-orchestration]
sources: [raw/articles/loop-wtf-is-a-loop-2026.md, raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: high
---

# OpenAI Codex

## 概述

OpenAI 推出的 AI 编程智能体工具，与 [[claude-code]] 并列为 [[loop-engineering]] 两大主流工具。^[raw/articles/loop-fable5-strictest-father-2026.md]

## Loop Engineering 六大模块的实现

| 模块 | Codex 实现 |
|---|---|
| [[automation]] | Automations 标签页，设置项目/Prompt/频率/运行环境 |
| [[worktree]] | 内置 worktree 支持，多线程同时操作同仓库不互相干扰 |
| [[skill]] | `.codex/agents/` + `SKILL.md`，用 `$` 或 `/skills` 调用 |
| [[connector]] | [[mcp]] 协议 |
| [[sub-agent]] | `.codex/agents/` 里用 TOML 文件定义，可选模型和推理力度 |
| Memory | 状态文件、Triage 收件箱 |

## 关键功能

- **Automations**：有发现的运行进入 Triage 收件箱，什么都没发现的自动归档^[raw/articles/loop-fable5-strictest-father-2026.md]
- **/goal**：运行到条件为真才停，支持暂停和恢复^[raw/articles/loop-fable5-strictest-father-2026.md]
- **Skill 自动触发**：任务描述匹配时自动触发，这也是为什么 Skill 描述越准确越好^[raw/articles/loop-fable5-strictest-father-2026.md]

## 与 Claude Code 的对比

| 模块 | Claude Code | Codex |
|---|---|---|
| 自动化调度 | `/loop`、cron、hooks、GitHub Actions | Automations 标签页 + `/goal` |
| 工作树隔离 | `git worktree`、`--worktree` | 内置 worktree 支持 |
| Skill 格式 | `.claude/agents/` | `.codex/agents/` |
| 连接器协议 | MCP | MCP |

详见 [[claude-code-vs-codex]]。

## 相关页面

- [[loop-engineering]] — 其支持的范式
- [[claude-code]] — 竞品对比
- [[skill]] — 可复用单位
