---
name: 15-factor-assessor
description: 评估当前项目架构是否符合“15要素应用 (15-Factor App)”的云原生标准，提供改进建议。
version: 1.0.0
---

# 15-Factor App Assessor

## Overview
此 Skill 用于帮助开发者评估其应用架构是否符合云原生开发的 15 个关键要素（基于经典的 12-Factor 扩展）。它可以对代码库进行静态分析，或通过问答形式引导用户检查架构设计。

## When to use
当用户要求进行“架构评审”、“云原生评估”、“检查配置管理”或提到“12要素/15要素”时使用此 Skill。

## Instructions
1.  **初步扫描**：首先检查项目根目录是否存在以下关键文件，以预判架构风格：
    * `Dockerfile` / `Containerfile` (容器化)
    * `.env.example` 或 `config` 目录 (配置管理)
    * `pom.xml`, `package.json`, `go.mod` (依赖管理)
    * `.github/workflows` 或 `.gitlab-ci.yml` (CI/CD)

2.  **评估模式**：
    * 如果用户要求“快速检查”，仅基于当前可见文件提供反馈。
    * 如果用户要求“完整评估”，请逐条通过交互式问答确认 15 个要素的落实情况。

3.  **输出要求**：
    * 对每个要素给出：✅ (达标), ⚠️ (需改进), ❌ (未达标) 或 ❓ (未知)。
    * 对于 ⚠️ 和 ❌，必须给出具体的修改建议（例如：“建议将硬编码的 DB 密码改为环境变量注入”）。

## The 15 Factors (Evaluation Criteria)

### Core 12 Factors (Original)
1.  **Codebase (基准代码)**:
    * 标准：一份代码库，多份部署。
    * 检查：是否在一个 Repo 中管理？是否复用了代码但区分了环境？
2.  **Dependencies (依赖)**:
    * 标准：显式声明依赖关系。
    * 检查：是否存在 `node_modules` 或 `vendor` 提交进 git 的情况？是否使用了 lock 文件？
3.  **Config (配置)**:
    * 标准：**在环境中存储配置**。
    * 检查：**关键！** 是否有硬编码的密码/密钥？是否使用环境变量 (Env Vars) 注入配置？
4.  **Backing services (后端服务)**:
    * 标准：把后端服务当作附加资源。
    * 检查：数据库、缓存是否通过 URL/连接串 访问？是否能在不改代码的情况下切换 Local Redis 和 Cloud Redis？
5.  **Build, release, run (构建，发布，运行)**:
    * 标准：严格分离构建和运行阶段。
    * 检查：是否支持不可变镜像构建？
6.  **Processes (进程)**:
    * 标准：以一个或多个无状态进程运行应用。
    * 检查：应用是否在本地内存中存储 Session 或文件？（如果是，则无法横向扩展）。
7.  **Port binding (端口绑定)**:
    * 标准：通过端口绑定提供服务。
    * 检查：应用是否自带 Web Server (如 Tomcat/Jetty/Gunicorn) 并监听端口，而不是依赖外部 Web 容器注入？
8.  **Concurrency (并发)**:
    * 标准：通过进程模型进行扩展。
    * 检查：是否可以通过增加进程副本数来提高并发能力？
9.  **Disposability (易处理)**:
    * 标准：快速启动和优雅终止。
    * 检查：启动时间是否在秒级？收到 SIGTERM 信号时是否能完成当前任务后安全退出？
10. **Dev/prod parity (环境等价)**:
    * 标准：保持开发、预发布、线上环境尽可能一致。
    * 检查：Dev 环境是否使用了和 Prod 不同的后端服务（如 Dev 用 SQLite，Prod 用 PostgreSQL）？
11. **Logs (日志)**:
    * 标准：把日志当作事件流。
    * 检查：应用是直接写文件（错误），还是输出到 `stdout/stderr`（正确）？
12. **Admin processes (管理进程)**:
    * 标准：后台管理任务当作一次性进程运行。
    * 检查：数据库迁移 (Migration) 是否是独立的脚本或命令？

### The +3 Factors (Beyond 12)
13. **API First (API 优先)**:
    * 标准：在开发前定义服务契约。
    * 检查：是否有 Swagger/OpenAPI 定义？前后端是否基于契约并行开发？
14. **Telemetry (遥测/监控)**:
    * 标准：关注应用内部状态，不仅仅是日志。
    * 检查：是否暴露了 Metrics 端点 (如 `/metrics`, Prometheus)？是否有分布式链路追踪 (Tracing)？
15. **Authentication/Authorization (认证与授权)**:
    * 标准：安全不仅仅是边界网关的事，要在应用层实现。
    * 检查：服务间调用是否包含 Auth Token？是否支持 RBAC？

## Pro Tips for Improvement
* **对于配置**：推荐使用 `dotenv` 库在开发环境模拟环境变量。
* **对于日志**：推荐使用结构化日志 (JSON format) 以便日志系统通过 ELK/Splunk 分析。
* **对于遥测**：推荐集成 OpenTelemetry。