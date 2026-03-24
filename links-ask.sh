#!/bin/bash
mkdir -p ~/.claude/skills
ln -nfs $(pwd)/anthropics/skills/skills/pdf ~/.claude/skills/
ln -nfs $(pwd)/anthropics/skills/skills/docx ~/.claude/skills/
ln -nfs $(pwd)/anthropics/skills/skills/xlsx ~/.claude/skills/
ln -nfs $(pwd)/anthropics/skills/skills/pptx ~/.claude/skills/
ln -nfs $(pwd)/anthropics/skills/skills/skill-creator ~/.claude/skills/

ls -alF --color=always ~/.claude/skills/