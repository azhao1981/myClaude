---
name: python-expert
description: Python 开发终极指南。强制执行：Service Layer 架构、KISS 极简代码风格、以及基于装饰器的全自动结构化日志。
author: You
version: 3.0.0
---

# Python Expert Development Guidelines

当用户进行 Python 编码任务时，必须严格遵守以下流程和规范。

## 0. 环境自检 (Pre-flight Check)
在编写任何业务代码前，先检查当前项目是否存在日志工具。
- **检查路径**：`utils/log_decorator.py` (或类似 common/utils 目录)
- **如果不存在**：
  必须立即根据本 Skill 中的 `assets/log_decorator.py` 内容，在项目中创建该文件。
  *告诉用户：“检测到项目中缺失标准日志模块，我已自动为您创建 `utils/log_decorator.py`。”*

## 1. 架构规范 (Architecture)
- **Controller (瘦接口)**：
  - 代码行数限制：< 20 行。
  - 职责：仅负责 Pydantic 参数校验、调用 Service、返回 HTTP Response。
  - **严禁**：编写业务逻辑、SQL 查询。
- **Service (核心业务)**：
  - 职责：处理所有业务逻辑、事务管理。
  - **KISS 原则**：不要过度封装。如果逻辑简单，直接写函数；只有需要状态管理时才写 Class。

## 2. 日志规范 (Logging Strategy)
**目标**：通过 AOP (切面编程) 实现全自动排查能力，保持业务代码纯净。

- ** 日志前缀示例 **：`2025-11-24T00:46:54.614 [INFO]text_splitter.py:62 - `
- **【强制】使用装饰器**：
  任何 **Service 层的公开方法** 和 **第三方 API 调用函数**，必须加上 `@log_execution` 装饰器。
- **【禁止】手动打点**：
  严禁在业务函数内部写 `logger.info("start...")` 或 `logger.info("end...")`。装饰器已经处理了所有入参、出参和耗时。
- **【示例】**：
  ```python
  from utils.log_decorator import log_execution

  class UserService:
      @log_execution(op_name="CreateUser")
      def create_user(self, username: str, email: str) -> int:
          # 纯业务逻辑，不需要写任何日志代码
          user = self.repo.save(username, email)
          return user.id
````

## 3\. 代码风格 (KISS & Clean Code)

  - **Type Hints 即文档**：
    使用 Python 类型提示 (`def func(a: int) -> bool:`)。
  - **注释零容忍**：
      - **禁止**写 Docstring，除非函数逻辑极其复杂（Regex、算法）。
      - **禁止**写“翻译代码”的行内注释（如 `# 这里是循环`）。
      - 代码本身必须自解释。如果需要注释，说明代码写得烂，请重构代码。
  - **命名规范**：
    变量名必须全称，禁止 `res`, `tmp`, `data`, `info`。使用 `user_profile`, `payment_result` 等具体名称。

## 4. Pydantic 数据验证（如果项目使用）

- **BaseModel 必须设置** `protected_namespaces=()`，允许使用 `model` 等保留字段名（符合业界标准如 OpenAI API）

# 最终检查清单 (Verification)

在生成代码交付给用户前，执行以下自我审查：

1.  是否已经自动创建了 `utils/log_decorator.py`？
2.  业务函数是否很短？（如果长，请拆分）
3.  业务函数里是否没有 `logger.info`？（全靠装饰器）
4.  是否只有复杂的函数才有 Docstring？（简单的全删掉）
5.  如果使用 Pydantic，是否设置了 `protected_namespaces=()`？
