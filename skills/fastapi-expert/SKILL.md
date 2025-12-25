---
name: fastapi-expert
description: 专门用于 FastAPI 项目的架构设计、代码审查和开发规范指导。基于 fastapi-best-practices 权威指南。
---

# FastAPI 专家技能 (Skill)

当你识别到当前项目是 FastAPI 应用，或者用户要求进行 FastAPI 相关开发时，请激活此技能并遵循以下准则。

## 1. 核心操作模式
- **优先查阅**：在提供代码建议前，请查阅本地参考文档：`references/best-practices-zh.md`。
- **一致性**：所有生成的 API 路由、Pydantic 模型和数据库操作必须符合该参考文档中的“最佳实践”。

## 2. 必须遵守的关键规则 (TL;DR)
如果用户没有特殊要求，默认执行以下规范：
- **异步原则**：除非有明确理由，否则一律使用 `async def` 和异步驱动。
- **依赖注入**：利用 `Depends` 管理 Auth、DB Session 和配置。
- **数据验证**：使用 Pydantic V2，并优先使用 `Annotated` 语法。
- **响应模型**：明确定义 `response_model`，严禁直接返回 ORM 对象。
- **项目结构**：遵循文档中的生产级目录拆分方案（`app/api`, `app/schemas` 等）。

## 3. 任务指令示例
- "根据参考文档中的项目结构，初始化一个新的 FastAPI 目录。"
- "Review 现有的 `main.py`，找出不符合 `best-practices-zh.md` 的地方并修正。"
- "为 `User` 模型创建一个符合最佳实践的 CRUD 逻辑。"

## 4. 冲突处理
如果参考文档与用户现有代码风格冲突，请先指出冲突点，并说明为什么参考文档的做法更具扩展性或安全性，由用户决定是否重构。