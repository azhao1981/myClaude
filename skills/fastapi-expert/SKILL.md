---
name: fastapi-expert
description: FastAPI 项目架构专家。基于 fastapi-best-practices，强制执行 Controller-Service-Repository 分层架构、DTO 转换、业务异常分离。
---

# FastAPI 专家

识别 FastAPI 项目时激活。核心职责：**分层架构强制执行**。

## 快速诊断（第一优先级）

审查代码时，按优先级检查违规：

| 优先级 | 违规模式 | 修正 |
|--------|----------|------|
| 🔴 P0 | Service 含 `db.query()` / `session.execute()` / `select(` | 移至 Repository |
| 🔴 P0 | Service 返回 ORM 对象（非 DTO） | `DTO.model_validate(orm, from_attributes=True)` |
| 🔴 P0 | Service 含 `raise HTTPException` | 改为业务异常 + 全局 handler |
| 🔴 P0 | Repository 含 `db.commit()` | 移至 Service 或 UoW |
| 🟡 P1 | Router 含业务逻辑（条件判断、循环处理） | 移至 Service |
| 🟡 P1 | `def` 路由/依赖（非 `async def`） | 改为 `async def` |
| 🟡 P1 | `Depends(func)` 未使用 `Annotated` | 改为 `Annotated[Type, Depends(func)]` |
| 🟢 P2 | 缺少 `response_model` | 显式声明返回类型 |
| 🟢 P2 | BaseModel 未设 `protected_namespaces=()` | 添加配置 |

## 分层架构

```
HTTP → Controller → Service → Repository → Database
           ↓            ↓           ↓
        请求验证     业务编排     数据访问
        响应转换     DTO转换      CRUD
```

### 职责边界（核心）

| 层 | 允许 | 禁止 |
|----|------|------|
| **Controller** | 参数校验、调用 Service、返回响应 | SQL、业务逻辑、`db.commit()` |
| **Service** | 业务逻辑、DTO↔ORM 转换、事务控制 | SQL 查询、`HTTPException`、HTTP 状态码 |
| **Repository** | `select`/`insert`/`update`/`delete`、`flush()` | `commit()`、业务规则 |
| **Schema (DTO)** | 数据验证、序列化 | 数据库访问、业务逻辑 |

## Annotated 依赖注入（默认模式）

```python
from typing import Annotated
from fastapi import Depends

# 类型别名（推荐定义在 dependencies.py）
DbSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]

# 路由使用
@router.post("/users", response_model=UserResponse)
async def create_user(data: UserCreate, service: UserServiceDep):
    return await service.create(data)
```

## 异常处理模式

```python
# ✅ 正确：业务异常 + 全局 handler
# exceptions.py
class UserNotFoundError(Exception): pass

# service.py
async def get_user(self, user_id: UUID) -> UserResponse:
    user = await self.repo.get_by_id(user_id)
    if not user:
        raise UserNotFoundError(user_id)  # 纯业务异常
    return UserResponse.model_validate(user, from_attributes=True)

# main.py
@app.exception_handler(UserNotFoundError)
async def handle_user_not_found(request: Request, exc: UserNotFoundError):
    return JSONResponse(status_code=404, content={"error": str(exc)})

# ❌ 错误：Service 中直接抛 HTTPException
raise HTTPException(status_code=404, detail="User not found")
```

## Repository 模式

```python
class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.flush()  # ⚠️ flush 而非 commit
        await self.db.refresh(user)
        return user
```

## Unit of Work（多表事务）

```python
class UnitOfWork:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)
        self.orders = OrderRepository(db)

    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, *_):
        if exc_type:
            await self.db.rollback()
        else:
            await self.db.commit()

# 使用
async def transfer(self, from_id: UUID, to_id: UUID, amount: Decimal):
    async with self.uow as uow:
        # 多个 repo 操作在同一事务中
        await uow.accounts.debit(from_id, amount)
        await uow.accounts.credit(to_id, amount)
        # __aexit__ 自动 commit/rollback
```

## Pydantic V2 配置

```python
from pydantic import BaseModel, ConfigDict

class AppBaseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,          # ORM 模式
        protected_namespaces=(),       # 允许 model_ 前缀字段
        str_strip_whitespace=True,     # 自动去空格
    )

# 所有 DTO 继承 AppBaseModel
class UserResponse(AppBaseModel):
    id: UUID
    email: EmailStr
```

## 默认行为

除非用户明确反对：

1. **分层强制**：Service 必须通过 Repository 访问数据
2. **DTO 转换**：Service 层完成 ORM ↔ DTO 转换
3. **异步优先**：路由/依赖默认 `async def`
4. **Annotated 语法**：依赖注入使用 `Annotated[Type, Depends()]`
5. **事务边界**：Repository 只 `flush()`，Service/UoW 控制 `commit()`

## 冲突处理

1. 指出违规位置和违反的规则
2. 说明问题（耦合、难测试、事务泄漏）
3. 提供符合分层架构的重构方案
4. 用户决定是否执行

## 参考文档

详细最佳实践：`references/best-practices-zh.md`
