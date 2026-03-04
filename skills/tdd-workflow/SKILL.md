---
name: tdd-workflow
description: 全真业务 TDD 工作流。Outside-In 驱动，从最外层 HTTP Controller 开始写测试，渐进式一次一个用例，内部实现由失败测试驱动产生。适用于：新功能开发、测试驱动开发、TDD、写测试、测试用例、补测试、加测试、test、test case、test it、verify fix。
---

# Skill: Real-World TDD Workflow (全真业务 TDD)

## 身份与核心哲学 (Identity & Philosophy)

你正在执行 **”全真业务 TDD 工作流”**。
本流程采用 **Outside-In** 策略：从最外层 HTTP Controller 开始写测试，内部细节由失败测试驱动产生。

**核心哲学:**

1. **Outside-In (由外向内)**: 第一个测试必须从**最外层 HTTP Controller**（即接收 HTTP 请求的 endpoint）开始。注意：这里的"API"**专指 HTTP Controller 层**，而非 Service 层方法或内部模块间调用。内部的 Service、Repository 等实现细节，只在测试报错时才去编写。禁止跳过 Controller 直接测内部实现。
2. **报错即导航 (Error Driven)**: 报错是未完成的需求。阅读日志来决定下一步动作。
3. **内部依赖走真实链路，外部依赖用 Mock**:
   - **内部依赖**（自有 DB/Redis/MQ）：必须贯通真实链路，严禁 Mock。
   - **外部依赖**（第三方 API、支付网关、短信服务、邮件服务等不可控的外部系统）：**必须 Mock/Stub**，因为它们不可控、可能产生真实费用、会导致测试不稳定。
4. **零后门操作 (No Backdoor Access)**: 测试代码**严禁**直接执行 SQL (DELETE/UPDATE/INSERT) 来准备或清理数据。所有数据变更必须通过**业务功能代码**完成。
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

**渐进式节奏（铁律）**：
- **一次只写一个测试用例**：可以先用注释列出所有想写的测试用例作为计划，但**每次只实现一个**。
- **一次只运行一个测试用例**：运行测试时，**必须精确指定到单个测试函数/方法**，禁止运行整个测试文件或测试套件。这确保你能精准定位失败原因。
- **通过后再写下一个**：当前测试绿灯后，才能开始写下一个测试用例。

**Outside-In 优先级**（严格按此顺序选择测试入口）：

1. **最优先**: HTTP Controller endpoint — 如果功能有 HTTP 入口，第一个测试**必须**通过 HTTP 请求调用 Controller。**注意**：这里指的是真正的 HTTP 请求（如 `TestClient.post("/api/users")`），不是直接调用 Service 层方法。
2. **次选**: Service 层公开方法 — **仅当**功能完全没有 HTTP 入口时（如内部定时任务、事件处理器、CLI 命令）。
3. **禁止**: 直接测试 Repository/DAO/私有方法 — 这些细节应由外层测试的失败来驱动产生。

* **动作**: 通过 HTTP 请求调用 Controller endpoint（最优先），或调用 Service 公开方法（次选）。
* **断言**: 检查业务副作用。
  * *允许*: 使用只读 SQL (`SELECT`) 来验证数据是否落库（仅用于断言）。
  * *推荐*: 如果有查询接口，优先调用查询接口来断言。
* **外部依赖**: 对第三方 API/服务使用 Mock/Stub，确保测试可重复、无副作用。
* **执行**: 运行**单个测试用例**（精确到测试函数名），禁止运行整个文件。

### 第三步：错误导航 (The Navigation)

**立即分析报错日志**，根据错误类型决定下一步：

#### 🔴 分支 A：基础设施阻断 (STOP)

* **信号**: `ConnectionRefused`, `Timeout`, `AuthError` (以及 Go/Node/Java 等对应的连接错误)。
* **指令**:
1. **立即停止**。
2. 向用户报告：”⚠️ **环境阻断**: 无法连接到真实依赖。”

#### 🟠 分支 B：Schema/结构 缺失 (Migration Required)

* **信号**: `TableNotFound`, `Column not found`, `Schema error`, `Relation does not exist`.
* **指令**:
1. **停止并请求**: 告诉用户“数据库 Schema 不匹配（缺表或缺字段）”。
2. **动作**: 询问用户是否需要生成 Migration 文件，或由用户手动变更数据库。
3. **严禁**: 在测试代码里写 `CREATE TABLE`。

#### 🟢 分支 C：业务逻辑缺失 (Code Required)

* **信号**: `AssertionError`, `Not Implemented`, `404 Not Found`.
* **指令**: 去项目业务代码目录编写实现。

### 第四步：绿灯 (Green)

再次运行**同一个测试用例**，确认通过。

* **清理规则**:
  * **首选**: 依赖数据库事务回滚 (Transaction Rollback) 机制（如果测试框架支持）。
  * **次选**: 调用**业务代码**的删除接口（例如 `UserService.Delete(uid)`）。
  * **最后手段**: 如果没有业务删除功能，**就让数据留在那里**（因为它是 UUID 隔离的，不影响别人）。

### 第五步：重构 (Refactor)

测试绿灯后，**在测试保护下**重构刚写的实现代码：

* 消除重复、改善命名、简化逻辑。
* 每次重构后立即运行**同一个测试用例**，确保仍然绿灯。
* **禁止**在重构阶段添加新功能或新测试。

### 循环

**回到第二步**，从计划列表中选取下一个测试用例，重复 Red → Green → Refactor 循环，直到所有用例完成。

## 铁律 (The Iron Laws)

1. **Outside-In 不可违**: 第一个测试必须从 **HTTP Controller endpoint** 开始，内部实现由失败测试驱动。
2. **内部真实，外部隔离**: 自有基础设施走真实链路；第三方外部服务必须 Mock。
3. **测试无特权**: 测试代码禁止直接执行 DML（DELETE/UPDATE/INSERT）或 DDL（CREATE/DROP），包括 setUp/tearDown 钩子中。
4. **遇阻即停**: 环境连接问题或 Schema 变更需求，必须停下来与用户交互。
5. **逐个击破**: 一次只写一个测试，只运行一个测试，通过后再写下一个。
6. **Red-Green-Refactor**: 每个测试用例必须走完完整的三步循环，不可跳过 Refactor。
