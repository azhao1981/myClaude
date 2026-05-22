---
name: GoF-OOP
description: |
  GoF 设计模式与 OOP 原则判断专家。当用户在做代码设计、讨论架构方案、考虑是否该用某种模式时触发，尤其当：需要决定是否引入抽象/接口、变量名带宿主技术前缀、存在类职责边界困惑、考虑用模式但不确定是否过度。不要在用户学概念/写简单函数/调试bug时触发。
---

# Skill: GoF-OOP 设计判断专家

> 这个 Skill 不教模型它已知的 SOLID/设计模式，而是注入它不知道的判断边界

## Step 0: 评测集（路由边界）

### 正例（该加载）

- "帮我把这个 2000 行的 order.js 重构成领域分层"
- "mfcOrders 这个类太臃肿了，怎么拆"
- "这段代码混杂了订单、支付、库存，怎么分层"
- "有个万能类把订单、用户、库存全写一起了"

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

Load when 用户想把臃肿的、混杂业务概念的代码重构成领域分层架构，且满足：
- 代码量超过 300 行
- 涉及 3+ 个业务实体
- 变量名包含宿主前缀

Not when 用户在问概念、写简单函数、做 API、调试 bug。

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

### 2.3 过度设计陷阱

| 看起来需要 | 实际不需要 | 原因 |
|------------|------------|------|
| 策略模式 | if-else | 只有一个实现时过度 |
| 工厂模式 | 直接 new | 只会用到一次 |
| 抽象接口 | 具体类 | 没有替换需求 |

**原则**：先有第二次使用的需求，再抽象。不是预支复杂性。

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

- [ ] 正例：混杂代码 → 给出领域分层方案
- [ ] 负例：解释 SOLID → 拒绝执行，引导到另一个 Skill
- [ ] 输出是意图级指导，不是命令级步骤
- [ ] 给出了具体命名建议，不只是说"不要用前缀"
- [ ] 包含坑点警告，不只是正确做法
