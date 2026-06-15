---
title: Ralph Loop
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [ralph-loop, agent-orchestration, timeline]
sources: [raw/articles/loop-wtf-is-a-loop-2026.md]
confidence: high
---

# Ralph Loop

## 定义

**Ralph Loop** 是 [[loop-engineering]] 进化阶梯的第三阶段，由 Geoffrey Huntley 于 2025 年 7 月发布。^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 核心特征

它简单得近乎侮辱人——**一个 bash 单行命令，一遍又一遍地把同一个 Prompt 文件传给 Agent。**^[raw/articles/loop-wtf-is-a-loop-2026.md]

真正的创新不是技术复杂度，而是**纪律**：
- 每次迭代把上下文重置为一组固定的锚点文件
- 而不是让对话无限增长

## 成果

Huntley 用 ralph loop 构建了一整套编程语言，花了大约 **297 美元**。^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 历史定位

> "不是 ralph/goal loop，那个已经过时了。大概是某种持续编排 Loop，负责监督其他线程/Agent。" —— @trashpandaemoji^[raw/articles/loop-wtf-is-a-loop-2026.md]

- Ralph 假设你的终端一直开着^[raw/articles/loop-wtf-is-a-loop-2026.md]
- 2026 版本（多 Agent 编排 Loop）假设它不会

Ralph loop 是从 AutoGPT 的失败到 /goal 产品化之间的关键桥梁——它证明了"重置上下文"的纪律性比"让对话无限增长"更有效。

## 进化脉络

| 阶段 | 代表 | 与 Ralph 的关系 |
|---|---|---|
| 前身 | AutoGPT（2023） | 让对话无限增长，永远空转 |
| **本阶段** | **Ralph Loop（2025.7）** | **固定锚点 + 上下文重置** |
| 后继 | /goal 命令（2026春） | 产品化 ralph loop + 验证器模型 |

## 相关页面

- [[loop-engineering]] — 核心范式
- [[claude-code]] / [[codex]] — 将 ralph loop 产品化为 /goal
