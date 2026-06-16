#!/usr/bin/env python3
"""Fusion skill — 用 omp 并行 fan-out 多模型盲评，落盘 panel 结果。

裁判与合成由当前会话 Claude 承担（见 SKILL.md），本脚本只负责 panel 阶段。
"""
import argparse
import asyncio
import json
import sys
import time
from asyncio.subprocess import PIPE
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
PROMPTS_DIR = SKILL_DIR / "prompts"
DEFAULT_PANEL = [
    "zhipu/glm-5.2",
    "minimax-code-cn/minimax-m3",
    "xiaomi/mimo-v2.5-pro",
]
JUDGE_KEYS = {
    "consensus",
    "contradictions",
    "partial_coverage",
    "unique_insights",
    "blind_spots",
}


def build_omp_cmd(model, question, system_prompt_text):
    """构建单条 panel 的 omp 无头命令（盲评 + 防递归 + 不留痕）。
    system_prompt_text 为已读取的提示文本（omp --system-prompt 不支持 @file，须内联）。
    """
    return [
        "omp", "-p",
        "--no-tools", "--no-skills", "--no-extensions", "--no-rules", "--no-session",
        "--system-prompt", system_prompt_text,
        "--model", model,
        question,
    ]


def validate_judge_json(data):
    """[Task 5 实现】裁判 JSON 必须是含五键的 dict。"""
    raise NotImplementedError


def filter_panel_results(results):
    """[Task 6 实现】把 panel 结果分流为 (responses, failed)。"""
    raise NotImplementedError
