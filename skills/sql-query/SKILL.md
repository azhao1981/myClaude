---
name: sql-query
description: 指导 AI 正确使用 SQL 命令行工具。强制优先使用原生 psql/mysql 执行查询，禁止用 Python 包装简单 SQL。
---

# SQL Query 执行策略

## 核心原则

**能用一条 SQL 解决的，禁止用 Python 包装。**

## 工具选择决策树

```
需要执行 SQL 吗？
├── 是：查询/更新/调试/探索
│   ├── 单条 SQL 能完成？ → 直接用 psql/mysql
│   ├── 需要循环/条件/多步？ → Python 脚本
│   └── 需要数据后处理（聚合、转换）？ → SQL 先做，Python 只处理 SQL 做不到的
└── 否 → 不需要本技能
```

## 命令行优先

### PostgreSQL (psql)

```bash
# 单条查询
psql -h host -U user -d db -c "SELECT * FROM users WHERE id = 1;"

# 带格式输出
psql -h host -U user -d db -c "\x" -c "SELECT * FROM users LIMIT 5;"

# 执行 SQL 文件
psql -h host -U user -d db -f query.sql

# 输出到 CSV
psql -h host -U user -d db -c "COPY (SELECT * FROM users) TO STDOUT CSV HEADER;"
```

### MySQL

```bash
# 单条查询
mysql -h host -u user -p db -e "SELECT * FROM users WHERE id = 1;"

# 垂直格式
mysql -h host -u user -p db -e "SELECT * FROM users LIMIT 5\G"

# 执行 SQL 文件
mysql -h host -u user -p db < query.sql

# 输出到 CSV
mysql -h host -u user -p db -e "SELECT * FROM users" | tr '\t' ','
```

## 禁止模式

### 禁止：用 Python 包装简单查询

```python
# 错误 ❌
import psycopg2
conn = psycopg2.connect(...)
cur = conn.cursor()
cur.execute("SELECT * FROM users WHERE id = 1")
result = cur.fetchone()
print(result)
```

正确做法：直接用 `psql -c "SELECT * FROM users WHERE id = 1;"`

### 禁止：用 Python 做 SQL 能做的聚合

```python
# 错误 ❌
results = cur.fetchall()
total = sum([r['amount'] for r in results])
```

正确做法：`SELECT SUM(amount) FROM orders;`

## 允许使用 Python 的场景

1. **循环批量操作**：需要根据条件动态生成 SQL
2. **跨库操作**：从 A 库读，写入 B 库
3. **复杂数据转换**：SQL 无法实现的业务逻辑
4. **需要留痕的测试脚本**：按 CLAUDE.md 规则写入 `tmp/` 目录

## 输出格式技巧

### psql 常用格式控制

```bash
# 扩展显示（垂直）
\x on

# 只输出数据（无表头）
\t on

# 输出为 HTML
\H

# 设置输出宽度
\pset format wrapped
\pset columns 100
```

### 直接导出

```bash
# psql 导出 CSV
\copy (SELECT * FROM users) TO '/tmp/users.csv' CSV HEADER

# mysql 导出
SELECT * FROM users INTO OUTFILE '/tmp/users.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
```

## 调试技巧

```sql
-- 查看执行计划
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';

-- 查看表结构
\d users           -- psql
DESCRIBE users;    -- mysql

-- 查看索引
\di users*         -- psql
SHOW INDEX FROM users;  -- mysql
```

## 与 sql-optimization-patterns 的关系

- **本技能**：决定「用什么工具执行 SQL」
- **sql-optimization-patterns**：决定「如何写出高效的 SQL」

两者互补，先用本技能选工具，再用优化技能写 SQL。
