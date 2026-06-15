---
source_url: https://mp.weixin.qq.com/s/2W45sMEP282_Kcz8AOYOYg
ingested: 2026-06-15
sha256: 03a8231bc3c6b531958366542a9ad2a2405b2ae39949b363be66a37f76e762e0
---

# 一文看懂 AI 编程智能体工程化新范式：Loop Engineering

过去两年，我们谈 AI 编程，最常说的词是 Prompt Engineering。

以前，我们像是在一轮一轮地「指挥」AI：你写一句提示词，它回一段代码；你指出问题，它再改一版。整个过程里，人始终站在每一轮交互的入口处。

现在，一个新的思路开始出现：与其每次都手动提示智能体，不如设计一个系统，让这个系统去发现任务、分配任务、检查结果、记录状态，并决定下一步。

AI 编程的关键能力，正在从「写好提示词」升级为「设计可持续运转的智能体工作系统」。

这个工程化新范式，就是最近被频繁讨论的 **Loop Engineering**。

## 为什么 Prompt Engineering 不够用了？

Peter Steinberger 最近说过一句话：

> You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents.

Claude Code 负责人 Boris Cherny 也表达过类似观点：

> I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops.

这两句话背后，指向同一个趋势：AI 编程协作的重心，正在从「人反复输入 Prompt」转向「人设计一个持续运行的工作循环」。

为什么会有这个变化？因为真实的软件开发，从来都不只是一次问答。它包含需求澄清、方案设计、代码修改、测试验证、错误修复、文档更新、代码审查、发布跟进。每一步都可能失败，每一步都需要反馈。

**Prompt Engineering 关注的是「这一轮怎么问得更好」，Loop Engineering 关注的是「整个流程怎么持续变好」。**

这并不意味着 Prompt Engineering 过时了。提示词仍然重要，只是它从舞台中央退到系统内部，变成循环中的一个组件。

## Loop Engineering 到底是什么？

**Loop Engineering，是围绕 AI 编程智能体设计一个可重复、可观察、可验证、可修正的工作循环。**

这里的 Loop，可以理解为一个递归目标。你给出目标、上下文、工具权限和停止条件，AI 在这个边界内持续迭代，直到任务完成，或者遇到需要人类判断的节点。

它关心的问题包括：
- AI 什么时候启动？
- 它读取哪些上下文？
- 它能调用哪些工具？
- 它如何知道自己做对了？
- 失败后怎么继续修正？
- 哪些操作必须交给人确认？
- 状态如何在下一轮继续使用？

### Prompt Engineering vs Loop Engineering

| 维度 | Prompt Engineering | Loop Engineering |
| --- | --- | --- |
| 关注点 | 单次提示词效果 | 持续任务闭环 |
| 典型问题 | 怎么问 AI 更准确 | 如何让 AI 可靠推进一组任务 |
| 输出形态 | 回答、建议、代码片段 | 自动化流程、协作链路、可验证结果 |
| 人类角色 | 提问者、修正者 | 流程设计者、约束制定者、审查者 |
| 风险控制 | 依赖提示词约束 | 依赖权限、验证、反馈、人工门禁 |

传统 Prompt Engineering 的问题可能是：「帮我修复这个登录失败的 bug。」

Loop Engineering 的问题会变成：「每天早上读取昨天的 CI 失败记录和用户反馈，找出高优先级 bug，为每个 bug 创建隔离工作区，生成修复方案，运行测试，失败后继续修正，通过后生成 PR，并把无法处理的部分写入待办清单。」

前者是一条指令，后者是一套系统。

## 一个 Loop 需要哪些核心构件？

一个 Loop 大致需要五个核心构件，再加一层外部记忆。

| 构件 | 作用 | 解决的问题 |
| --- | --- | --- |
| Automations | 定时触发任务 | 人不必反复手动检查 |
| Worktrees | 隔离并行工作 | 多个 agent 修改互相冲突 |
| Skills | 沉淀项目知识 | 每轮都从零理解项目 |
| Connectors | 接入真实工具 | AI 只能停留在本地文件 |
| Sub-agents | 分离执行和验证 | 实现者自我审查不可靠 |
| Memory | 记录长期状态 | 上下文跨轮次丢失 |

### Automations：循环的心跳

Automation 是让 Loop 真正「循环」起来的部分。只有当它可以按时间、事件或条件自动启动，循环才会拥有自己的节奏。

更关键的是停止条件。比如「所有 auth 测试通过，并且 lint 整洁」。当循环有了可验证的终点，它就不再只是盲目重试。

### Worktrees：并行工作的隔离层

Git worktree 的作用，就是给每个 agent 一个独立 checkout。它们共享同一份仓库历史，但在不同目录里工作。

不过，**Worktrees 只能解决机械冲突，不能解决人的审查带宽。**

### Skills：项目知识的沉淀方式

Skill 的价值，就是把这些项目知识、开发约定、构建步骤、历史决策写成外部能力。这相当于给 Loop 建了一套项目操作手册。

没有 Skills，Loop 每轮都在重新理解项目；有了 Skills，项目意图才会逐渐形成复利效应。

### Plugins / Connectors：连接真实工具链

真实开发发生在更大的系统里：issue tracker、PR、CI、数据库、监控平台、Slack、Linear、Notion、内部 API。

工具链连接越深，权限设计越要保守。

### Sub-agents：把执行者和检查者分开

在无人值守的 Loop 里，最重要的结构之一，是把 maker 和 checker 分开。

这并不意味着 sub-agent 越多越好。更合理的做法，是在高风险、高价值、需要第二判断的环节使用它们。

### Memory：让循环跨轮次延续

模型会忘记，仓库不会。这个 Memory 可以是一个 Markdown 文件，也可以是 Linear board、issue 列表、状态表、任务清单。

没有 Memory，Loop 每次启动都像失忆。有了 Memory，Loop 才有连续性。

## 一个真实 Loop 是怎么跑起来的？

每天早上，Automation 自动在项目里运行。它调用一个 triage skill，读取昨天的 CI 失败、open issues、recent commits，以及团队反馈。

接着，它把发现的问题整理到一个 Markdown 状态文件。对于值得处理的问题，Loop 会创建一个独立 worktree。一个 sub-agent 进入这个 worktree，阅读项目 skills，理解相关代码，起草修复方案。

修改完成后，另一个 sub-agent 接手审查。如果测试失败，Loop 会把失败输出重新送回实现 agent。如果测试通过，Connectors 可以打开 PR、关联 ticket。

| 阶段 | AI 可以做什么 | 人类需要把关什么 |
| --- | --- | --- |
| 发现问题 | 读取 CI、issue、commit，整理异常 | 判断优先级是否符合业务目标 |
| 拆解任务 | 生成修复计划和影响范围 | 判断方案方向是否合理 |
| 编码实现 | 修改代码、补测试、更新文档 | 审查关键逻辑和边界条件 |
| 验证反馈 | 运行测试、根据失败继续修复 | 判断测试信号是否足够可信 |
| 提交结果 | 生成 PR、更新 ticket、写变更说明 | 决定是否合并与发布 |

## 构建 Loop，但不要离开驾驶位

越是能自动运行的系统，越需要认真设计边界。

**第一个风险是 token 成本。** Automation、sub-agents、长上下文、反复验证，都会快速放大消耗。

**第二个风险是无人值守错误。** Loop 可以无人值守地运行，也可能无人值守地犯错。它生成的「done」只是一个声明，不等于代码真的可靠。

**第三个风险是理解债。** AI 帮你写得越快，你越容易来不及理解系统发生了什么。

**第四个风险是认知投降。** 当 Loop 足够顺滑，人很容易从「设计系统」退化成「按下启动」。

你需要做的事情包括：
1. 设计循环：明确任务如何启动、如何推进、如何停止。
2. 设定边界：规定 AI 能读什么、能写什么、哪些动作必须确认。
3. 沉淀上下文：用 Skills 和 Memory 记录项目规则与历史决策。
4. 选择验证信号：明确什么叫「完成」，什么叫「失败」。
5. 审查最终结果：确认代码真的工作，而不是只相信系统摘要。

**Loop 是杠杆，不是替身。它能放大一个工程师的判断，也会放大一个工程师的缺席。**

这也是为什么 Loop Engineering 比 Prompt Engineering 更难。它不只考验你会不会写提示词，还考验你是否理解软件工程里的流程、状态、边界、反馈和责任。
