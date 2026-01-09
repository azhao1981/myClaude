#!/bin/bash
mkdir -p ~/.claude/skills
ln -nfs $(pwd)/ref/planning-with-files/planning-with-files-cn ~/.claude/skills/
ln -nfs $(pwd)/ref/wshobson/agents/plugins/developer-essentials/skills/sql-optimization-patterns-cn ~/.claude/skills/

ls -alF --color=always ~/.claude/skills/