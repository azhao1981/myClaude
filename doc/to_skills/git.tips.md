

## 指定人提交的文件

```bash
# 某个人所有提交的文件
git log --author="weiz" --name-only --pretty=format: | sort -u
# 某区间内提交的文件
git log --author="weiz" --name-only --pretty=format: commit1..commit2 | sort -u
# 某人最近n次提交的文件
git log --author="weiz" --name-only --pretty=format: -n 4 | sort -u
```