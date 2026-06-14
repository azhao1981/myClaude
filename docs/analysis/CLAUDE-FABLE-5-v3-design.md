# Claude Fable 5 — v3 (CLI / Pi) 改造设计

> 本文件是 v3 prompt 的**设计依据**（四层转换 + 三图），不含 prompt 本身。
> prompt 正文见 `CLAUDE-FABLE-5-v3.md`（纯 prompt，无图无说明）。

## 定位

v2（claude.ai 沙箱聊天版）改造为 Pi / oh-my-pi 终端编码 agent 的 system prompt。手法：**以 v2 全文为基底，逐节剪裁（网页专属层）+ 修改（环境/工具/定位层），其余行为层大段保留**——不做摘要式重写。

## 四层转换（v2 网页 → v3 CLI）

| 层 | v2（网页） | v3（CLI / Pi） |
|---|---|---|
| 运行环境 | `/home/claude` 沙箱、`/mnt/*` 只读 | 本地真实文件系统 + 终端 REPL |
| 工具集 | Artifacts `create_file`/`present_files`、recipe/places/weather widget、MCP picker、`image_search` | `read`/`write`/`edit`/`bash` + LSP/调试器/子代理/web 搜索 |
| 渲染 | Artifacts UI、`{antml:cite}`、`{antml:invoke}` | 终端 markdown 纯文本 |
| 定位 | 全人群通用聊天助手 | 开发者编码 agent（默认放行 + 危险确认、自验证必经） |

**保留**：`claude_behavior` 全部（product/refusal/legal/tone/wellbeing/reminders/evenhandedness/mistakes/knowledge_cutoff）、`memory_system`、`search_instructions` 核心、skills 使用机制。
**剪裁**：`persistent_storage`(window.storage)、`mcp_app_suggestions`、`computer_use` 的 Artifacts 沙箱部分、`using_image_search_tool`、网页 `Tool Definitions` schema、`Claudeception`、`citation_instructions`、`network/filesystem_configuration`。
**修改**：Identity（web→CLI）、文件操作环境（沙箱→本地）、工具说明（网页工具→Pi 工具）。

---

## 设计图

### 一、业务流程图（已定稿）

```mermaid
graph TD
    Actor["开发者"] -->|"发起指令"| Entry["指令入口 (REPL)"]
    Entry --> Parse["意图解析与规划"]
    Parse --> D1{"需理解现状?"}
    D1 -- "是" --> Nav["导航能力<br/>读文件/搜符号/LSP"]
    Nav --> D2{"需行动?"}
    D1 -- "否" --> D2
    D2 -- "是" --> Risk{"危险操作?"}
    Risk -- "否" --> Act["行动能力<br/>执行/编辑/git"]
    Risk -- "是" --> Gate["权限确认点<br/>默认放行的例外"]
    Gate -- "通过" --> Act
    Gate -- "拒绝" --> Report["终端汇报"]
    Act --> Verify["自验证 必经<br/>LSP/调试器/相关测试"]
    Verify --> D3{"可并行拆分?"}
    D3 -- "是" --> Sub["子代理分派"]
    D3 -- "否" --> Merge["结果汇总"]
    Sub --> Merge
    Parse -. "需外部信息" .-> Research["外部检索<br/>web搜索/URL读取"]
    Research --> Merge
    Merge --> Report
    Report --> D4{"继续?"}
    D4 -- "是" --> Entry
    D4 -- "否" --> End(["会话结束"])
```

### 二、ER 图（已确认）

```mermaid
erDiagram
    DEVELOPER ||--o{ SESSION : "发起指令"
    SESSION ||--|| CAPABILITY_LAYER : "调用编排"
    CAPABILITY_LAYER {
        string kinds "导航/行动/验证/检索/编排"
    }
    CAPABILITY_LAYER ||--o{ WORKSPACE : "读写操作"
    WORKSPACE {
        string nature "本地真实文件系统"
    }
    CAPABILITY_LAYER }o--|| PERMISSION_BOUNDARY : "行动类受约束"
    PERMISSION_BOUNDARY {
        string policy "默认放行+危险确认"
    }
    CAPABILITY_LAYER ||--o{ VERIFICATION_LOOP : "每次行动后触发"
    VERIFICATION_LOOP {
        string mandate "必经回路"
    }
    CAPABILITY_LAYER ||--o{ SUBAGENT_POOL : "可并行分派"
    SUBAGENT_POOL {
        string mode "并行+独立上下文"
    }
    SUBAGENT_POOL }o--o{ WORKSPACE : "共享文件系统"
    SESSION }o--o{ PERSISTENT_DIRECTIVES : "启动时加载"
    PERSISTENT_DIRECTIVES {
        string source "skills/全局规则/记忆"
    }
    CAPABILITY_LAYER }o--o{ EXTERNAL_KNOWLEDGE : "按需检索"
    EXTERNAL_KNOWLEDGE {
        string source "web搜索/URL读取"
    }
    SESSION ||--o{ TERMINAL_OUTPUT : "产出汇报"
    TERMINAL_OUTPUT {
        string format "markdown纯文本"
    }
```

### 三、架构图（已确认）

```mermaid
graph TD
    subgraph EDGE["交互边界"]
        Dev["开发者"]
        IO["终端 IO<br/>指令接收 / 汇报渲染"]
    end

    subgraph CORE["编排核心"]
        Parse["意图解析与规划"]
        Loop["任务循环控制"]
        Sub["子代理<br/>独立上下文·并行"]
    end

    subgraph CAP["能力层"]
        Nav["导航<br/>读 / 搜符号 / LSP"]
        Act["行动<br/>执行 / 编辑 / git"]
        Verify["验证<br/>LSP / 调试器 / 测试"]
        Search["检索<br/>web 搜索 / URL"]
    end

    subgraph GOV["治理层（横切）"]
        Perm["权限边界<br/>默认放行 + 危险确认"]
        Directive["持久指令<br/>skills / 规则 / 记忆"]
        Safety["安全与 wellbeing 约束"]
    end

    subgraph RES["资源层"]
        WS["本地工作区<br/>真实文件系统"]
        Ext["外部知识源 web"]
    end

    Dev -->|"自然语言指令"| IO
    IO --> Parse --> Loop
    Loop -->|"调用"| Nav
    Loop -->|"调用"| Act
    Loop -->|"调用"| Search
    Act -->|"每次行动后·必经"| Verify
    Loop -->|"并行分派"| Sub
    Nav --> WS
    Act --> WS
    Verify --> WS
    Sub -->|"共享读写"| WS
    Search --> Ext
    IO -.->|"渲染输出"| Dev

    Perm -.->|"约束"| Act
    Directive -.->|"加载到"| Parse
    Safety -.->|"约束全程"| Loop
```
