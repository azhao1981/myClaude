

## install


```bash
pnpm install -g @anthropic-ai/claude-code

claude --version
```

## uage

```bash
./links.sh
```

到项目的 claude 中： 请根据 15-factor skill 评估一下当前项目的架构。

## gemini create skill

```markdown
请忽略你以往关于 "Skills" 的所有知识（不要用 JSON Schema 或 MCP Tool 的格式）。 
必须阅读官方文档：https://code.claude.com/docs/en/skills 
阅读后,
直接给出一个最简短的 .md 文件格式模板（包含头部 YAML 和正文结构），以证明你掌握了正确的写法。
```
## code-simplifier

```bash
claude plugin install code-simplifier
/plugin install code-simplifier
# 请使用 code-simplifier 帮我整理一下刚才修改的代码。

# 更新
/plugin marketplace update claude-plugins-official
/plugin install code-simplifier@claude-plugins-official

```

.claude\plugins\marketplaces\claude-plugins-official\plugins\code-simplifier\agents 文件夹里。

## Skill: Planning with Files
这个是 manus 团队使用的技术，用于计划等

## ref:

[太狠了！把 Manus 核心秘诀做成 Skills 开源，Claude 瞬间进化！](https://mp.weixin.qq.com/s/0WV89hNCPgsa9lZwTLYABg)
https://github.com/OthmanAdi/planning-with-files

[SKILLS](https://dx72dwmn5vc.feishu.cn/wiki/NLUbwM4S2iGZIUkmo8BcN53Qnhf)

https://dx72dwmn5vc.feishu.cn/wiki/AlqIwSLsaiWjdKkycmbcrigTnig

```bash
git submodule add git@github.com:azhao1981/claude-plugins-official.git anthropics/claude-plugins-official
ule add git@github.com:azhao1981/skills.git anthropics/skills
git submodule add git@github.com:azhao1981/planning-with-files.git ref/planning-with-filesgit submod
git submodule add git@github.com:azhao1981/agents.git ref/wshobson/agents
# 初始化子模块
git submodule init

# 更新子模块（拉取代码）
git submodule update

# 或者一步完成
git submodule update --init --recursive
# 查看子模块状态
git submodule status

# 更新所有子模块
git submodule update --remote
# 删除子模块（需要多个步骤）
git submodule deinit <path>
git rm <path>
rm -rf .git/modules/<path>
```




## language

```bash
❯ code ~/.claude/settings.json 
"language": "chinese"
```
## Andrej Karpathy

你扮演 Andrej Karpathy，机器学习专家。
帮我