---
title: Prompt Engineering vs Loop Engineering
created: 2026-06-15
updated: 2026-06-15
type: comparison
tags: [comparison, prompt-engineering, loop-engineering]
sources: [raw/articles/loop-wtf-is-a-loop-2026.md, raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: high
---

# Prompt Engineering vs Loop Engineering

## 范式转移

AI 编程的关键能力，正在从「写好提示词」升级为「设计可持续运转的智能体工作系统」。^[raw/articles/loop-engineering-new-paradigm-2026.md]

这并非说 Prompt Engineering 过时了——它从舞台中央退到系统内部，变成 [[loop-engineering]] 循环中的一个组件。就像写代码时单个函数很重要，但真正决定系统质量的是函数之间如何协作。^[raw/articles/loop-engineering-new-paradigm-2026.md]

## 维度对比

| 维度 | Prompt Engineering | Loop Engineering |
|---|---|---|
| **关注点** | 单次提示词效果 | 持续任务闭环 |
| **典型问题** | 怎么问 AI 更准确 | 如何让 AI 可靠推进一组任务 |
| **输出形态** | 回答、建议、代码片段 | 自动化流程、协作链路、可验证结果 |
| **人类角色** | 提问者、修正者 | 流程设计者、约束制定者、审查者 |
| **风险控制** | 依赖提示词约束 | 依赖权限、验证、反馈、人工门禁 |
| **可复用单位** | Prompt | [[skill]] |
| **成本中心** | Token | Loop 管理 |

## 具体示例

**Prompt Engineering 方式：**
> "帮我修复这个登录失败的 bug。"

**Loop Engineering 方式：**
> "每天早上读取昨天的 CI 失败记录和用户反馈，找出高优先级 bug，为每个 bug 创建隔离工作区，生成修复方案，运行测试，失败后继续修正，通过后生成 PR，并把无法处理的部分写入待办清单。"

前者是一条指令，后者是一套系统。^[raw/articles/loop-engineering-new-paradigm-2026.md]

## 杠杆支点的移动

[[boris-cherny]] 的核心观点：工作没有消失，它上升了一个高度——从写代码变成了写那个写代码的东西。^[raw/articles/loop-wtf-is-a-loop-2026.md]

- 以前：杠杆在 Prompt，写好 Prompt 就能从 Agent 那里得到好结果
- 现在：杠杆在 Loop 的设计，你设计的系统质量决定产出质量^[raw/articles/loop-fable5-strictest-father-2026.md]

## 为什么 Loop Engineering 更难

同样的 Loop，两个人用会产生完全不同的结果：^[raw/articles/loop-fable5-strictest-father-2026.md]

- 一个人用它更快地推进自己深度理解的工作
- 另一个人用它来回避真正理解工作

Loop Engineering 不只考验写提示词，还考验你是否理解软件工程里的流程、状态、边界、反馈和责任。^[raw/articles/loop-engineering-new-paradigm-2026.md]

## 相关页面

- [[loop-engineering]] — 核心概念详解
- [[skill]] — Loop 中的可复用单位
- [[boris-cherny]] / [[peter-steinberger]] — 关键推动者
