---
title: Skill
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [skill, loop-engineering, automation]
sources: [raw/articles/loop-wtf-is-a-loop-2026.md, raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: high
---

# Skill

## 定义

**Skill** 是 [[loop-engineering]] 中可复用的基本单位——不是 Prompt，而是比 Prompt 更持久的知识封装。^[raw/articles/loop-wtf-is-a-loop-2026.md]

> "Loop 是管道。资产是它调用的 Skill。"^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 格式

一个包含 `SKILL.md` 文件的文件夹，里面放指令和元数据，外加可选的脚本、参考资料和资产文件。^[raw/articles/loop-fable5-strictest-father-2026.md]

- [[codex]]：`.codex/agents/` + `SKILL.md`，用 `$skill-name` 或 `/skills` 调用
- [[claude-code]]：`.claude/agents/` + `SKILL.md`，机制相同

Skill 是撰写格式，Plugin 是分发格式（跨仓库共享或打包多个 Skill）。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 解决的核心问题

每次新对话，Agent 不应该重新解释整个项目背景。^[raw/articles/loop-fable5-strictest-father-2026.md]

Skill 把这些固化在外部：
- 项目约定
- 构建步骤
- 历史踩过的坑
- 某个模块为什么不能重构

## 复利效应

> 没有Skill 的 Loop，每轮都从零推导你的项目；有了 Skill，它是在复利增长的。^[raw/articles/loop-fable5-strictest-father-2026.md]

Agent 每次启动都是空白的，它会用自己的推断填补你没说清楚的地方。Skill 是把意图写在外部——写一次，每次运行都能读到。^[raw/articles/loop-fable5-strictest-father-2026.md]

## Steinberger 的 Skill 哲学

[[peter-steinberger]] 反复强调：^[raw/articles/loop-wtf-is-a-loop-2026.md]

- 如果你做某件事超过一次，就把它变成自动化 Skill
- 如果你做了一件很难的事，事后也把它变成 Skill，下次就免费了
- 一个没有可复用 Skill 的 Loop，只是一个 `while true` 套着一个陌生人
- 调用有名字的、经过测试的 Skill 的 Loop 会复利增长

## Skill 描述的重要性

> 聪明的描述不如准确的描述管用。^[raw/articles/loop-fable5-strictest-father-2026.md]

在 Codex 中，Skill 可以在任务描述匹配时自动触发。因此 Skill 描述越准确越好——错误匹配会导致错误触发。

## 相关页面

- [[loop-engineering]] — Skill 是其中的核心构件
- [[peter-steinberger]] — Skill 哲学的推动者
- [[claude-code]] / [[codex]] — Skill 的实现载体
