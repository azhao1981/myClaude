---
title: Automation
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [automation, loop-engineering]
sources: [raw/articles/loop-wtf-is-a-loop-2026.md, raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: high
---

# Automation（自动化调度）

## 定义

Automation 是 [[loop-engineering]] 循环的**心跳**——让 Loop 成为真正的循环，而不是手动跑一次就结束。^[raw/articles/loop-engineering-new-paradigm-2026.md]

没有自动触发机制，所谓 Loop 只是你手动执行了一次任务。只有当它可以按时间、事件或条件自动启动，循环才会拥有自己的节奏。^[raw/articles/loop-engineering-new-paradigm-2026.md]

## 调度方式

| 工具 | 实现 |
|---|---|
| [[codex]] | Automations 标签页，设置项目/Prompt/频率/运行环境 |
| [[claude-code]] | `/loop`、cron、hooks、GitHub Actions |

- 有发现的运行进入 Triage 收件箱，什么都没发现的自动归档^[raw/articles/loop-fable5-strictest-father-2026.md]
- [[boris-cherny]] 真的就是用 cron 跑的^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 停止条件（最关键）

> 当循环有了可验证的终点，它就不再只是盲目重试。^[raw/articles/loop-engineering-new-paradigm-2026.md]

**/goal** 命令不是按频率循环，而是一直跑到你写的条件为真才停。每一轮结束后，一个独立的小模型负责判断是否已完成——写代码的 Agent 不是给自己评分的那个。^[raw/articles/loop-fable5-strictest-father-2026.md]

三个硬性停止条件：**最大迭代次数、无进展检测、token/美元预算上限。**^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 成本风险

> Uber 在四个月烧完全年 AI 预算后，给工程师设了每人每工具每月 1500 美元上限。^[raw/articles/loop-wtf-is-a-loop-2026.md]

> "没有护栏，你就会遇到无限循环，账单超出预算数个数量级。"^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 相关页面

- [[loop-engineering]] — Automation 是其心跳
- [[worktree]] — 自动化调度的并行隔离层
- [[claude-code]] / [[codex]] — 实现载体
