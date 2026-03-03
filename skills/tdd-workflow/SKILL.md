---
name: tdd-workflow
description: 全真业务 TDD 工作流。Outside-In 驱动，从最外层 API 开始写测试，内部实现由失败测试驱动产生。适用于：新功能开发、测试驱动开发、TDD、写测试、测试用例、补测试、加测试、test、test case、test it、verify fix。
---

# Skill: Real-World TDD Workflow (全真业务 TDD)

## 身份与核心哲学 (Identity & Philosophy)

你正在执行 **”全真业务 TDD 工作流”**。
本流程采用 **Outside-In** 策略：从最外层业务接口开始写测试，内部细节由失败测试驱动产生。

**核心哲学:**

1. **Outside-In (由外向内)**: 第一个测试必须从**最外层业务入口**（API endpoint / Controller）开始。内部的 Service、Repository 等实现细节，只在核心测试报错时才去编写。禁止跳过外层直接测内部实现。
2. **报错即导航 (Error Driven)**: 报错是未完成的需求。阅读日志来决定下一步动作。
3. **内部依赖走真实链路，外部依赖用 Mock**:
   - **内部依赖**（自有 DB/Redis/MQ）：必须贯通真实链路，严禁 Mock。
   - **外部依赖**（第三方 API、支付网关、短信服务、邮件服务等不可控的外部系统）：**必须 Mock/Stub**，因为它们不可控、可能产生真实费用、会导致测试不稳定。
4. **零后门操作 (No Backdoor Access)**: 测试代码**严禁**直接执行 SQL (DELETE/UPDATE/INSERT) 来准备或清理数据。所有数据变更必须通过**业务功能代码**（Service/API）完成。
5. **先验证根因，再修复 (Verify Before Fix)**: 修复失败测试前，必须先追踪实际数据流（数据库查询、日志分析）确认根因，**严禁**通过篡改测试数据来凑通过。

## 输入参数 (Input Parameters)

* `feature_context`: (String) 待实现的业务功能描述。
* `tdd_directory`: (String) TDD 测试文件的存放目录（需与单元测试物理隔离）。

## 执行协议 (Execution Protocol)

### 第一步：隔离与准备 (Setup)

* **创建文件**: 在 `tdd_directory` 下创建新的测试文件。
* **数据策略**:
* **唯一性 (Isolation)**: 必须使用 UUID/Random 生成本次测试独享的数据 Key。
* **视开发即生产 (Dev is Prod)**:
* **绝对禁令**: 测试代码**严禁**执行任何形式的 `DELETE`、`TRUNCATE` 或 `DROP` 语句。
* **理由**: 你无权绕过业务逻辑直接操作数据库。哪怕是清理数据，也必须调用业务提供的 `Delete()` 功能。如果该功能未开发，则**不清理**。


### 第二步：红灯测试 - Outside-In 契约 (The Red Test)

**先列计划，再写单个**：可以先用注释列出所有想写的测试用例，但**一次只能写一个**，避免测试用例膨胀导致难以调试。

**Outside-In 优先级**（严格按此顺序选择测试入口）：

1. **最优先**: API endpoint（HTTP 请求） — 如果功能有 API 入口，第一个测试**必须**从 API 层开始。
2. **次选**: Service 层公开方法 — 仅当功能无 API 入口时（如内部定时任务、事件处理器）。
3. **禁止**: 直接测试 Repository/DAO/私有方法 — 这些细节应由外层测试的失败来驱动产生。

* **动作**: 调用最外层业务入口。
* **断言**: 检查业务副作用。
  * *允许*: 使用只读 SQL (`SELECT`) 来验证数据是否落库（仅用于断言）。
  * *推荐*: 如果有查询接口，优先调用查询接口来断言。
* **外部依赖**: 对第三方 API/服务使用 Mock/Stub，确保测试可重复、无副作用。
* **执行**: 运行项目对应的测试命令。

### 第三步：错误导航 (The Navigation)

**立即分析报错日志**，根据错误类型决定下一步：

#### 🔴 分支 A：基础设施阻断 (STOP)

* **信号**: `ConnectionRefused`, `Timeout`, `AuthError` (以及 Go/Node/Java 等对应的连接错误)。
* **指令**:
1. **立即停止**。
2. 向用户报告：“⚠️ **环境阻断**: 无法连接到真实依赖。”



#### 🟠 分支 B：Schema/结构 缺失 (Migration Required)

* **信号**: `TableNotFound`, `Column not found`, `Schema error`, `Relation does not exist`.
* **指令**:
1. **停止并请求**: 告诉用户“数据库 Schema 不匹配（缺表或缺字段）”。
2. **动作**: 询问用户是否需要生成 Migration 文件，或由用户手动变更数据库。
3. **严禁**: 在测试代码里写 `CREATE TABLE`。



#### 🟢 分支 C：业务逻辑缺失 (Code Required)

* **信号**: `AssertionError`, `Not Implemented`, `404 Not Found`.
* **指令**: 去 `src/` 编写业务代码。

### 第四步：绿灯与清理 (Green & Verification)

再次运行测试。

* **清理规则 (Strict Cleanup)**:
* **首选**: 依赖数据库事务回滚 (Transaction Rollback) 机制（如果测试框架支持）。
* **次选**: 调用**业务代码**的删除接口（例如 `UserService.Delete(uid)`）。
* **最后手段**: 如果没有业务删除功能，**就让数据留在那里**（因为它是 UUID 隔离的，不影响别人）。
* **禁止**: 绝对不要为了清理环境而在 `teardown` 里写 `db.execute("DELETE FROM...")`。


## 铁律 (The Iron Laws)

1. **Outside-In 不可违**: 第一个测试必须从最外层入口开始。内部实现由失败测试驱动，而非提前设计。
2. **内部真实，外部隔离**: 自有基础设施（DB/Redis/MQ）走真实链路；第三方外部服务必须 Mock。
3. **测试无特权**: 测试代码也是"用户"。用户不能运行 `DELETE FROM users`，测试代码也不能。
4. **遇阻即停**: 遇到环境连接问题或 Schema 变更需求，必须停下来与人交互，而不是自动执行破坏性操作。
5. **逐个击破**: 不要一次性写所有测试用例。可以列计划，但**一次只写一个测试**，通过后再写下一个。
6. **Setup/Teardown 禁写**: 禁止在 `setUp`/`tearDown`、`beforeEach`/`afterEach`、`up`/`down` 等钩子中执行写入或删除数据的操作。所有数据变更必须在**测试用例内部**显式完成，确保副作用可追溯。
