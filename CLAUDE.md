# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是 Claude Code 的个人配置仓库，用于管理自定义 Skills（技能）和插件。

### 核心命令

#### 环境设置
```bash
# 创建技能软链接到 Claude 配置目录
./links.sh

# 更新子模块（Skills 和 Plugins）
git submodule update --init --recursive
git submodule update --remote
```

#### Skills 管理
- Skills 存储位置：`skills/` 目录
- 安装目标：`~/.claude/skills/`
- 可用 Skills 见下文"内置 Skills"部分

#### 子模块
- `anthropics/skills` - 官方 Skills 仓库
- `anthropics/claude-plugins-official` - 官方插件市场
- `ref/planning-with-files` - Manus 风格的文件规划系统
- `ref/wshobson/agents` - 社区 Agents 集合

## 内置 Skills

本项目定义了以下自定义 Skills，在执行相应任务时会自动应用：

| Skill | 触发条件 | 核心职责 |
|-------|---------|---------|
| `technical-analysis` | 用户说"分析"、方案设计 | 五层技术分析，含 Mermaid 架构图、数据演进、决策矩阵 |
| `code-review` | "Review"、"审查"代码/文档 | 代码/文档质量审查，KISS 原则检查 |
| `coding-style` | 写代码/修改/重构 | 极简主义编码，禁止过度注释，最小 Git Diff |
| `tdd-workflow` | 新功能/TDD 开发 | 全真业务 TDD，禁 Mock，零后门操作 |
| `precision-test` | "test it"、"verify fix" | 精准单测试运行，禁全量测试 |
| `python-expert` | Python 编码任务 | Service Layer 架构，装饰器日志，KISS 风格 |
| `fastapi-expert` | FastAPI 项目 | 分层架构 (Controller-Service-Repository)，DTO 转换 |
| `prompt-design` | "写Prompt"、"优化提示词" | KV Cache 优化，静态前动态后结构 |
| `15-factor-assessor` | 架构评审、云原生评估 | 15-Factor App 标准，配置管理检查 |
| `smart-lsp` | 代码导航、符号搜索 | LSP 工具优先，命令行工具降级 |
| `define-tech-spec` | 技术文档编写 | 生成内部技术规格，纯工程内容 |

## 技能路由规则

根据任务类型自动选择 Skill：
- **分析/决策/方案** → `technical-analysis`
- **审查代码/文档** → `code-review`
- **写代码/修改/重构** → `coding-style`
- **新功能/测试/TDD** → `tdd-workflow`
- **Dify/Prompt 设计** → `prompt-design`

## 核心约束

1. **反臆造**：除非用户明确要求，否则禁止提供工期估算
2. **环境圣像化**：测试即生产，严禁破坏性操作
3. **Migration 禁令**：严禁直接运行数据库 Migration
4. **极简主义**：KISS 原则，数据结构优于代码逻辑
5. **零过度注释**：代码自解释，禁止解释"What"的注释

## 配置文件

- `main/CLAUDE.md` - 全局系统上下文（用户私有规则）
- `.claude/settings.local.json` - Claude Code 本地配置（API、权限）
- `settings/permissions.json` - 权限配置模板

## 参考

- 官方文档：https://code.claude.com/docs/en/skills
- 中文 Skills 汇总：https://dx72dwmn5vc.feishu.cn/wiki/NLUbwM4S2iGZIUkmo8BcN53Qnhf
