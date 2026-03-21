---
name: python-expert
description: Python 开发终极指南。强制执行：Service Layer 架构、KISS 极简代码风格、以及基于装饰器的全自动结构化日志。
author: You
version: 4.0.0
---

# Python Expert Development Guidelines

当用户进行 Python 编码任务时，必须严格遵守以下流程和规范。

## 0. 环境自检 (Pre-flight Check)
在编写任何业务代码前，先检查当前项目是否存在日志工具。
- **检查路径**：`utils/log_decorator.py` (或类似 common/utils 目录)
- **如果不存在**：
  必须立即根据本 Skill 中的 `assets/log_decorator.py` 内容，在项目中创建该文件。
  *告诉用户："检测到项目中缺失标准日志模块，我已自动为您创建 `utils/log_decorator.py`。"*

## 1. 架构规范 (Architecture)

**核心风格**：**面向对象 (OOP)** 为第一原则，以类为组织单元，实例属性承载状态。

### 1.1 Service 层设计规范

- **【推荐】使用类封装**：所有业务 Service 应写成 Class，使用实例属性管理状态。
- **【推荐】实例方法 + 实例属性**：使用 `self.xxx` 访问配置、客户端、缓存，而非通过参数传递。
- **【避免】静态方法**：减少使用 `@staticmethod`，优先使用实例方法。
- **【避免】纯函数式 Service**：将 Service 写成一组纯函数，宜使用类封装。

### 1.2 工具类/辅助类设计规范

- **解析器 (Parser)**：推荐使用类封装，实例方法而非静态方法。
- **客户端 (Client)**：推荐使用类封装，配置通过 `__init__` 注入。
- **数据转换**：简单转换可用函数，复杂转换推荐使用类。

### 1.3 Controller 层 (瘦接口)

- 代码行数限制：< 20 行。
- 职责：仅负责 Pydantic 参数校验、调用 Service、返回 HTTP Response。
- **严禁**：编写业务逻辑、SQL 查询。

### 1.4 KISS 原则

- 无状态逻辑可用函数（如纯计算、数据转换）；有状态时必须用 Class。
- 不要过度封装，但一旦需要状态管理，立即使用类。

## 2. 日志规范 (Logging Strategy)
**目标**：通过 AOP (切面编程) 实现全自动排查能力，保持业务代码纯净。

- **日志前缀示例**：`2025-11-24T00:46:54.614 [INFO]text_splitter.py:62 - `
- **【强制】使用装饰器**：
  任何 **Service 层的公开方法** 和 **第三方 API 调用函数**，必须加上 `@log_execution` 装饰器。
- **【禁止】手动打点**：
  严禁在业务函数内部写 `logger.info("start...")` 或 `logger.info("end...")`。装饰器已经处理了所有入参、出参和耗时。

## 3. 代码风格 (KISS & Clean Code)

  - **Type Hints 即文档**：使用 Python 类型提示。
  - **注释零容忍**：
      - **禁止**写 Docstring，除非函数逻辑极其复杂（Regex、算法）。
      - **禁止**写"翻译代码"的行内注释。
      - 代码本身必须自解释。
  - **命名规范**：变量名必须全称，禁止 `res`, `tmp`, `data`, `info`。
  - **模块组织规范**：
      - **`__init__.py` 只做导出**：严禁在 `__init__.py` 中放置实现代码。
      - **实现与导出分离**：业务逻辑、工具函数必须放在独立模块中（如 `client.py`, `service.py`）。

## 4. Pydantic 数据验证（如果项目使用）

- **BaseModel 必须设置** `protected_namespaces=()`

## 5. 代码质量工具链 (Quality Tools)

**工具概览**：

| 工具 | 用途 | 配置位置 |
|------|------|----------|
| **Ruff** | 格式化 + Lint | `pyproject.toml [tool.ruff]` |
| **MyPy** | 静态类型检查 | `pyproject.toml [tool.mypy]` |
| **Pyright** | 类型检查 (VSCode Pylance 同款) | `pyproject.toml [tool.pyright]` |

**快速命令**：

```bash
make check      # 一键检查 (推荐)
make lint       # 格式化 + Lint
make typecheck  # 类型检查 (mypy + pyright)
make format     # 仅格式化
```

**Ruff 配置示例** (`pyproject.toml`)：

```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP"]
ignore = ["B008", "E501"]  # B008: 函数参数默认值调用函数; E501: 行过长

[tool.ruff.format]
quote-style = "double"
```

**类型检查模式**：

| 模式 | MyPy | Pyright | 说明 |
|------|------|---------|------|
| 基础 | 默认 | `typeCheckingMode = "basic"` | 平衡 (推荐) |
| 严格 | `strict = true` | `typeCheckingMode = "strict"` | 最严格 |

**常见类型问题修复**：

```python
# 错误: None 不能赋值给 str
class Service:
    def __init__(self):
        self._url = getattr(settings, "url", None)
        requests.post(self._url, ...)

# 修复: 添加类型注解 + 显式检查
class Service:
    _url: str

    def __init__(self):
        url = getattr(settings, "url", None)
        if not url:
            raise ValueError("URL 未配置")
        self._url = url
```

**CI 集成**：

```yaml
- name: Lint
  run: uv run ruff check .

- name: Type Check
  run: uv run mypy src/ && uv run pyright src/
```

**Dev 依赖**：

```toml
[dependency-groups]
dev = [
    "ruff>=0.15",
    "mypy>=1.0",
    "pyright>=1.1",
    "types-requests>=2.32.4.20260107",
]
```

# 最终检查清单 (Verification)

1.  **是否优先使用类和实例方法**？（避免使用 `@staticmethod`）
2.  Service 的配置/客户端是否通过实例属性 (`self.xxx`) 获取？（而非参数传递）
3.  业务函数是否很短？（如果长，请拆分）
4.  业务函数里是否没有 `logger.info`？（全靠装饰器）
5.  是否只有复杂的函数才有 Docstring？（简单的全删掉）
6.  如果使用 Pydantic，是否设置了 `protected_namespaces=()`？
7.  `__init__.py` 是否只包含导出？（实现代码必须在独立模块中）
8.  是否已经自动创建了 `utils/log_decorator.py`？
9.  提交前是否运行 `make check` 通过？
