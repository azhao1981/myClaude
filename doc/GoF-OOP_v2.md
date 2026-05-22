# Skill: 领域分层重构判断专家

> 核心原则：这个 Skill 不教模型它已知的 SOLID/设计模式，而是注入它不知道的判断边界

---

## Step 0: 评测集（路由边界定义）

### 正例（该加载）

- "帮我把这个 2000 行的 order.js 重构成领域分层"
- "mfcOrders 这个类太臃肿了，怎么拆"
- "这段代码混杂了订单、支付、库存，怎么分层"
- "有个万能类把订单、用户、库存全写一起了，怎么拆"

### 负例（不该加载）

| 请求 | 为什么不该加载 |
|------|----------------|
| "给我解释一下 SOLID 原则" | 这是教学 Skill 的活，不是重构 |
| "帮我写一个简单的加减法函数" | 不需要领域分层 |
| "代码报错帮我看看" | 这是调试 Skill 的活 |
| "帮我做个 REST API" | 这是基础设施 Skill 的活 |
| "解释一下策略模式和工厂模式的区别" | 这是学习理解，不是重构任务 |

### 临近混淆（容易误判）

| 请求 | 实际应该 |
|------|----------|
| "帮我把代码模块化一下" | 太模糊，需要追问具体场景 |
| "帮我提取几个函数" | 可能是简单抽取，不是领域重构 |
| "这段 Java 代码太乱了" | 没说清楚是领域问题还是风格问题 |

---

## Step 1: 描述

**Load when** 用户想把臃肿的、混杂业务概念的代码重构成领域分层架构，且满足以下任一条件：
- 代码量超过 300 行
- 涉及 3+ 个业务实体
- 变量名包含 `mfc`/`sql`/`http` 等宿主前缀

**Not when** 用户在问概念（SOLID、设计模式）、写简单函数、做 API、调试 bug。

---

## Step 2: 正文（意图级指导 + 坑点）

### 2.1 什么时候该拆（领域判断）

| 信号 | 判断 |
|------|------|
| 函数超过 500 行 | 考虑拆 |
| 变量名带 `mfc`/`sql`/`http` | 必须拆 |
| 一个函数涉及 3+ 个业务概念 | 必须拆 |
| 不到 100 行且不常改动 | 暂时不拆 |
| 只在一个地方用到 | 暂时不拆 |

### 2.2 领域命名红线（工程判断）

```markdown
❌ 绝对禁止（让核心业务"认识"了底层系统）:
   mfcOrder, mfcOrders, mfcOrderProcessor
   sqlUser, sqlUserRepository
   httpClient, apiManager
   restOrderGateway, jdbcTemplate

✅ 正确（核心层对"谁调用它"保持隐形）:
   Order, OrderProcessor
   User, IUserRepository
   OrderGateway
```

**为什么**：如果 `Order` 知道自己是 `mfc` 的，那核心业务就绑死在这个系统上了。

### 2.3 过度设计陷阱（失败经验）

| 看起来需要 | 实际不需要 | 原因 |
|------------|------------|------|
| 策略模式 | if-else | 只有一个实现时会过度 |
| 工厂模式 | 直接 new | 只会用到一次 |
| 抽象接口 | 具体类 | 没有替换需求 |
| 领域事件 | 直接调用 | 还没有复杂的业务流程 |

**原则**：先有第二次使用的需求，再抽象。不是预支复杂性。

### 2.4 领域层 vs 基础设施层边界

```markdown
┌─────────────────────────────────────┐
│         Domain Layer                │
│   （禁止出现技术栈名词）             │
│                                     │
│   interface OrderRepository { ... } │
│   class Order { ... }               │
│   interface IOrderProcessor { ... } │
└─────────────────────────────────────┘
                  ↓ 依赖注入
┌─────────────────────────────────────┐
│      Infrastructure Layer          │
│   （才允许具体系统名称）             │
│                                     │
│   class MfcOrderRepository          │
│       implements OrderRepository    │
│   class MfcOrderProcessor           │
│       implements IOrderProcessor   │
│   class HttpInventoryGateway { ... }│
└─────────────────────────────────────┘
```

### 2.5 重构常见失败案例

**失败模式 1：空壳领域层**
```markdown
// 看起来分了层，实际上没分
class Order {           // Domain
    private MfcOrderData data;  // 泄漏了！
}
```
→ 检查：领域层绝对不能直接持有具体系统的数据结构

**失败模式 2：上帝接口**
```markdown
// 一个接口干所有事
interface IOrderService {
    void create();
    void cancel();
    void pay();
    void refund();
    void ship();
    void deliver();
}
```
→ 拆成小接口：IOrderCreator, IOrderCanceller, IPaymentService...

**失败模式 3：循环依赖**
```
Domain ←→ Infrastructure  // 灾难
```
→ 依赖方向只能是从 Infrastructure 指向 Domain

---

## Step 3: 目录层级

```
skill/
├── scripts/
│   └── check_prefix.sh     # 检测代码中是否有 mfc/sql/http 前缀
├── references/
│   └── anti-patterns.md   # 过度设计案例集（按需加载）
└── skill.md                # 主文件保持轻量
```

### scripts/check_prefix.sh 示例

```bash
#!/bin/bash
# 检查文件中是否有宿主前缀
grep -E "(mfc|sql|http|rest|jdbc|api)" "$1" || echo "Clean: no host prefixes found"
```

### references/anti-patterns.md 目录

| 文件 | 内容 | 加载时机 |
|------|------|----------|
| `anti-patterns.md` | 过度设计案例集 | 当模型问"这个场景需要设计模式吗"时 |
| `refactoring-failures.md` | 常见重构失败案例 | 当重构结果看起来太复杂时 |

---

## Step 4: 验证清单（发布前必须检查）

### 功能验证
- [ ] 正例测试：混杂业务代码 → 模型给出领域分层方案
- [ ] 负例测试：解释 SOLID → 模型拒绝执行，提示找另一个 Skill

### 质量验证
- [ ] 输出是否包含意图级指导而非命令级步骤
- [ ] 是否给出了具体的领域命名建议（而非只说"不要用前缀"）
- [ ] 是否包含坑点警告（而非只有正确做法）

### 边界验证
- [ ] 描述中的小词改动是否影响路由
- [ ] 相邻 Skill（SOLID 教学、设计模式教学）是否会产生误触发

---

## Step 5: 与其他 Skill 的边界协议

| 相邻 Skill | 本 Skill 的边界 |
|------------|----------------|
| SOLID 教学 | SOLID 教学管"是什么"，本 Skill 管"什么时候用/怎么重构" |
| 设计模式 | 设计模式管"有哪些模式"，本 Skill 管"什么时候不要模式" |
| 代码审查 | 代码审查管"问题在哪"，本 Skill 管"怎么重构解决" |
| 简单重构 | 简单重构（提取函数）不需要本 Skill |

---

## 总结：上下文税判断

```markdown
这个 Skill 值得交税吗？

交税项：
- 领域判断规则（什么时候拆）
- 命名红线（mfc/sql/http 禁止模式）
- 过度设计陷阱（什么时候不拆）
- 失败案例（空壳领域层、上帝接口、循环依赖）

模型已知（写了浪费）：
- SOLID 五个原则是什么
- 策略/工厂/装饰器模式怎么用
- 重构的基本概念

结论：注入模型不知道的判断边界，而非教它已知的知识
```
