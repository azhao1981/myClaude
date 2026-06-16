import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_fusion import build_omp_cmd, validate_judge_json, filter_panel_results, safe_decode


def test_build_omp_cmd_has_blind_flags():
    cmd = build_omp_cmd("xiaomi/mimo-v2.5-pro", "1+1?", "你是盲评专家")
    assert cmd[0] == "omp"
    assert "-p" in cmd
    assert "--no-skills" in cmd      # 防递归
    assert "--no-tools" in cmd       # 纯作答
    assert "--no-extensions" in cmd
    assert "--no-rules" in cmd
    assert "--no-session" in cmd     # 不留痕
    assert "--model" in cmd
    assert "xiaomi/mimo-v2.5-pro" in cmd
    assert "你是盲评专家" in cmd        # 系统提示内联
    assert not any(str(x).startswith("@") for x in cmd)  # omp --system-prompt 不支持 @file


def test_build_omp_cmd_question_is_last_arg():
    cmd = build_omp_cmd("m", "我的问题", "sysp")
    assert cmd[-1] == "我的问题"


def test_validate_judge_json_all_keys_present():
    assert validate_judge_json({
        "consensus": [], "contradictions": [],
        "partial_coverage": [], "unique_insights": [], "blind_spots": [],
    }) is True


def test_validate_judge_json_missing_key():
    assert validate_judge_json({"consensus": [], "contradictions": []}) is False


def test_validate_judge_json_not_dict():
    assert validate_judge_json([]) is False
    assert validate_judge_json("not a dict") is False


def test_filter_panel_results_splits_ok_and_failed():
    results = [
        {"model": "a", "ok": True, "content": "ans"},
        {"model": "b", "ok": False, "error": "boom"},
        {"model": "c", "ok": True, "content": "ans2"},
    ]
    responses, failed = filter_panel_results(results)
    assert [r["model"] for r in responses] == ["a", "c"]
    assert [r["model"] for r in failed] == ["b"]


def test_filter_panel_results_all_failed():
    results = [{"model": "a", "ok": False, "error": "x"}]
    responses, failed = filter_panel_results(results)
    assert responses == []
    assert len(failed) == 1


def test_safe_decode_handles_truncated_multibyte():
    # 0xe9 是 UTF-8 多字节字符首字节，单独出现即截断/非法（重现 glm 64KB 边界截断 bug）
    assert safe_decode(b"abc\xe9") == "abc�"


def test_safe_decode_strips_whitespace():
    assert safe_decode(b"  hello\n\n") == "hello"
