---
name: smart-lsp
description: 智能代码导航：自动选择最佳工具进行符号搜索、定义查找、引用查找等LSP操作。当LSP工具不可用时，自动降级到命令行工具（gopls/ctags/ripgrep等），对用户透明。
---

# Smart LSP - 智能代码导航 Skill

## 设计理念

**双层策略，无缝切换**：
1. **优先使用 LSP 工具** - Claude Code 内置的 LSP 客户端
2. **自动降级到命令行工具** - 当 LSP 不可用时，使用语言特定的命令行工具

用户无感知，获得最可靠的代码导航体验！

## 自动触发条件

当用户提出以下需求时，自动使用此 skill：
- "查找所有 X 函数" / "搜索符号" / "find symbols"
- "查找定义" / "go to definition" / "在哪里定义的"
- "查找引用" / "find references" / "哪里调用了这个函数"
- "查看函数签名" / "show signature"
- "列出文件中的函数" / "list functions in file"
- "代码导航" 相关的任何操作

## 工作流程

### 第一步：环境检测

```bash
# 1. 检测项目类型
ls go.work go.work.sum 2>/dev/null && echo "Go Workspace"
ls go.mod 2>/dev/null && echo "Go Module"
ls package.json tsconfig.json 2>/dev/null && echo "Node/TS"
ls pyproject.toml setup.py 2>/dev/null && echo "Python"
ls Cargo.toml 2>/dev/null && echo "Rust"

# 2. 检测 LSP 可用性
# （Claude Code 自动检测 LSP 服务器）
```

### 第二步：工具选择矩阵

| 语言 | LSP 工具 | Fallback 命令行工具 | 备注 |
|------|---------|-------------------|------|
| **Go** | gopls | `gopls workspace_symbol`<br>`gopls definition` | 完美支持 Go Workspace |
| **Python** | pylsp<br>jedi-language-server | `rg` + `ctags`<br>或 `ast` 模块 | 静态分析 |
| **JavaScript/TypeScript** | tsserver<br>typescript-language-server | `rg` + `ctags`<br>或 `ast-grep` | 需要构建 |
| **Rust** | rust-analyzer | `rg` + `ctags` | 通常 LSP 可用 |
| **C/C++** | clangd | `rg` + `ctags`<br>或 `global` (GNU Global) | 需要编译数据库 |

### 第三步：执行操作

#### 方案 A：LSP 工具可用（优先）

```python
# 使用 Claude Code 的 LSP 工具
LSP(
  operation="workspaceSymbol|goToDefinition|findReferences|...",
  filePath="...",
  line=1,
  character=1
)
```

#### 方案 B：LSP 不可用（降级）

**Go 项目（使用 gopls）**：
```bash
# 符号搜索
gopls workspace_symbol <关键词>

# 查找定义
gopls definition <文件>:<行>:<列>

# 查找引用
gopls references <文件>:<行>:<列>

# 文件符号
gopls symbols <文件>
```

**通用项目（使用 ripgrep + ctags）**：
```bash
# 符号搜索（使用 ripgrep）
rg "^(func|def|class|interface|type) <符号名>" --type go

# 使用 ctags（需要安装）
ctags -R --fields=+ne -f -
ctags -x --sort=no src/ | grep "符号名"

# 组合搜索（强大！）
rg "func init\(\)" --type go -l
```

**Python 项目（使用 ast 模块）**：
```python
python3 << 'EOF'
import ast
import sys

with open(sys.argv[1]) as f:
    tree = ast.parse(f.read())

for node in ast.walk(tree):
    if isinstance(node, ast.FunctionDef):
        print(f"{node.lineno}:{node.name}")
EOF
```

## 核心功能实现

### 1. 符号搜索（Symbol Search）

**自动选择逻辑**：
```
IF Go 项目:
    TRY: gopls workspace_symbol <关键词>
    OR: rg "func <关键词>\(" --type go
ELSE IF Python 项目:
    TRY: rg "^def <keyword>" --type py
    OR: 使用 ast 模块解析
ELSE:
    TRY: rg "class|def|function <keyword>"
    OR: ctags -x | grep <keyword>
```

**示例**：
```bash
# 查找所有 init() 函数
# Go 项目
gopls workspace_symbol init | grep "init.*Function" | grep -v "_Cfunc"

# 或使用 ripgrep
rg "^func init\(\)" --type go -n
```

### 2. 查找定义（Go to Definition）

**自动选择逻辑**：
```
IF Go 项目:
    TRY: gopls definition <文件>:<行>:<列>
    OR: rg "func <函数名>\(" --type go -A 5
ELSE:
    TRY: rg "^(def|class|function) <函数名>" -A 10
```

**示例**：
```bash
# 查找 time_duration.go:42:6 的定义
gopls definition src/robot/.../time_duration.go:42:6

# 或使用 ripgrep
rg "func.*TimeDuration" --type go -B 2 -A 10
```

### 3. 查找引用（Find References）

**自动选择逻辑**：
```
IF Go 项目:
    TRY: gopls references <文件>:<行>:<列>
    OR: rg "<函数名>" --type go -n
```

**示例**：
```bash
# 查找谁调用了某个函数
gopls references src/robot/.../base.go:22:1

# 或使用 ripgrep
rg "InitFoundation\(" --type go -n
```

### 4. 列出文件符号（Document Symbols）

**自动选择逻辑**：
```
IF Go 项目:
    TRY: gopls symbols <文件>
    OR: rg "^(func|type|const|var)" <文件> -n
```

**示例**：
```bash
# 列出文件中的所有函数
gopls symbols src/robot/foundation/common/embedding/base.go

# 或使用 ripgrep
rg "^(func|type|const|var)" src/robot/.../base.go -n
```

## 最佳实践

### 1. Go Workspace 项目特殊处理

**问题**：根目录没有 `go.mod`，LSP 工具初始化失败
**解决**：直接使用 `gopls` 命令行工具（完美支持 workspace）

```bash
# ✅ 推荐
gopls workspace_symbol init

# ❌ 避免
LSP(workspaceSymbol, ...)  # 会失败
```

### 2. 大型项目性能优化

```bash
# 设置超时，防止长时间扫描
timeout 10 gopls workspace_symbol <关键词>

# 限制搜索范围
gopls workspace_symbol <关键词> | grep "/foundation/"

# 使用缓存
# gopls 会自动缓存索引，第二次搜索很快
```

### 3. 结果过滤和格式化

```bash
# 过滤噪音（排除生成的代码）
gopls workspace_symbol init | grep -v "pb.go" | grep -v "_Cfunc"

# 提取位置信息
gopls workspace_symbol init | awk '{print $1}' | sed 's/:$//'

# 统计数量
gopls workspace_symbol init | wc -l
```

## 输出格式标准化

无论使用哪种工具，统一输出格式：

```
文件路径:行号:列号 [符号类型] 符号名
```

示例：
```
src/robot/foundation/common/embedding/base.go:22:6 [Function] init()
src/robot/foundation/common/entity_recognise/time_duration.go:42:6 [Function] init()
```

## 常见问题排查

### Q1: gopls 卡住不动？
```bash
# 检查 gopls 进程
ps aux | grep gopls

# 重启 gopls
pkill gopls
gopls serve &
```

### Q2: ripgrep 找不到符号？
```bash
# 确认正则表达式
rg "func init\(\)" --type go

# 不区分大小写
rg "func init\(\)" --type go -i

# 搜索更多文件类型
rg "func init\(\)" -type-add 'go:*.go' --type go
```

### Q3: ctags 没有安装？
```bash
# Ubuntu/Debian
sudo apt-get install universal-ctags

# macOS
brew install ctags

# 验证
ctags --version
```

## 技术细节

### Go Workspace 项目检测

```bash
# 检测是否为 Go Workspace
if [ -f go.work ] && [ ! -f go.mod ]; then
    echo "Go Workspace detected - use gopls CLI"
fi
```

### LSP 工具可用性检测

Claude Code 自动检测，但可以通过错误信息判断：
```
No LSP server available for file type: .go
```
→ 立即降级到命令行工具

### 工具优先级决策树

```
用户请求符号搜索
    ↓
检测项目类型和文件类型
    ↓
LSP 工具可用？
    ├─ 是 → 使用 LSP 工具
    └─ 否 → 检测是否有命令行工具
            ├─ 有 → 使用命令行工具
            └─ 无 → 提示用户安装工具
```

## 示例对话

**用户**：查找所有 init() 函数

**Smart LSP**：
1. 检测项目：Go Workspace（`go.work` 存在）
2. 尝试 LSP 工具：失败（无 `go.mod`）
3. 自动降级：使用 `gopls workspace_symbol init`
4. 过滤结果：排除 `_Cfunc` 和生成的代码
5. 输出：
   ```
   找到 31 个 init() 函数：

   src/robot/foundation/updater/0_init.go:12:6
   src/robot/foundation/updater/0_init.go:41:6
   src/robot/foundation/common/embedding/bgem3.go:36:6
   ...
   ```

**用户**：`InitFoundation` 在哪里定义的？

**Smart LSP**：
1. 检测：Go 项目
2. 使用：`gopls workspace_symbol InitFoundation`
3. 找到定义：`src/robot/foundation/updater/bot_update.go:281`
4. 输出：
   ```
   定义位置：src/robot/foundation/updater/bot_update.go:281:6

   func InitFoundation() {
       // 初始化 Foundation 服务
       ...
   }
   ```

## 总结

**Smart LSP Skill 的价值**：
- ✅ **透明降级**：用户无需关心底层工具
- ✅ **语言无关**：支持 Go, Python, JS, Rust 等主流语言
- ✅ **高可用性**：LSP 失败时自动使用命令行工具
- ✅ **性能优化**：智能选择最快的工具
- ✅ **结果标准化**：统一的输出格式

**在 Go Workspace 项目中尤其有用，解决了 LSP 工具无法初始化的核心问题！**
