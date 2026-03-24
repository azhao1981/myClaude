
这两个不变，直接在页面上 fork update
- anthropics/claude-plugins-official	git@github.com:azhao1981/claude-plugins-official.git
- anthropics/skills	git@github.com:azhao1981/skills.git

这两个需要手动更新
- ref/planning-with-files	git@github.com:azhao1981/planning-with-files.git
- ref/wshobson/agents	git@github.com:azhao1981/agents.git

### planning-with-files-cn

```bash
git remote add github git@github.com:OthmanAdi/planning-with-files.git
git fetch github
git rebase github/master
git push -f
```

### sql-optimization-patterns-cn
```bash
git remote add github git@github.com:wshobson/agents.git
git fetch github
git rebase github/main
```