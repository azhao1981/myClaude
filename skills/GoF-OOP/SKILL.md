---
name: GoF-OOP
description: |
  GoF 设计模式与 OOP 判断专家。当用户做代码设计、讨论架构、决定是否引入模式时触发，尤其当：变量名带技术前缀、职责边界模糊、不确定是否过度。不要在学概念/写简单函数/调试bug时触发。
---

# Skill: GoF-OOP 设计判断专家

> 这个 Skill 不教模型它已知的 SOLID/设计模式，而是注入它不知道的判断边界

## Step 0: 评测集（路由边界）

### 正例（该加载）

- "我需要为这个订单模块设计接口吗？以后可能要换实现"
- "这个支付流程用策略模式还是状态机好？"
- "什么情况下才值得引入工厂模式？"
- "这种继承层次合理吗，还是用组合更好？"
- "mfcOrders 这个类职责太多了，怎么拆"

### 负例（不该加载）

| 请求 | 原因 |
|------|------|
| "给我解释一下 SOLID 原则" | 教学 Skill 的活 |
| "帮我写一个简单的加减法函数" | 不需要领域分层 |
| "代码报错帮我看看" | 调试 Skill 的活 |
| "帮我做个 REST API" | 基础设施 Skill 的活 |
| "解释策略模式和工厂模式的区别" | 学习理解，不是重构 |

### 临近混淆

| 请求 | 实际应该 |
|------|----------|
| "帮我把代码模块化一下" | 太模糊，追问场景 |
| "帮我提取几个函数" | 可能是简单抽取 |
| "这段 Java 代码太乱了" | 没说清楚是领域问题还是风格问题 |

---

## Step 1: 描述

Load when 用户在做 OOP 设计、考虑是否引入抽象/接口/模式，且满足以下之一：
- 变量名带宿主技术前缀（mfc/sql/http）
- 存在类职责边界模糊
- 考虑用某种模式但不确定是否过度
- 继承/组合结构选择困惑

Not when 用户在学概念、写简单函数、做 API、调试 bug。

---

## Step 2: 正文

### 2.1 什么时候该拆

| 信号 | 判断 |
|------|------|
| 函数超过 500 行 | 考虑拆 |
| 变量名带 `mfc`/`sql`/`http` | 必须拆 |
| 一个函数涉及 3+ 业务概念 | 必须拆 |
| 不到 100 行且不常改动 | 暂时不拆 |
| 只在一处用到 | 暂时不拆 |

### 2.2 领域命名红线

```
❌ 禁止（让核心业务认识底层系统）:
   mfcOrder, mfcOrders, sqlUser, httpClient, restOrderGateway

✅ 正确（核心层对谁调用它保持隐形）:
   Order, User, OrderGateway, IOrderRepository
```

### 2.3 双轨输出（核心输出规范）

当用户询问设计决策时，**必须同时输出两条路径**：

| 路径 | 内容 |
|------|------|
| 模式方案 | 用设计模式/OOP 的完整方案，包含类图、接口定义、调用链 |
| 简单方案 | 函数式/过程式的最小实现，包含函数签名、调用链 |

**然后让用户选择。不要替用户决定"这次不需要模式"。**

**为什么必须双轨**：
- AI 有系统性偏差：默认输出函数式/过程式方案，几乎不会主动设计 OOP 结构。
- 用户调用此 Skill = 明确要求模式思考。"模式方案"是被要求的功能，不是过度设计。
- 单轨输出（只给简单方案）在实践中等于永远不给模式方案，违背了 Skill 的存在意义。
- 这不是"预想的设计"，是"补偿已知偏差"——确保用户能看到完整的决策空间。

### 2.4 领域层 vs 基础设施层

```
Domain Layer（禁止技术栈名词）:
  interface OrderRepository { ... }
  class Order { ... }

Infrastructure Layer（才允许具体系统）:
  class MfcOrderRepository implements OrderRepository { ... }
  class HttpInventoryGateway { ... }
```

### 2.5 重构失败案例

**空壳领域层**：
```java
// 看起来分层了，实际没有
class Order {
    private MfcOrderData data;  // 泄漏了！
}
```

**上帝接口**：
```java
// 一个接口干所有事
interface IOrderService {
    void create(); void cancel(); void pay(); void refund(); void ship();
}
// 应该拆成 IOrderCreator, IOrderCanceller, IPaymentService...
```

**循环依赖**：Domain ←→ Infrastructure 是灾难，依赖方向只能从 Infra 指向 Domain。

---

## Step 3: 脚本和参考

### scripts/check_prefix.sh

```bash
#!/bin/bash
# 检测宿主前缀：mfc/sql/http/rest/jdbc/api
grep -E "(mfc|sql|http|rest|jdbc|api)" "$1" && echo "FOUND: host prefix detected" || echo "CLEAN"
```

### references/anti-patterns.md

当用户问"这个场景需要设计模式吗"时加载。

当重构结果看起来太复杂时加载。

---

## Step 4: 验证清单

- [ ] 正例：设计决策问题 → 给出模式/抽象/边界判断
- [ ] 负例：学概念/简单函数/调试 → 拒绝加载
- [ ] 输出是意图级指导，不是命令级步骤
- [ ] 给出了具体命名建议，不只是说"不要用前缀"
- [ ] 包含坑点警告，不只是正确做法
