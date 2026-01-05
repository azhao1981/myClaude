#!/bin/bash
mkdir -p ~/.claude/skills
ln -nfs $(pwd)/main/CLAUDE.md ~/.claude/CLAUDE.md
ln -nfs $(pwd)/skills/15-factor-assessor ~/.claude/skills/
ln -nfs $(pwd)/skills/python-expert ~/.claude/skills/
ln -nfs $(pwd)/skills/fastapi-expert ~/.claude/skills/
ln -nfs $(pwd)/skills/precision-test ~/.claude/skills/
ln -nfs $(pwd)/skills/define-tech-spec ~/.claude/skills/
ln -nfs $(pwd)/skills/code-review ~/.claude/skills/
ln -nfs $(pwd)/skills/coding-style/ ~/.claude/skills/
ln -nfs $(pwd)/skills/prompt-design/ ~/.claude/skills/
ln -nfs $(pwd)/skills/tdd-workflow/ ~/.claude/skills/
ln -nfs $(pwd)/skills/technical-analysis/ ~/.claude/skills/