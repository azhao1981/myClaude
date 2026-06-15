---
title: Connector
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [connector, mcp, loop-engineering]
sources: [raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: high
---

# Connector（连接器）

## 定义

**Connector** 让 [[loop-engineering]] 中的 Agent 从「只能读写本地文件」升级为「参与真实开发流程」。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 解决的问题

一个只能看到文件系统的 Loop，能做的事很有限。真实开发发生在更大的系统里：issue tracker、PR、CI、数据库、监控平台、Slack、Linear、Notion、内部 API。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 能力范围

Connectors 建立在 [[mcp]] 协议之上，让 Agent 能：^[raw/articles/loop-fable5-strictest-father-2026.md]

- 读取 issue tracker
- 查询数据库
- 访问 staging API
- 往 Slack 发消息
- 自动开 PR
- 关联 Linear 票
- CI 绿了自动通知频道

> 这是 Agent 说"这是修复方案"和 Loop 自动开 PR、关联 Linear 票之间的差距。^[raw/articles/loop-fable5-strictest-father-2026.md]

## Plugin 与 Connector 的关系

Plugin 把 Connectors 和 [[skill]] 打包在一起，队友一次安装，不用自己从头重建。为一个工具写的 Connector 通常在另一个里也能直接用。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 权限设计原则

> 工具链连接越深，权限设计越要保守。^[raw/articles/loop-engineering-new-paradigm-2026.md]

需要清晰边界：权限给多大、能不能写生产数据、能不能自动发消息、能不能改 ticket 状态。^[raw/articles/loop-engineering-new-paradigm-2026.md]

## 相关页面

- [[loop-engineering]] — Connector 是其核心构件
- [[mcp]] — Connector 的底层协议
- [[skill]] — 与 Connector 一起打包成 Plugin
