更新一下我们的 submodule ，并看下他们都更新了什么
哪些是我们需要的
哪些是新增加有用的


创建一个 SKILLS: git-expert

整理和合并分支

执行步骤：
1. git log --oneline -10  # 查看最近提交，找到分叉基线 + 查找任务标签
2. git reset --soft {基线分支或commit}  # 软重置到分叉点，保留修改到暂存区
3. git status && git diff --stat  # 查看当前分支相对于基线的差异
4. git commit -m "{任务标签} {类型}: {描述}"  # 将所有修改合并为一次提交
5. git push -f origin {当前分支}  # 强制推送 feature 分支（历史已改写）
6. git fetch origin && git rebase origin/develop  # 与远程 develop 同步
7. git checkout develop && git pull  # 切换到本地 develop，拉取最新
8. git merge --ff-only {当前分支}  # 快进合并 feature 分支

关键规则：
- 分叉点识别：从 git log 图形中找到当前分支的起始点（通常是 develop/master，或具体 commit）
- 任务标签来源（按优先级）：
  1. 用户的对话中明确提供
  2. 从 git log 中的历史提交查找（如 "09aebf5 AI-2905 短信工具"）
  3. 如果都找不到，必须询问用户："任务编号和描述是什么？"
- Commit 格式："{任务标签} {类型}: {描述}"，标签必须在最前面
- 如果无法确定分叉点，询问用户："reset 到哪个分支/commit？"
- git push -f 只推送 feature 分支，绝不推送 origin develop