
# Skill: Real-World TDD Workflow (全真业务 TDD)

## 身份与核心哲学 (Identity & Philosophy)

你正在执行 **"全真业务 TDD 工作流"**。
本流程要求测试代码必须模拟真实的“客户端”或“上层调用者”，**严禁越权操作**。

**核心哲学:**

1. **报错即导航 (Error Driven)**: 报错是未完成的需求。阅读日志来决定下一步动作。
2. **严禁 Mock (No Mocks)**: 必须贯通真实业务链路（DB/Redis/API）。
3. **零后门操作 (No Backdoor Access)**: 测试代码**严禁**直接执行 SQL (DELETE/UPDATE/INSERT) 来准备或清理数据。所有数据变更必须通过**业务功能代码**（Service/API）完成。

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


### 第二步：红灯测试 - 确立契约 (The Red Test)

编写一个调用真实业务入口的测试用例。

* **动作**: 调用业务层代码 (Service/API)。
* **断言**: 检查业务副作用。
* *允许*: 使用只读 SQL (`SELECT`) 来验证数据是否落库（这是唯一的例外，仅用于断言）。
* *推荐*: 如果有查询接口，优先调用查询接口来断言。


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

1. **Mock 即谎言**: 严禁 Mock 数据库和基础设施。
2. **测试无特权**: 测试代码也是“用户”。用户不能运行 `DELETE FROM users`，测试代码也不能。
3. **遇阻即停**: 遇到环境连接问题或 Schema 变更需求，必须停下来与人交互，而不是自动执行破坏性操作。
