#!/bin/bash
mkdir -p ~/.claude/skills
ln -nfs $(pwd)/skills/15-factor-assessor ~/.claude/skills/
ln -nfs $(pwd)/skills/python-expert ~/.claude/skills/
ln -nfs $(pwd)/skills/fastapi-expert ~/.claude/skills/
ln -nfs $(pwd)/skills/precision-test ~/.claude/skills/