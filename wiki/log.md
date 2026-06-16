# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete

## [2026-06-15] create | Wiki initialized
- Domain: AI 编程智能体工程化
- Structure created with SCHEMA.md, index.md, log.md
- Tag taxonomy defined: loop-engineering, prompt-engineering, agent-orchestration, skill, sub-agent, worktree, memory, automation, connector, mcp, etc.

## [2026-06-15] ingest | 三篇 Loop Engineering 微信公众号文章批量入库
- Sources:
  - `raw/articles/loop-wtf-is-a-loop-2026.md` — 【译】别再手动写 Prompt 了，去写 Loop
  - `raw/articles/loop-fable5-strictest-father-2026.md` — 一文读懂什么是 Loop，Claude Fable 5 是 Loop 最严厉的父亲
  - `raw/articles/loop-engineering-new-paradigm-2026.md` — 一文看懂 AI 编程智能体工程化新范式：Loop Engineering
- Wiki pages created (14):
  - `concepts/loop-engineering.md` — 核心概念页，综合三篇
  - `concepts/skill.md` — Skill 概念（可复用单位）
  - `concepts/sub-agent.md` — 子 Agent 概念（执行与验证分离）
  - `concepts/automation.md` — 自动化调度（循环的心跳）
  - `concepts/worktree.md` — 工作树隔离（并行隔离层）
  - `concepts/connector.md` — 连接器（接入真实工具链）
  - `concepts/mcp.md` — MCP 协议（Connector 底层协议）
  - `concepts/ralph-loop.md` — Ralph Loop（进化阶梯第三阶段）
  - `comparisons/prompt-vs-loop-engineering.md` — 范式对比
  - `comparisons/claude-code-vs-codex.md` — 工具对比
  - `entities/boris-cherny.md` — Claude Code 创建者
  - `entities/peter-steinberger.md` — 推文引爆讨论
  - `entities/claude-code.md` — Anthropic 工具
  - `entities/codex.md` — OpenAI 工具
- Forward link remaining: [[loop-evolution-timeline]]（仅 1 处引用，待未来 ingest 填充）

## [2026-06-16] ingest | Claude Code Settings 层级与合并规则
- Source: `raw/claude.settings.md`（首份位于 `raw/` 根目录、非 `raw/articles/` 的来源；官方文档整理稿）
- 新增 wiki 页（1）:
  - `concepts/claude-code-settings.md` — 四层 Scope（Managed/User/Project/Local）+ 优先级 + `--settings` 合并陷阱 + `--setting-sources` 真正替代法
- 反向链补强：[[claude-code]] 与 [[boris-cherny]] 的"相关页面"区加入 [[claude-code-settings]] 链接
- Index 页数：14 → 15

## [2026-06-16] ingest | OpenRouter Fusion 与多模型审议范式
- Source: `raw/Fusion.md`（文件名大写 F，按上游惯例保留；非 `raw/articles/` 来源，官方文档分析整理稿）
- 源文件含可观察的成本/延迟数字，但部分数字（面板上限 8、延迟倍数）属社区推断，已在两页 frontmatter 标 `contested: true`、`confidence: medium`
- 新增 wiki 页（2）:
  - `entities/openrouter-fusion.md` — 产品实体（OpenRouter 平台 / Fusion / 三入口 / 五维 JSON / 韧性 / 性能）
  - `concepts/multi-model-deliberation.md` — 范式抽象（Panel/Judge/Outer 三段式；与 [[sub-agent]] 的纵向/横向分工对照；适用与误用）
- 反向链补强：[[sub-agent]] 和 [[loop-engineering]] 的"相关页面"区加入 [[multi-model-deliberation]]
- Index 页数：15 → 17
