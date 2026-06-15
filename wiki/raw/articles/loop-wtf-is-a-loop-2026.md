---
source_url: https://mp.weixin.qq.com/s/cxRvqwWW4Yo4UmufAsXEEA
ingested: 2026-06-15
sha256: 5c71d3fe0dc677ea777a494531f3623be2d04b87df666863e705f606c87f27b6
---

# 【译】别再手动写 Prompt 了，去写 Loop——但 Loop 到底是什么？

> Mike Van Horn — 自驾驶烤箱公司创始人（被 Weber 收购），Lyft 前身联合创始人 · @mvanhorn
> 原文：WTF Is a Loop? Peter Steinberger vs. Boris Cherny
> 链接：x.com/mvanhorn
> 发布：2026-06-08

【导读】本周 AI 编程圈被一条推文刷屏了：Peter Steinberger 说别再手动写 Prompt 了，去写 Loop。220 万浏览，评论区吵成一锅粥——因为几乎所有转发它的人都说不清 Loop 到底是什么。Mike Van Horn 花了一周时间翻遍了 Reddit、X、Hacker News，从 2022 年 ReAct 论文到 2026 年的多 Agent 编排，把 Loop 的五年代际、实战用法和隐性成本全翻出来了。这不是一篇追热点的文章，而是一份写给还困在 Loop 里敲 Prompt 的人的出门指南。

## 【概览】

- Loop 是你写的一个小程序，替你给 Agent 写 Prompt，判断是否完成，没完成就再来一轮
- 五年进化阶梯：ReAct（2022）→ AutoGPT（2023）→ ralph loop（2025）→ /goal（2026 春）→ 多 Agent 编排 Loop
- Loop 就是 cron 加一个长在里面的决策者，有趣的工程全在让决策者不跑偏
- Loop 的好坏取决于自我检查能力，验证比编排更重要
- 成本已从 token 转移到 Loop 管理——Uber 四个月烧完全年 AI 预算
- Loop 里的可复用单位是 Skill，不是 Prompt

## 让整个时间线窒息的推文

本周有一条推文让整个 AI 编程时间线陷入了疯狂。Peter Steinberger 在 6 月 7 日发了它，浏览量突破 220 万，评论区变成了一场关于它到底是什么意思的混战。

> "月度提醒：你不应该再手动给编程 Agent 写 Prompt 了。你应该设计 Loop 来让 Agent 自己写 Prompt。"
> ——Peter Steinberger (@steipete)，2026 年 6 月 7 日

最有代表性的回复来自 Varadh Jain，他问了唯一重要的问题：这在实际中长什么样？而成为整场讨论基调的回答，来自 Matthew Berman。

> "除了他和 Boris，没人知道。"
> ——Matthew Berman (@MatthewBerman)，2026 年 6 月 7 日

我没有翻白眼，因为我每晚都会跑一个 Loop，在我睡觉的时候给大约 30 个开源仓库提交 Pull Request。

一拨人喊 prompt engineering 已死。另一拨人——那些手上真的在敲键盘的——要谨慎得多。

> "不是 ralph/goal loop，那个已经过时了。大概是某种持续编排 Loop，负责监督其他线程/Agent。"
> ——@trashpandaemoji，2026 年 6 月 7 日

## Loop 到底是什么

Boris Cherny 在 2024 年 9 月把 Claude Code 作为副项目创建出来。据报道，它现在支撑着 GitHub 上接近 4% 的公开 commit。

在 6 月 2 日由 WorkOS 主办的 Acquired Unplugged 活动上，他给出了你能找到的最清晰的 Loop 定义。

> "现在它又升了一个台阶，进入了下一波抽象——我不再手动给 Claude 写 Prompt 了。我运行 Loop，由 Loop 来给 Claude 写 Prompt，决定做什么。我的工作是写 Loop。"
> ——Boris Cherny，WorkOS Acquired Unplugged，2026 年 6 月 2 日

大白话版本：Loop 是一个你写的小程序，它替你给编程 Agent 写 Prompt，读取它产出的内容，判断是否完成，没完成就再给一次。你不再是被困在 Loop 里面敲 Prompt 的人。你成了 Loop 的作者。模型变成了子程序。

Boris 把它讲成三个阶段。一年前他手写代码加自动补全。然后同时跑 5 到 10 个 Claude 会话，逐个给每个写 Prompt。现在他完全不写 Prompt 了——他写那些给 Claude 写 Prompt 的 Loop，几百个 Agent 读他的 GitHub、Slack 和 Twitter，决定接下来构建什么。

> "过去 30 天里，我对 Claude Code 的所有贡献，100% 由 Claude Code 自己写的。我提交了 259 个 PR。"
> ——Boris Cherny，via Simon Willison，2025 年 12 月 27 日

他在 11 月删掉了自己的 IDE，再也没有打开过。

## 从 ReAct 到编排：Loop 的进化阶梯

评论区之所以混乱，是因为 Loop 至少隐藏着五种不同的东西。

**第一阶段**是学术界的 while 循环。2022 年的 ReAct 论文将其形式化：模型推理、调用工具、读取结果、重复直到完成。一个模型，一个 Loop，一个人在旁边看着。

**第二阶段**是 2023 年的 AutoGPT——给它一个目标，让它自己给自己写 Prompt。结果因永远空转而出了名。这次失败播下了长达数年的"Agent 是玩具"的种子。

**第三阶段**是 Trash Panda 说的"过时了"的东西：ralph loop，由 Geoffrey Huntley 在 2025 年 7 月发布。它简单得近乎侮辱人——一个 bash 单行命令，一遍又一遍地把同一个 Prompt 文件传给 Agent。它真正的创新是纪律：每次迭代把上下文重置为一组固定的锚点文件，而不是让对话无限增长。Huntley 用它构建了一整套编程语言，花了大约 297 美元。

**第四阶段**把它产品化了。2026 年春天，Codex 和 Claude Code 都推出了 /goal 命令，运行 ralph loop 直到一个小型验证器模型确认任务完成。

**第五阶段**是 Boris 和 Steinberger 真正指的东西。四个变化发生了：Loop 变成了工作单位，不再是任务。Loop 开始监督其他 Loop，并发运行、按计划调度。调度取代了人工触发。持久性变得显性化——有 git 支持的状态和崩溃恢复。

## 不过是戴了帽子的 cron job

> "Cronjob 最近的品牌升级真有趣。"
> ——X 回复，Loop 讨论，2026 年 6 月

是的，调度层就是 cron。Boris 真的就是用 cron 跑的。Claude Code 的 /loop 命令底层就是 cron。

但 cron 从来没有的是中间那部分。cron job 跑一个固定脚本。Loop 跑的是一个模型——它会查看当前状态，决定下一步做什么，做了之后检查是否有效，然后决定是否继续。决策是 Agent 做的，不是你的，也不是硬编码的分支判断。

**Loop 是 cron 加上一个长在身体里的决策者。** 有趣的工程问题，全在于你围绕那个决策者包了多少东西，让它不会跑偏。

## 真正上手建一个 Loop

Claude Code 推出了 /loop，Boris 自己的例子是标准入门模板：

```
/loop babysit all my PRs. Auto-fix build issues, and when comments come in, use a worktree agent to fix them.
```

Boris 发了五条建议，关于让 Opus 自主运行数小时甚至数天：

1. 用 auto mode 设置权限，这样 Claude 不需要每次都来审批
2. 用 dynamic workflows 让 Claude 编排成百上千个 Agent 来完成任务
3. 用 /goal 或 /loop 推动 Claude 一直跑直到完成
4. 把 Claude Code 放在云端，这样你可以关上电脑
5. 确保 Claude 有办法端到端地自我验证它的产出

第五条是炒作者跳过而实践者死磕的：一个 Loop 的可信度，完全取决于它检查自己工作的能力。

## 反转：Loop 成了最贵的部分

> "今年我发布的每个 AI Agent 就是一个 for 循环、一次 LLM 调用、加一个 try/catch 包着 JSON 解析。唯一有 Agent 味道的，就是月底的 Anthropic 账单。"
> ——@rohit_jsfreaky，2026 年 6 月

Uber 在四个月烧完全年 AI 预算后，给工程师设了每人每工具每月 1500 美元的 Claude Code 和 Cursor 上限。

> "AI 编程中最贵的东西不再是写代码，而是管理 Agent Loop。"
> ——@runes_leo，2026 年 6 月

所有在生产环境中的人最怕的失败模式，是停不下来的 Loop。每一份认真的 2026 年 Loop 文章都收敛到同样的三个硬性停止条件：**最大迭代次数、无进展检测、token 或美元预算上限。**

## 不是 Loop，是 Skill

Loop 是管道。资产是它调用的 Skill。

Steinberger 的另一个反复出现的观点：如果你做某件事超过一次，就把它变成一个自动化 Skill；如果你做了一件很难的事，事后也把它变成 Skill，下次就免费了。

一个里面没有可复用 Skill 的 Loop，只是一个 while true 套着一个陌生人。一个调用了一组经过测试、有名字的 Skill 的 Loop，是一个会复利增长的系统。

## 研究中发现的关键模式

- Loop 是 cron 加上一个长在身体里的决策者：模型在每个循环选择下一步动作
- 血统是真的：2022 年 ReAct、2023 年 AutoGPT、2025 年 ralph、2026 年春天 /goal、现在的编排 Loop
- Loop 的好坏取决于它的反馈。持续的审查和验证门控才是让 Loop 可信的原因
- 最贵的资源从 token 转移到了 Loop 管理
- Loop 里面可复用的单位是 Skill，不是 Prompt
