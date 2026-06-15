---
title: Worktree
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [worktree, loop-engineering]
sources: [raw/articles/loop-wtf-is-a-loop-2026.md, raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: high
---

# Worktree（工作树隔离）

## 定义

**Worktree** 是 [[loop-engineering]] 中解决并行 Agent 文件冲突的隔离层。^[raw/articles/loop-fable5-strictest-father-2026.md]

同时跑多个 Agent 的第一个问题，是文件冲突。两个 Agent 写同一个文件，和两个工程师向同一行代码提交但彼此没沟通，是完全相同的麻烦。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 原理

`git worktree` 是一个在独立分支上的独立工作目录，和同一个仓库历史共享。一个 Agent 的改动物理上无法触碰另一个 Agent 的检出。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 实现

| 工具 | 实现 |
|---|---|
| [[codex]] | 内置 worktree 支持，多线程同时操作同仓库不互相干扰 |
| [[claude-code]] | `git worktree`、`--worktree` 标志、子 Agent 上 `isolation: worktree` 配置 |

每个子 Agent 拿到新鲜检出，结束后自动清理。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 关键限制

> Worktree 只能解决机械冲突，不能解决人的审查带宽。^[raw/articles/loop-fable5-strictest-father-2026.md]

> 你能同时跑多少个 Agent，取决于你有多少时间看它们的输出，而不是工具本身。^[raw/articles/loop-fable5-strictest-father-2026.md]

你可以同时跑十个 Agent，但最终仍然要有人判断哪个方案值得合并，哪个方案引入了隐患。^[raw/articles/loop-engineering-new-paradigm-2026.md]

## 相关页面

- [[loop-engineering]] — Worktree 是其并行隔离层
- [[automation]] — 调度并行任务的触发机制
- [[sub-agent]] — 在独立 worktree 中工作的执行单元
