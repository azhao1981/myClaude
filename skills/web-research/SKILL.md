---
name: web-research
description: 选对网络研究工具、别全用 web_search 的判断：库/框架 API 查 Context7，GitHub 仓库架构问 DeepWiki，时效/观点/报错用 web_search，SPA 页面切 browser，多源调研并行组合。当任务需在这些工具间选择或组合多源时触发；单条普通搜索不必加载。Use when choosing among research tools, not for one quick lookup.
---

# Web Research — 工具选择判断

模型默认会把一切都丢给 `web_search`。这个 skill 只补一件事：**什么时候不该用 web_search**。
搜→抓→查的流水线模型已经会，不重复。

## ⚠️ 设计约定（改本 skill 前必读，别擅自"优化"掉）

下面几条反直觉，agent 最爱自作主张改坏——本 skill 被改坏过好几次，**每条都对应一次真实翻车**。把 WHY 写明白，是因为：连带着完整上下文的 agent 都理解错了，冷读的 agent 只会错得更狠。

1. **代理地址写在 skill 里、故意不进环境变量。** 进 env = 全局每次都走代理（不要的）；写在 skill = fetch 失败时按需手动取来兜底。别以"挪到 env 更规范 / 这是会变的配置"为由删它——**它就是 fetch 兜底机制本身**。
2. **默认直连，代理只在失败时手动加。** 国内站 / 自建服务直连最快；只有国外站直连超时才加代理。别改成默认走代理。
3. **SearXNG 域名、代理等具体值必须留着。** 这是"我本机多个 agent（OMP / Claude Code…）共用同一套基础设施"的需要——这里的"通用"指**我的各 agent 通用，不是发布给外人**。别拿"通用性 / 防腐烂"当理由删掉我的实际配置。
4. **fetch 抓不到，八成不是站点挂了。** 直连超时=没走代理；200 但内容空=SPA。先按「fetch 失败分诊」对症，别瞎重试或直接放弃。
5. **GitHub 仓库别图快用 web_search。** 慢一点的 DeepWiki 才给源码级答案（见下「核心判断」硬规则）。

## 核心判断（模型默认会做错的地方）

- **查库/框架 API，别 web_search → 用 Context7**：官方文档直出，比搜索引擎的二手博客准。
- **GitHub 仓库的实现/架构/某功能怎么做 = 硬规则先 DeepWiki**：命中 `github.com/owner/repo` 就第一步调 DeepWiki，**不准先用 web_search 凑**。慢(30-120s)是正常的，换来的是源码级答案；web_search 只够得到 README。只有"有没有类似项目 / 火不火"这种发现类才用搜索。
- **`read` 抓 SPA 会拿到空壳**（见下「fetch 失败分诊」），别误判成"页面没内容"。
- **摘要够用就别再 read**：web_search 已经给出答案时，多抓一次 URL 是纯浪费 token。
- **独立的线并行发起**：互不依赖的 search / read / Context7 / DeepWiki 放同一 turn 并行，别串行干等。

## 选哪个工具（唯一判断表）

| 用户意图 | 用哪个 | 别用 |
|----------|--------|------|
| "X 是什么 / 最新进展 / 哪个更好" | web_search | — |
| 某库/框架 API 怎么用（Depends、useEffect、新版特性） | **Context7** | ❌ web_search |
| 某库报错怎么解决（实战经验） | web_search | Context7（文档没有报错案例） |
| 某 GitHub 仓库的架构 / 模块 / 实现细节 | **DeepWiki** | ❌ web_search |
| "有哪些类似 X 的项目"（发现类） | web_search | DeepWiki（只能问已知 repo） |
| 给了 URL 要看内容 | read（native） | — |
| URL 是 SPA（JS 渲染） | browser 工具 | read（只拿到空壳） |

## fetch 失败分诊（先分诊，别盲目重试）

默认**直连抓取**——国内站 / 自建服务直连最快。失败时按现象对症，**不要默认每次走代理**。

| fetch 现象 | 病因 | 处理 |
|------------|------|------|
| 超时 / 卡住 / code 000 | 国外站，直连不通 | **手动加代理重试**（见下命令） |
| 200 但内容空 / 只有 `<div id="root\|app\|__next">` | SPA，JS 没渲染 | 切 `browser` 渲染，或 Jina Reader |
| `"Please enable JavaScript"` | 同上，SPA | 同上 |
| 抓到一半截断 / 乱码 | UA / 压缩 | 补 `-A` UA、`--compressed` 重试 |
| HTML 本来就有大量正文 | 不是病，SSR | native 直连即可 |

**代理 = 失败兜底，故意不进环境变量**（进了就全局每次走代理，不是想要的）；地址记在本 skill + `~/.env`，按需手动取：

```bash
PROXY="http://172.30.144.1:1082"            # WSL→Win 网关:1082；重启变了就用下一行动态取
# PROXY="http://$(ip route show default | awk '{print $3}'):1082"
curl -x "$PROXY" -sSL -A "Mozilla/5.0" <url>   # 仅在直连超时/连不上时手动用
```

native fetch 工具抓不到时，退到这条 `curl -x` 取内容。

## 工具调用速查（只给真名，语法不教）

- **Context7 MCP**：两步——`resolve-library-id`（解析库名）→ `query-docs`（查文档）。完整工具名以运行时 MCP 注册为准，不写死。
- **DeepWiki**：用 `deepwiki-ask` skill 对 `owner/repo` 提问（`--structure` 看目录，`-q` 提问）。
- **web_search / read / browser**：native 工具，调用语法模型已知。

## 评测集（路由边界）

### 正例（该加载）

- "调研一下 Crawl4AI 这个工具"（要组合 search + Context7 + DeepWiki）
- "FastAPI 的依赖注入怎么用"（该走 Context7 而非搜索）
- "langchain 的 LCEL 是怎么实现的"（该走 DeepWiki）
- "这个 github 仓库怎么实现的"（强制先 DeepWiki，别 web_search 凑）
- "web_search 出来的链接 fetch 不了"（分诊：超时→加代理，空壳→SPA→browser）
- "这个 pricing 页面 read 抓不到内容"（SPA 判断）

### 负例（不该加载）

| 请求 | 原因 |
|------|------|
| "帮我搜一下今天天气" | 单条普通 web_search，无需选型 |
| "什么是 RAG" | 概念问答，模型直接答 |
| "读一下这个 README 文件"（本地） | read 本地文件，不是网络研究 |
| "帮我写段爬虫代码" | 普通 coding task |

### 临近混淆

| 请求 | 实际应该 |
|------|----------|
| "查一篇 arxiv 论文" | arxiv skill |
| "帮我优化提示词" | prompt-design |

## 当前环境配置

| 项 | 配置 |
|------|------|
| web_search | provider=searxng，endpoint=`https://search.us.gezhishirt.club`（自建 SearXNG） |
| fetch | provider=auto（native 优先，SPA fallback 到 browser） |
| 代理 | `172.30.144.1:1082`（WSL→Win 网关，重启会变）——**fetch 失败时手动兜底，故意不进环境变量**，用法见「fetch 失败分诊」 |
| Context7 | MCP 已连接，无需额外配置 |
| DeepWiki | `deepwiki-ask` skill（`~/.claude/skills/deepwiki-ask/`） |

> 生效配置在 harness（OMP: `~/.omp/agent/config.yml` + `~/.env`）；上表是当前实际值，改配置去改源头，本表仅作排障对照。

## See Also

- [[concepts/web-search]] — web_search + fetch 工具完整文档
- [[entities/jina-reader]] — Jina Reader 远程抓取服务
- `~/.claude/skills/deepwiki-ask/SKILL.md` — DeepWiki 仓库查询
- `~/.claude/skills/arxiv/SKILL.md` — arXiv 学术论文搜索
