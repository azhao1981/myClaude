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
    "deepseek/deepseek-v4-pro",
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
LARGE_THRESHOLD = 8192  # result JSON 超 8KB → stdout 只给指针，详情读落盘文件


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
    """裁判 JSON 必须是含五键的 dict。"""
    return isinstance(data, dict) and JUDGE_KEYS.issubset(data.keys())


def filter_panel_results(results):
    """把 panel 结果分流为 (成功 responses, 失败 failed)。"""
    responses = [r for r in results if r.get("ok")]
    failed = [r for r in results if not r.get("ok")]
    return responses, failed


def safe_decode(data: bytes) -> str:
    """安全解码字节流：遇非法/截断的多字节字符用替换符，不抛异常。"""
    return data.decode(errors="replace").strip()


def read_prompt(argv_question, prompt_file, stdin_text):
    """读取 panel 输入：优先 --prompt-file，其次 stdin（argv question == "-"），最后 argv。
    argv 有 ARG_MAX 物理限制，超大输入必须用文件/stdin。
    """
    if prompt_file:
        return Path(prompt_file).read_text(encoding="utf-8")
    if argv_question in (None, "-"):
        return stdin_text
    return argv_question


def format_output(result, threshold=LARGE_THRESHOLD):
    """大结果只输出指针（指向落盘文件），小结果输出完整 JSON。"""
    full = json.dumps(result, ensure_ascii=False, indent=2)
    size = len(full.encode("utf-8"))
    if size > threshold:
        return json.dumps(
            {"large": True, "saved_to": result.get("saved_to"),
             "status": result.get("status"), "size": size},
            ensure_ascii=False, indent=2,
        )
    return full


async def call_panel(model, question, panel_prompt_path):
    """跑单个 panel 模型。读取盲评提示文件内容后内联传入。
    成功 {model, ok, content}；失败 {model, ok, error}。
    """
    system_prompt_text = Path(panel_prompt_path).read_text(encoding="utf-8")
    cmd = build_omp_cmd(model, question, system_prompt_text)
    try:
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            return {"model": model, "ok": False, "error": safe_decode(stderr)}
        return {"model": model, "ok": True, "content": safe_decode(stdout)}
    except Exception as e:
        return {"model": model, "ok": False, "error": f"{type(e).__name__}: {e}"}


async def run_panel(models, question, panel_prompt):
    """并行 fan-out 全部 panel 模型，返回 (responses, failed)。"""
    tasks = [call_panel(m, question, panel_prompt) for m in models]
    results = await asyncio.gather(*tasks)
    return filter_panel_results(results)


async def main(question, models, out_dir):
    """编排：fan-out panel → 降级判定 → 落盘 JSON。返回结果 dict。"""
    responses, failed = await run_panel(models, question, PROMPTS_DIR / "panel.md")
    if not responses:
        result = {
            "status": "error",
            "failure_reason": "all_panels_failed",
            "failed_models": failed,
        }
    else:
        result = {
            "status": "ok" if not failed else "partial",
            "question": question,
            "models": models,
            "panel": responses,
            "failed_models": failed or None,
        }
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"fusion_{int(time.time())}.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    result["saved_to"] = str(path)
    return result


def parse_args(argv):
    p = argparse.ArgumentParser(description="Fusion panel fan-out via omp")
    p.add_argument("question", nargs="?", default=None,
                   help="要审议的问题；'-' 读 stdin；大输入用 --prompt-file")
    p.add_argument("--prompt-file", default=None, help="从文件读取问题（大输入主推）")
    p.add_argument("--models", default=None, help="逗号分隔的模型列表，默认三人组")
    p.add_argument("--out", default="tmp", help="结果落盘目录")
    a = p.parse_args(argv)
    models = a.models.split(",") if a.models else list(DEFAULT_PANEL)
    return a.question, a.prompt_file, [m.strip() for m in models], Path(a.out)


if __name__ == "__main__":
    _argv_q, _prompt_file, _models, _out = parse_args(sys.argv[1:])
    _stdin = sys.stdin.read() if (_argv_q in (None, "-") and not _prompt_file) else ""
    _q = read_prompt(_argv_q, _prompt_file, _stdin)
    if not _q.strip():
        sys.exit("error: 缺少问题（用位置参数 / --prompt-file / stdin '-' 提供）")
    _result = asyncio.run(main(_q, _models, _out))
    print(format_output(_result))
    if _result.get("status") == "error":
        sys.exit(1)
