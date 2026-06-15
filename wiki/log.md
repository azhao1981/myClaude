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
