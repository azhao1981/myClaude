---
source_url: https://mp.weixin.qq.com/s/ALuFleuLG6_fBlnn5Jnlnw
ingested: 2026-06-15
sha256: d1574e43eb1b8a33d5646d3a4e9d0c816ad557383abd23238a6cdd63b31e6ac9
---

# 一文读懂什么是 Loop，Claude Fable 5 是 Loop 最严厉的父亲

最近 Loop 这个话题受到了很多关注。Claude Code 之父 Boris Cherny 这两天在回顾 cc 一周年时提到，他现在的工作就是写 Loop。

Boris 这句话的背景是在过去一年半里，Anthropic 内部的工程师经历了两次认知的转变。

第一次发生在大约一年半前。工程师开始意识到，他们不需要直接写源代码，只需要跟 Agent 说话，让 Agent 来写代码。

第二次正在发生。工程师不再直接跟 Agent 对话，而是跟 Loop 或例程交互，由 Loop 调度 Agent，Agent 再去写代码。

人从执行者，变成了系统设计者。

## Loop 到底是什么

谷歌云 AI 工程总监 Addy Osmani 给了一个清晰的描述：**Loop Engineering，就是用你设计的系统替代你本人去提示 Agent。**

你不再是那个不断输入指令的人，你是那个设计循环结构的人。

Loop 可以理解为一个递归目标：你定义一个目的，AI 持续迭代直到完成。它大概由五个模块和一个记忆机制构成。

OpenAI 的 Codex 和 Anthropic 的 Claude Code，两款产品目前都已具备这五个模块。

### 模块一：自动化调度

自动化让 Loop 成为真正的循环，而不是你手动跑一次就结束的东西。

在 Codex 里，你在 Automations 标签页里创建任务，选好项目、Prompt、执行频率，以及是在本地检出环境还是后台工作树上运行。有发现的运行进入 Triage 收件箱，什么都没发现的自动归档。Claude Code 的做法是通过调度和钩子。你可以用 /loop 按固定间隔运行 Prompt 或命令，可以设置 cron 任务，可以在 Agent 生命周期的特定节点触发 shell 命令，也可以把整套流程推到 GitHub Actions 上。

还有一个值得单独讲的指令：**/goal**。它不是按频率循环，而是一直跑到你写的条件为真才停。每一轮结束后，一个独立的小模型负责判断是否已完成，这意味着写代码的 Agent 不是给自己评分的那个。

### 模块二：工作树隔离

同时跑多个 Agent 的第一个问题，是文件冲突。

git worktree 解决了这个问题。它是一个在独立分支上的独立工作目录，和同一个仓库历史共享，一个 Agent 的改动物理上无法触碰另一个 Agent 的检出。

Codex 内置了 worktree 支持。Claude Code 通过 git worktree、--worktree 标志以及子 Agent 上的 isolation: worktree 配置实现同样的隔离。

需要注意的是，worktree 解决的是机械层面的冲突，**你的 Review 带宽才是真正的上限。**

### 模块三：Skill

Skill 解决的是一个基本问题：每次新对话，你不应该再重新解释一遍整个项目背景。

两款工具用的格式相同：一个包含 SKILL.md 文件的文件夹，里面放指令和元数据，外加可选的脚本、参考资料和资产文件。

Skill 的另一层价值是固化意图。Agent 每次启动都是空白的，它会用自己的推断填补你没说清楚的地方。Skill 是把意图写在外部。**没有 Skill 的 Loop，每轮都从零推导你的项目；有了 Skill，它是在复利增长的。**

Skill 是撰写格式，Plugin 是分发格式。

### 模块四：插件与连接器

只能看到文件系统的 Loop，能做的事很有限。

Connectors 建立在 MCP 协议之上，让 Agent 能读取 issue tracker、查询数据库、访问 staging API、往 Slack 发消息。Codex 和 Claude Code 都支持 MCP。

这是 Agent 说"这是修复方案"和 Loop 自动开 PR、关联 Linear 票、CI 绿了自动通知频道之间的差距。

### 模块五：子 Agent

Loop 里最有用的结构设计，是把写代码的和检查代码的分开。

写代码的模型给自己的代码打分，会打得太好看。用不同指令、有时还用不同模型的第二个 Agent，会抓到第一个说服自己接受了的问题。

Codex 按需生成子 Agent，你在 .codex/agents/ 里用 TOML 文件定义。Claude Code 在 .claude/agents/ 里同样设置子 Agent。两款工具里常见的分工是：一个探索，一个实现，一个对照规格验证。

> /goal 在底层做的，本质上也是这个拆分：Loop 是否完成，由一个新鲜的模型来判断，不是那个做了工作的。

### 加一个记忆机制

Loop 的第六个组件，通常听起来太朴素：一个 markdown 文件，或一块 Linear 看板，任何存在于单次对话之外、记录已做什么和下一步做什么的东西。

**模型会忘，仓库不会。** 记忆必须在磁盘上，不能只在上下文里。

## 一个完整 Loop 长什么样

把这些组件拼在一起，单个线程就变成了一个小型控制系统。

每天早晨，一个自动化任务在仓库上跑。它的 Prompt 调用一个 Triage Skill，读取昨天的 CI 失败记录、未关闭的 issue、最近的提交，把发现写进一个 markdown 文件或 Linear 看板。对于每个值得处理的发现，开一个独立的工作树，派一个子 Agent 去起草修复方案，再派第二个子 Agent 对照项目 Skill 和现有测试来审查这份草案。

Connectors 让 Loop 自动开 PR、更新票据。状态文件是整个系统的骨架。你设计了一次，之后没有手动提示任何一步。

## Loop 做不了的三件事

**验证还是你的责任。** 无人看守跑的 Loop，也是无人看守地犯错。"完成"是个声明，不是证明。

**你对代码库的理解会腐烂。** Loop 发出代码的速度越快，实际存在的代码和你真正理解的代码之间的差距就越大。这是理解债。

**不作为也是一种风险。** 当 Loop 自己跑起来，很容易停止有自己的判断，拿到什么就接受什么。这是认知放弃。

## Claude Fable 5 的自校正实验

Anthropic 内部工程师 Lance Martin 做了一组实验，专门测试 Loop 模式在最新模型上的效果。

他用的任务叫 Parameter Golf。有一个关键细节：**谁来评分很重要。** 研究发现，模型给自己的输出打分效果差，用独立的验证子 Agent 比自我评价效果更好。

结果：Fable 5 对训练流程的改进幅度大约是 Opus 4.7 的 6 倍。Fable 5 倾向于下更大的结构性赌注，比如架构改动。Opus 4.7 的第一次实验产生了一个小提升，之后几乎全是同一个模式：调一个标量，测量，正向就保留。

内存能力上，Fable 5 倾向于走完整个路径：失败并记录，调查原因，核实诊断结论，提炼为通用规则，下次直接查规则而不是重新推导。最强运行里核实覆盖率达到 73%。

## 两款主流工具的对比

| 模块 | Claude Code | Codex |
| --- | --- | --- |
| 自动化调度 | /loop、cron、hooks、GitHub Actions | Automations 标签页；/goal 跑到条件为真才停 |
| 工作树隔离 | git worktree、--worktree 标志 | 内置 worktree 支持 |
| Skill 格式 | .claude/agents/ + SKILL.md | .codex/agents/ + SKILL.md |
| 连接器协议 | MCP | MCP |

## 写在最后

Boris Cherny 的那句话，最后落地的意思不是工作变简单了，而是杠杆支点移动了。以前杠杆在 Prompt，现在杠杆在 Loop 的设计。

同样的 Loop，两个人用会产生完全不同的结果。一个人用它更快地推进自己深度理解的工作，另一个人用它来回避真正理解工作。

这也是为什么 Loop 设计比 Prompt 工程更难，不是更容易。Loop 需要你有很深的工程技术背景，还要烧得起 tokens。
