#!/bin/bash
mkdir -p ~/.claude/skills
ln -nfs $(pwd)/ref/planning-with-files/planning-with-files-cn ~/.claude/skills/

ls -alF --color=always ~/.claude/skills/