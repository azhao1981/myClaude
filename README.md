

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

## ref:

让 gemini 帮写Prompt时一定要加上这个，不然他不认识skills

https://code.claude.com/docs/en/skills

[SKILLS](https://dx72dwmn5vc.feishu.cn/wiki/NLUbwM4S2iGZIUkmo8BcN53Qnhf)

https://dx72dwmn5vc.feishu.cn/wiki/AlqIwSLsaiWjdKkycmbcrigTnig

```bash
git submodule add git@github.com:azhao1981/skills.git anthropics/skills
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
