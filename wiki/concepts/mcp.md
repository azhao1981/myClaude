---
title: MCP (Model Context Protocol)
created: 2026-06-15
updated: 2026-06-15
type: concept
tags: [mcp, connector, loop-engineering]
sources: [raw/articles/loop-fable5-strictest-father-2026.md, raw/articles/loop-engineering-new-paradigm-2026.md]
confidence: medium
---

# MCP (Model Context Protocol)

## 定义

**MCP** 是 [[connector]] 的底层协议，让 AI 编程智能体接入外部工具和数据源。^[raw/articles/loop-fable5-strictest-father-2026.md]

## 在 Loop Engineering 中的角色

在 [[loop-engineering]] 体系中，MCP 让 Agent 突破文件系统的边界，连接到真实开发环境。^[raw/articles/loop-fable5-strictest-father-2026.md]

- [[codex]] 和 [[claude-code]] 都支持 MCP^[raw/articles/loop-fable5-strictest-father-2026.md]
- 为一个写的 Connector 通常在另一个里也能直接用^[raw/articles/loop-fable5-strictest-father-2026.md]
- Plugin 把基于 MCP 的 Connectors 和 [[skill]] 打包分发^[raw/articles/loop-fable5-strictest-father-2026.md]

## 互操作性

MCP 的最大价值是跨工具兼容——为 Claude Code 开发的 Connector 在 Codex 中通常可直接使用，反之亦然。这降低了生态碎片化风险。

## 相关页面

- [[connector]] — MCP 之上的应用层
- [[loop-engineering]] — MCP 使能的范式
- [[claude-code]] / [[codex]] — 均支持 MCP
