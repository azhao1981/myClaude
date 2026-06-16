---
title: Loop Engineering
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [loop-engineering, agent-orchestration, automation, paradigm]
sources: [raw/articles/loop-wtf-is-a-loop-2026.md, raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: high
---

# Loop Engineering

## TL;DR

围绕 AI 编程智能体设计一个**可重复、可观察、可验证、可修正**的工作循环。^[raw/articles/loop-engineering-new-paradigm-2026.md]

核心公式:**Loop = cron + 长在里面的决策者**^[raw/articles/loop-wtf-is-a-loop-2026.md]。六构件:Automation(自动化调度)、Worktree(工作树隔离)、Skill(技能)、Connector/MCP(连接器)、Sub-agent(子 Agent)、Memory(记忆)。五年代际:ReAct(2022)→ AutoGPT(2023)→ Ralph Loop(2025.7)→ /goal 命令(2026 春)→ 多 Agent 编排 Loop(2026.6)。主流落地产品:Claude Code(Anthropic)、Codex(OpenAI),均已具备上述全部构件。

> "Loop Engineering，就是用你设计的系统替代你本人去提示 Agent。" —— Addy Osmani(谷歌云 AI 工程总监)^[raw/articles/loop-fable5-strictest-father-2026.md]

## 定义

**Loop Engineering** 是围绕 AI 编程智能体设计一个可重复、可观察、可验证、可修正的工作循环。^[raw/articles/loop-engineering-new-paradigm-2026.md]

> "Loop Engineering，就是用你设计的系统替代你本人去提示 Agent。" —— Addy Osmani（谷歌云 AI 工程总监）^[raw/articles/loop-fable5-strictest-father-2026.md]

你不再是那个不断输入指令的人，你是那个**设计循环结构的人**。模型从「对话伙伴」变成了「子程序」。

Loop 可以理解为一个**递归目标**：你定义一个目的，AI 持续迭代直到完成。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 核心公式

**Loop = cron + 长在里面的决策者**^[raw/articles/loop-wtf-is-a-loop-2026.md]

- cron job 跑固定脚本；Loop 跑一个模型——它查看当前状态，决定下一步做什么，检查是否有效，决定是否继续
- 决策是 Agent 做的，不是硬编码的分支判断
- 有趣的工程问题全在于你围绕决策者包了多少东西，让它不跑偏

## 与 Prompt Engineering 的区别

| 维度 | Prompt Engineering | Loop Engineering |
|---|---|---|
| 关注点 | 单次提示词效果 | 持续任务闭环 |
| 典型问题 | 怎么问 AI 更准确 | 如何让 AI 可靠推进一组任务 |
| 输出形态 | 回答、代码片段 | 自动化流程、可验证结果 |
| 人类角色 | 提问者、修正者 | 流程设计者、约束制定者、审查者 |

详见 [[prompt-vs-loop-engineering]]。

Prompt Engineering 并未过时——它从舞台中央退到系统内部，变成循环中的一个组件。^[raw/articles/loop-engineering-new-paradigm-2026.md]

## 六大核心构件

| 构件 | 作用 | 解决的问题 |
|---|---|---|
| [[automation]]（自动化调度） | 定时触发任务，循环的心跳 | 人不必反复手动检查 |
| [[worktree]]（工作树隔离） | 给每个 Agent 独立 checkout | 多个 Agent 修改互相冲突 |
| [[skill]]（技能） | 沉淀项目知识，可复用单位 | 每轮都从零理解项目 |
| [[connector]]（连接器） | 基于 [[mcp]] 接入真实工具链 | AI 只能停留在本地文件 |
| [[sub-agent]]（子 Agent） | 分离执行与验证 | 实现者自我审查不可靠 |
| Memory（记忆） | 记录长期状态 | 上下文跨轮次丢失 |

> 模型会忘，仓库不会。记忆必须在磁盘上，不能只在上下文里。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 进化阶梯

Loop 并非新概念，它有五年血统：^[raw/articles/loop-wtf-is-a-loop-2026.md]

1. **2022 — ReAct 论文**：模型推理→调用工具→读取结果→重复（学术 while 循环）
2. **2023 — AutoGPT**：给目标自己写 Prompt，但永远空转
3. **2025.7 — [[ralph-loop]]**：bash 单行命令反复传同一 Prompt，每次重置上下文
4. **2026 春 — /goal 命令**：[[codex]] 和 [[claude-code]] 产品化，跑到验证器确认完成
5. **2026.6 — 多 Agent 编排 Loop**：Loop 监督其他 Loop，并发调度，持久状态，崩溃恢复

详见 [[loop-evolution-timeline]]。

## 一个完整 Loop 的工作流程

```
每天早晨 → Automation 触发
  → 调用 Triage Skill，读取 CI 失败/issues/commits
  → 整理发现写入状态文件（Memory）
  → 为每个值得处理的问题开独立 worktree
  → Sub-agent A 起草修复方案
  → Sub-agent B 审查（对照项目 Skill 和测试）
  → 测试失败？→ 反馈给实现 Agent 继续修
  → 测试通过？→ Connectors 自动开 PR/关联 ticket
  → 状态文件记录进展 → 明天从今天停的地方继续
```

你设计了一次，之后没有手动提示任何一步。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 四大风险

| 风险 | 说明 |
|---|---|
| **验证是你的责任** | 无人看守的 Loop 也会无人看守地犯错。"完成"是声明，不是证明 |
| **理解债** | Loop 发代码越快，你真正理解的代码和实际存在的代码差距越大 |
| **Token 成本失控** | Uber 四个月烧完全年预算；无限循环账单超预算数个数量级 |
| **认知投降** | 从「设计系统」退化成「按下启动」，Loop 从杠杆变成黑箱 |

三个硬性停止条件：**最大迭代次数、无进展检测、token/美元预算上限。**^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 关键引言

> "我不给 Claude 写 Prompt 了。我运行 Loop，由 Loop 来给 Claude 写 Prompt，决定做什么。我的工作是写 Loop。" —— [[boris-cherny]]^[raw/articles/loop-wtf-is-a-loop-2026.md]

> "你不应该再手动给编程 Agent 写 Prompt 了。你应该设计 Loop 来让 Agent 自己写 Prompt。" —— [[peter-steinberger]]^[raw/articles/loop-wtf-is-a-loop-2026.md]

## 一句话总结

**Loop 是杠杆，不是替身。它能放大一个工程师的判断，也会放大一个工程师的缺席。**^[raw/articles/loop-engineering-new-paradigm-2026.md]

Loop Engineering 比 Prompt Engineering 更难——它不只考验写提示词，还考验对软件工程流程、状态、边界、反馈和责任的理解。^[raw/articles/loop-engineering-new-paradigm-2026.md]

## 相关页面

- [[sub-agent]] — 六大构件之一，纵向分工（执行/验证）
- [[automation]] — 六大构件之一，循环的心跳
- [[worktree]] — 六大构件之一，并行隔离层
- [[skill]] — 六大构件之一，可复用单位
- [[mcp]] — Connector 的底层协议
- [[ralph-loop]] — 进化阶梯第三阶段
- [[multi-model-deliberation]] — 五大代际中"多 Agent 编排 Loop"阶段的代表性范式
- [[prompt-vs-loop-engineering]] — 范式对比
