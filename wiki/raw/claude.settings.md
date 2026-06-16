---
source_url: https://code.claude.com/docs/en/settings
ingested: 2026-06-16
sha256: 7e984c6da1f726ba2e52bdea60707770c8d64c676679e364086821e3b5b3a499
---

# Claude Code Settings 层级与 `--settings` 行为

> 来源:[code.claude.com/settings](https://code.claude.com/docs/en/settings)、[code.claude.com/permissions](https://code.claude.com/docs/en/permissions)、[code.claude.com/cli-reference](https://code.claude.com/docs/en/cli-reference)
> 适用版本:Claude Code v2.1.x(2026-06)

## 1. 四层 Scope

| Scope | 路径 | 谁生效 | 是否入库 |
|---|---|---|---|
| **Managed** | 系统级 `managed-settings.json`、plist/registry、Server-managed | 机器所有用户 | IT 部署 |
| **User** | `~/.claude/settings.json` | 你,跨所有项目 | 否 |
| **Project** | `<cwd>/.claude/settings.json` | 项目所有协作者 | 是 |
| **Local** | `<cwd>/.claude/settings.local.json` | 你,仅本仓库 | 否(`.gitignore`) |

## 2. 优先级(从高到低)

```
1. Managed             ← 最高,不可被任何来源覆盖
2. Command line        ← --settings / --setting-sources
3. Local               ← .claude/settings.local.json
4. Project             ← .claude/settings.json
5. User                ← ~/.claude/settings.json
```

合并规则:**同一 key 出现在多层时,高层覆盖低层**;key 只在低层出现就直接继承。Managed 永远赢。

例外:`permissions.allow/deny/ask` 是**跨层累加**而不是覆盖(详见 [permissions 文档](https://code.claude.com/docs/en/permissions#settings-precedence))。

## 3. `--settings` 行为

```bash
claude --settings /path/to/foo.json
```

**不是替代,是合并**:

- `foo.json` 落在 **Command line 层**(第 2 优先级)
- 比 `~/.claude/settings.json` 高,比 `~/.claude/settings.json` + `.claude/settings.json` + `.claude/settings.local.json` 三层加起来**低**
- `foo.json` 没写的 key → 从 `~/.claude/settings.json` 继承
- 同 key 在 `.claude/settings.json` / `.claude/settings.local.json` 里**会反过来盖掉 foo.json**

### 反直觉示例

```
~/.claude/settings.json     : { "model": "sonnet", "theme": "dark" }
~/alt.json                  : { "model": "opus" }
./.claude/settings.json     : { "model": "haiku" }
```

执行 `claude --settings ~/alt.json`:

| key | 最终值 | 来源 |
|---|---|---|
| `theme` | `dark` | `~/.claude/settings.json`(继承) |
| `model` | `haiku` | `.claude/settings.json`(项目级赢 CLI) |

→ `--settings` 里的 `opus` 被项目级 `haiku` 反杀。

## 4. 真正"替代"的两种办法

### 4.1 `--setting-sources` 限定加载范围(推荐)

```bash
# 只用 user + 临时文件,跳过 project / local
claude --setting-sources user --settings ~/alt.json

# 只用 project,跳过 user / local
claude --setting-sources project --settings ~/alt.json

# 只用临时文件 + local(忽略 user 和 project)
claude --setting-sources local --settings ~/alt.json
```

可选值:`user`、`project`、`local`,逗号分隔。**配合 `--settings` 才能精确控制合并范围**,避免被项目级配置反噬。

### 4.2 在 alt.json 里"清空"字段

多数 key 不支持 `null`,通用性差,不推荐。

## 5. 常见误用对照

| 你想要的 | 推荐做法 |
|---|---|
| 临时跑一套配置,自动和现有 settings 合并 | `claude --settings ~/alt.json` |
| 临时跑一套配置,**完全替代**现有 settings | `claude --setting-sources user --settings ~/alt.json` |
| 个人在本仓库的微调,不入库 | 编辑 `.claude/settings.local.json`(已自动 gitignore) |
| 跨项目统一个人偏好 | 编辑 `~/.claude/settings.json` |
| 团队共享的权限/MCP/hooks | 编辑 `.claude/settings.json` 并提交 |
| 组织级强制策略 | 走 Managed(`managed-settings.json` / MDM) |

## 6. 改动生效时机

Claude Code 监听 settings 文件变化并自动重载,**大多数 key 不需要重启**(`permissions`、`hooks`、`apiKeyHelper` 等)。只有这两个 key 需要重启:

- `model`(用 `/model` 命令热切换)
- `outputStyle`(`/clear` 或重启)

## 7. 配置校验

```bash
claude doctor
```

会列出每条非法配置项及来源。Managed 设置采用宽容解析(剥离非法条目、保留合法部分),User/Project/Local 是**严格解析**(整文件拒绝)。这意味着在推到生产前,先在本地用 `claude doctor` 验证一遍。

## 8. 相关 CLI Flags

| Flag | 作用 |
|---|---|
| `--settings <path>` | 注入一个 settings 文件到 Command line 层 |
| `--setting-sources user,project,local` | 控制从哪些 scope 加载配置 |

## 9. 引用

- [Settings 官方文档](https://code.claude.com/docs/en/settings)
- [Settings precedence (permissions)](https://code.claude.com/docs/en/permissions#settings-precedence)
- [CLI Reference](https://code.claude.com/docs/en/cli-reference)
- [Debug your configuration](https://code.claude.com/docs/en/debug-your-config)
