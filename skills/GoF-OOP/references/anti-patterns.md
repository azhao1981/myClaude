# 领域重构 Anti-Patterns

## 1. 空壳领域层

```java
// ❌ 错误：领域层直接持有具体系统数据结构
class Order {
    private MfcOrderData data;  // 泄漏了底层系统
}

// ✅ 正确：领域层只持有通用类型
class Order {
    private OrderId id;
    private CustomerId customerId;
    private Money totalAmount;
}
```

## 2. 上帝接口

```java
// ❌ 错误：一个接口干所有事
interface IOrderService {
    void create();
    void cancel();
    void pay();
    void refund();
    void ship();
    void deliver();
    void returnGoods();
}

// ✅ 正确：按职责拆成小接口
interface IOrderCreator { void create(OrderRequest req); }
interface IOrderCanceller { void cancel(OrderId id); }
interface IPaymentService { void pay(OrderId id, Money amount); }
```

## 3. 循环依赖

```
// ❌ 错误
Domain ←→ Infrastructure

// ✅ 正确：依赖只能从 Infra 指向 Domain
Domain ←
         ↖ Infrastructure
```

## 4. 事务脚本模式伪装成领域

```java
// ❌ 错误：看起来用了类，实际还是过程式
class OrderService {
    void createOrder(String userName, String productId, int quantity) {
        // 1000 行的过程代码
    }
}

// ✅ 正确：领域对象有行为和状态
class Order {
    private OrderId id;
    private List<OrderLine> lines;

    void addLine(Product product, int quantity) { ... }
    void confirm() { ... }
    Money calculateTotal() { ... }
}
```

## 5. 贫血领域对象

```java
// ❌ 错误：对象只有 getter/setter
class Order {
    private OrderId id;
    private CustomerId customerId;

    public OrderId getId() { return id; }
    public void setId(OrderId id) { this.id = id; }
    // ... 大量 getter/setter
}

// ✅ 正确：有业务行为
class Order {
    private OrderId id;
    private OrderStatus status;

    void place() { this.status = OrderStatus.PLACED; }
    void cancel() {
        if (this.status == OrderStatus.SHIPPED) {
            throw new IllegalStateException("Cannot cancel shipped order");
        }
        this.status = OrderStatus.CANCELLED;
    }
}
```

## 6. 过度抽象

```java
// ❌ 错误：还没有替代需求就抽象
interface IRepository<T, Id> {
    T findById(Id id);
    List<T> findAll();
    void save(T entity);
    void delete(Id id);
}

// 当只有 MfcOrderRepository 一个实现时，
// 这个抽象是过度设计

// ✅ 正确：先有第二个实现，再抽象
class MfcOrderRepository { ... }
class RestOrderRepository { ... }  // 出现第二个实现

interface IOrderRepository { ... }  // 这时才抽象
```

## 7. 领域层使用基础设施概念

```java
// ❌ 错误：领域层出现技术概念
class Order {
    private Connection dbConnection;
    private HttpRequest httpRequest;
}

// ✅ 正确：领域层只有业务概念
class Order {
    private List<OrderLine> lines;
    private Customer customer;
}
```
