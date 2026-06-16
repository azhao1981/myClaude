---
title: Claude Code Settings 层级与合并规则
created: 2026-06-16
updated: 2026-06-16
type: concept
tags: [claude-code, settings, cli, agent-orchestration]
sources: [raw/claude.settings.md]
confidence: high
---

# Claude Code Settings 层级与合并规则

## 定义

[[claude-code]] 的运行配置由**四层 Scope** 叠加而成，每一层覆盖不同的"谁生效 / 是否入库"语义。命令行上的 `--settings` 与 `--setting-sources` 不是简单的"临时换配置"，而是把临时文件注入到第 2 层（Command line），再按优先级与各层合并——理解这一点是绕开反直觉行为的关键。^[raw/claude.settings.md]

## 四层 Scope

| Scope | 路径 | 谁生效 | 是否入库 |
|---|---|---|---|
| **Managed** | 系统级 `managed-settings.json`、plist/registry、Server-managed | 机器所有用户 | IT 部署 |
| **User** | `~/.claude/settings.json` | 你，跨所有项目 | 否 |
| **Project** | `<cwd>/.claude/settings.json` | 项目所有协作者 | 是 |
| **Local** | `<cwd>/.claude/settings.local.json` | 你，仅本仓库 | 否（`.gitignore`） |

^[raw/claude.settings.md]

## 优先级与合并规则

从高到低：

```
1. Managed             ← 最高，不可被任何来源覆盖
2. Command line        ← --settings / --setting-sources
3. Local               ← .claude/settings.local.json
4. Project             ← .claude/settings.json
5. User                ← ~/.claude/settings.json
```

合并规则：**同一 key 出现在多层时，高层覆盖低层**；key 只在低层出现就直接继承。Managed 永远赢。^[raw/claude.settings.md]

**例外**：`permissions.allow/deny/ask` 是**跨层累加**而不是覆盖——这是为了保证安全策略不会因为高层没写就被悄悄放开。^[raw/claude.settings.md]

## `--settings` 的反直觉之处

```bash
claude --settings /path/to/foo.json
```

`foo.json` 落在 **Command line 层**（第 2 优先级）——它的行为是**合并，不是替代**：

- `foo.json` 没写的 key → 从 `~/.claude/settings.json` 继承
- 但 `foo.json` 里写了的 key，会被**项目级 / local 级反过来盖掉**
- 因此单用 `--settings` 通常达不到"临时换配置"的预期效果^[raw/claude.settings.md]

### 反直觉示例

```
~/.claude/settings.json     : { "model": "sonnet", "theme": "dark" }
~/alt.json                  : { "model": "opus" }
./.claude/settings.json     : { "model": "haiku" }
```

执行 `claude --settings ~/alt.json` 的最终结果：

| key | 最终值 | 来源 |
|---|---|---|
| `theme` | `dark` | `~/.claude/settings.json`（继承） |
| `model` | `haiku` | `.claude/settings.json`（项目级赢 CLI） |

→ `--settings` 里的 `opus` 被项目级 `haiku` 反杀。^[raw/claude.settings.md]

## 真正"替代"的两种办法

### 配合 `--setting-sources` 限定加载范围（推荐）

```bash
# 只用 user + 临时文件，跳过 project / local
claude --setting-sources user --settings ~/alt.json

# 只用 project，跳过 user / local
claude --setting-sources project --settings ~/alt.json

# 只用临时文件 + local（忽略 user 和 project）
claude --setting-sources local --settings ~/alt.json
```

可选值：`user`、`project`、`local`，逗号分隔。**配合 `--settings` 才能精确控制合并范围**，避免被项目级配置反噬。^[raw/claude.settings.md]

### 在 alt.json 里"清空"字段

多数 key 不支持 `null`，通用性差，不推荐。^[raw/claude.settings.md]

## 常见误用对照

| 你想要的 | 推荐做法 |
|---|---|
| 临时跑一套配置，自动和现有 settings 合并 | `claude --settings ~/alt.json` |
| 临时跑一套配置，**完全替代**现有 settings | `claude --setting-sources user --settings ~/alt.json` |
| 个人在本仓库的微调，不入库 | 编辑 `.claude/settings.local.json`（已自动 gitignore） |
| 跨项目统一个人偏好 | 编辑 `~/.claude/settings.json` |
| 团队共享的权限/MCP/hooks | 编辑 `.claude/settings.json` 并提交 |
| 组织级强制策略 | 走 Managed（`managed-settings.json` / MDM） |

^[raw/claude.settings.md]

## 改动生效时机

Claude Code 监听 settings 文件变化并自动重载，**大多数 key 不需要重启**（`permissions`、`hooks`、`apiKeyHelper` 等）。只有这两个 key 需要重启：

- `model`（用 `/model` 命令热切换）
- `outputStyle`（`/clear` 或重启）^[raw/claude.settings.md]

## 配置校验

```bash
claude doctor
```

会列出每条非法配置项及来源。Managed 设置采用宽容解析（剥离非法条目、保留合法部分），User/Project/Local 是**严格解析**（整文件拒绝）。在推到生产前，先在本地用 `claude doctor` 验证一遍。^[raw/claude.settings.md]

## 设计观察

- **Managed 永远赢 + permissions 跨层累加**：这两条规则保证了 IT 部署的安全底线——下层配置不能"绕过"上层策略。这与传统 Unix 的"近处覆盖远处"原则不完全一致。
- **Project 层比 CLI 临时文件优先级还高**：这是反直觉点，但意图明确——团队共享配置不应被个人临时开关轻易推翻。
- **`.local.json` 自动 `.gitignore`**：让"个人临时覆盖"无需污染版本控制，配合 `--setting-sources local` 即可在本仓库做安全实验。

## 相关页面

- [[claude-code]] — Settings 的载体，其六大模块视角
- [[boris-cherny]] — Claude Code 创建者，settings 体系的设计者
- [[automation]] — `hooks`、`/loop` 等均通过 settings 配置并支持热重载
- [[mcp]] — MCP 服务器配置通过 Project 层 settings 共享给团队

## 引用

- [Settings 官方文档](https://code.claude.com/docs/en/settings)
- [Settings precedence (permissions)](https://code.claude.com/docs/en/permissions#settings-precedence)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Debug your configuration](https://code.claude.com/docs/en/debug-your-config)
