---
name: git-quick
description: When user says commit this file and git add fails because file is in .gitignore'd directory, just use git add -f. Do NOT diagnose.
when_to_use: User asks to commit a file, git add fails with "ignored by .gitignore", but sibling files in same directory are tracked. This means directory uses -f pattern.
---

# Git Add Ignored File(最短路径)

## 最短路径(2 步)

```
git add -f <file>
git commit -m <message>
```

## 不要做

- 不要 git check-ignore -v 诊断
- 不要 cat .gitignore
- 不要多次 git status
- 不要先 git add 失败再 -f
- 不要修改 .gitignore 规则

## 核心判断

如果同目录已有 tracked 文件,说明这目录的文件是项目既定通过 -f 强制跟踪的模式 — 直接 -f add 即可。

## 重要:已 tracked 文件也要用 -f

即使文件**已经**在 git 跟踪中(此前用过 `-f` add 过),**后续修改再 `git add`** 仍可能被 .gitignore 拦截,需要 `-f` 重复使用。

**反例**(2026-06-08, MDS骑手信息查询3PO 第 2 次 commit):
```bash
# 文件已 tracked, 但 .gitignore 仍在拦截
git add 'docs/mfc/raw/SOP...md'
# 报: The following paths are ignored by one of your .gitignore files: docs/mfc/raw
# 用户: "请加 git" — 看似已 tracked 应该能 add

# 正解: 直接 -f
git add -f 'docs/mfc/raw/SOP...md'
git commit -m '...'
```

**核心**:`.gitignore` 规则**不区分**文件是新增 vs 已 tracked, 只要路径在 ignore 列表里, 任何 `git add` 操作都要 `-f`。

## 反例(浪费 token 的 12 步)

git status → git ls-files → git status --short → cat .gitignore → git check-ignore -v → find .gitignore → git check-ignore -v <sibling> → sed -n → 思考怎么 add → git add 失败 → git add -f → git commit

正确流程 = 步骤 11 + 12。

## 历史踩坑(2026-06-08)

MDS骑手信息查询3PO文档 git add 时,我走了反例 12 步,浪费 ~10 个 tool call。用户批评: 一个简单的 git,为什么有这么多步。

## 相关

- 项目工作流: docs/mfc/raw/SOP流程图梳理/ 整个目录 .gitignore 但通过 -f 跟踪
- 同模式应用: 任何 docs/mfc/raw/ 下新建文件都直接 git add -f
- 真正想排除 .gitignore 时才用 git check-ignore -v 诊断
