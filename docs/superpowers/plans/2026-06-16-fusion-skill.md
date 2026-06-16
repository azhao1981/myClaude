# Fusion Skill 实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现一个 `fusion` skill——用 `omp` 并行 fan-out 多个不同模型盲评，由当前会话 Claude 做五维裁判并合成终稿（比较，而非合并）。

**Architecture:** `SKILL.md`（流程指令）+ `run_fusion.py`（asyncio 编排 panel fan-out via omp，落盘 JSON）+ `prompts/{panel,judge}.md`（盲评/裁判提示）。panel 阶段调 omp；judge 与 synthesis 由当前会话 Claude 承担，不再起 omp。脚本只含可测纯逻辑 + 最小集成层。

**Tech Stack:** Python 3.12（asyncio + argparse + subprocess）、`omp` CLI（Oh My Pi v16.0.1）、pytest 9.0.3、Markdown。

**对应 spec:** `docs/superpowers/specs/2026-06-16-fusion-skill-design.md`

---

## File Structure

| 文件 | 责任 | 创建/修改 |
|---|---|---|
| `skills/fusion/SKILL.md` | 触发条件 + 三段流程指令 | 创建 |
| `skills/fusion/run_fusion.py` | panel fan-out 编排（纯逻辑可测 + 集成层） | 创建 |
| `skills/fusion/test_run_fusion.py` | 纯逻辑单元测试 | 创建 |
| `skills/fusion/prompts/panel.md` | 面板成员盲评系统提示 | 创建 |
| `skills/fusion/prompts/judge.md` | 裁判五维 JSON 指南 | 创建 |
| `links.sh` | 注册 fusion 软链接 | 修改 |
| `.gitignore` | 忽略 `tmp/`（审议落盘） | 修改 |

**可测纯函数**（TDD）：`build_omp_cmd`、`validate_judge_json`、`filter_panel_results`。
**集成层**（端到端验证）：`call_panel`、`run_panel`、`main`、`parse_args`。

---

## Task 1: 脚手架与软链接注册

**Files:**
- Create: `skills/fusion/prompts/`（目录）
- Modify: `links.sh`
- Modify: `.gitignore`

- [ ] **Step 1: 创建 skill 目录结构**

Run:
```bash
mkdir -p skills/fusion/prompts
```

- [ ] **Step 2: 在 links.sh 末尾的 skills 块追加 fusion 软链接**

在 `links.sh` 第 20 行 `ln -nfs $(pwd)/skills/web-research ~/.claude/skills/` 之后插入一行：

```bash
ln -nfs $(pwd)/skills/fusion ~/.claude/skills/
```

- [ ] **Step 3: 在 .gitignore 追加 tmp/（审议结果落盘目录）**

在 `.gitignore` 末尾追加：

```
# Fusion 审议落盘结果
tmp/
```

- [ ] **Step 4: 跑 links.sh 验证软链接生效**

Run:
```bash
./links.sh 2>&1 | grep fusion
```
Expected: 一行显示 `fusion -> .../skills/fusion`

- [ ] **Step 5: Commit**

```bash
git add skills/fusion links.sh .gitignore
git commit -m "scaffold fusion skill: dir + symlink + gitignore tmp/"
```

---

## Task 2: 盲评系统提示 prompts/panel.md

**Files:**
- Create: `skills/fusion/prompts/panel.md`

- [ ] **Step 1: 写 panel.md**

写入 `skills/fusion/prompts/panel.md`：

```markdown
# 面板成员盲评提示

你是一名独立的研究专家。请独立、完整地回答用户的问题。

规则：
- 你是唯一的专家，独立作答。**绝不**提及任何其他 AI 模型，也不要假设存在评审小组或其他人。
- 不确定时，明确标注你的置信度。
- 直接给出你的专业判断，不要含糊。
```

- [ ] **Step 2: Commit**

```bash
git add skills/fusion/prompts/panel.md
git commit -m "add fusion panel blind-review prompt"
```

---

## Task 3: 裁判指南 prompts/judge.md

**Files:**
- Create: `skills/fusion/prompts/judge.md`

- [ ] **Step 1: 写 judge.md（五维 JSON schema）**

写入 `skills/fusion/prompts/judge.md`：

```markdown
# 裁判指南：比较而非合并

你是严谨的分析裁判。对比 panel 各模型对同一问题的回答。**不要**把它们合并成一段叙述，而是产出严格的结构化分析。

输出**单一合法 JSON 对象**，恰好包含这五个键（无内容用 `[]`）：

{
  "consensus": [
    {"claim": "...", "supported_by": ["模型id", ...]}
  ],
  "contradictions": [
    {"topic": "...", "stances": [{"model": "...", "stance": "主张+依据"}], "assessment": "哪方证据更强，或确属模糊"}
  ],
  "partial_coverage": [
    {"models": ["..."], "point": "仅部分模型提及，为何重要"}
  ],
  "unique_insights": [
    {"model": "...", "insight": "仅单一模型提出的高价值观点"}
  ],
  "blind_spots": [
    "..."
  ]
}

规则：
- 仅当 2+ 模型独立认同时才算 consensus。
- contradictions 按**证据质量**而非人数权衡。
- 每个主张归属到具体模型，主张保持原子化。
- 只输出 JSON，不要散文、不要 markdown 代码围栏。
```

- [ ] **Step 2: Commit**

```bash
git add skills/fusion/prompts/judge.md
git commit -m "add fusion judge five-dimension JSON guide"
```

---

## Task 4: run_fusion.py 骨架 + build_omp_cmd（TDD）

**Files:**
- Create: `skills/fusion/run_fusion.py`
- Create: `skills/fusion/test_run_fusion.py`

- [ ] **Step 1: 写失败测试 test_run_fusion.py**

写入 `skills/fusion/test_run_fusion.py`：

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from run_fusion import build_omp_cmd, validate_judge_json, filter_panel_results


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
```

> 注：`validate_judge_json` / `filter_panel_results` 的测试在 Task 5/6 追加，此处先 import 占位。

- [ ] **Step 2: 跑测试验证失败**

Run:
```bash
python3 -m pytest skills/fusion/test_run_fusion.py -v
```
Expected: FAIL — `ImportError: cannot import name 'build_omp_cmd' from 'run_fusion'`（模块尚不存在）

- [ ] **Step 3: 写 run_fusion.py 骨架 + build_omp_cmd**

写入 `skills/fusion/run_fusion.py`：

```python
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
```

- [ ] **Step 4: 跑测试验证通过**

Run:
```bash
python3 -m pytest skills/fusion/test_run_fusion.py -v
```
Expected: 2 passed（build_omp_cmd 两个测试通过；import 占位不报错因后续函数尚未定义会 NameError——见 Step 5 说明）

> Step 5 说明：因 test 文件顶部 import 了尚未定义的 `validate_judge_json`/`filter_panel_results`，此时会 ImportError。**故 Task 4 先在 run_fusion.py 追加两个占位桩**（Task 5/6 再填实现），保证 Task 4 测试能跑通：

在 `run_fusion.py` 的 `build_omp_cmd` 函数之后追加：

```python


def validate_judge_json(data):
    """[Task 5 实现】裁判 JSON 必须是含五键的 dict。"""
    raise NotImplementedError


def filter_panel_results(results):
    """[Task 6 实现】把 panel 结果分流为 (responses, failed)。"""
    raise NotImplementedError
```

重跑：
```bash
python3 -m pytest skills/fusion/test_run_fusion.py -v
```
Expected: 2 passed

- [ ] **Step 6: Commit**

```bash
git add skills/fusion/run_fusion.py skills/fusion/test_run_fusion.py
git commit -m "add run_fusion scaffold + build_omp_cmd (TDD)"
```

---

## Task 5: validate_judge_json（TDD）

**Files:**
- Modify: `skills/fusion/run_fusion.py`（替换 `validate_judge_json` 桩）
- Modify: `skills/fusion/test_run_fusion.py`（追加测试）

- [ ] **Step 1: 追加失败测试**

在 `test_run_fusion.py` 末尾追加：

```python
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
```

- [ ] **Step 2: 跑测试验证失败**

Run:
```bash
python3 -m pytest skills/fusion/test_run_fusion.py -v
```
Expected: 3 个 validate 测试 FAIL — `NotImplementedError`

- [ ] **Step 3: 实现 validate_judge_json**

把 `run_fusion.py` 中的桩替换为：

```python
def validate_judge_json(data):
    """裁判 JSON 必须是含五键的 dict。"""
    return isinstance(data, dict) and JUDGE_KEYS.issubset(data.keys())
```

- [ ] **Step 4: 跑测试验证通过**

Run:
```bash
python3 -m pytest skills/fusion/test_run_fusion.py -v
```
Expected: 5 passed

- [ ] **Step 5: Commit**

```bash
git add skills/fusion/run_fusion.py skills/fusion/test_run_fusion.py
git commit -m "implement validate_judge_json (TDD)"
```

---

## Task 6: filter_panel_results（TDD）

**Files:**
- Modify: `skills/fusion/run_fusion.py`（替换 `filter_panel_results` 桩）
- Modify: `skills/fusion/test_run_fusion.py`（追加测试）

- [ ] **Step 1: 追加失败测试**

在 `test_run_fusion.py` 末尾追加：

```python
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
```

- [ ] **Step 2: 跑测试验证失败**

Run:
```bash
python3 -m pytest skills/fusion/test_run_fusion.py -v
```
Expected: 2 个 filter 测试 FAIL — `NotImplementedError`

- [ ] **Step 3: 实现 filter_panel_results**

把 `run_fusion.py` 中的桩替换为：

```python
def filter_panel_results(results):
    """把 panel 结果分流为 (成功 responses, 失败 failed)。"""
    responses = [r for r in results if r.get("ok")]
    failed = [r for r in results if not r.get("ok")]
    return responses, failed
```

- [ ] **Step 4: 跑测试验证通过**

Run:
```bash
python3 -m pytest skills/fusion/test_run_fusion.py -v
```
Expected: 7 passed

- [ ] **Step 5: Commit**

```bash
git add skills/fusion/run_fusion.py skills/fusion/test_run_fusion.py
git commit -m "implement filter_panel_results (TDD)"
```

---

## Task 7: 集成层 call_panel / run_panel / main / CLI

**Files:**
- Modify: `skills/fusion/run_fusion.py`（追加集成函数 + `__main__`）

> 集成层依赖外部 `omp`/网络，不写单测；靠 Task 9 端到端验证。

- [ ] **Step 1: 在 run_fusion.py 末尾追加集成代码**

在 `filter_panel_results` 之后追加：

```python


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
            return {"model": model, "ok": False, "error": stderr.decode().strip()}
        return {"model": model, "ok": True, "content": stdout.decode().strip()}
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
    p.add_argument("question", help="要审议的问题")
    p.add_argument("--models", default=None, help="逗号分隔的模型列表，默认三人组")
    p.add_argument("--out", default="tmp", help="结果落盘目录")
    a = p.parse_args(argv)
    models = a.models.split(",") if a.models else list(DEFAULT_PANEL)
    return a.question, [m.strip() for m in models], Path(a.out)


if __name__ == "__main__":
    _q, _models, _out = parse_args(sys.argv[1:])
    _result = asyncio.run(main(_q, _models, _out))
    print(json.dumps(_result, ensure_ascii=False, indent=2))
    if _result.get("status") == "error":
        sys.exit(1)
```

- [ ] **Step 2: 语法自检（不调 omp）**

Run:
```bash
python3 -c "import sys; sys.path.insert(0,'skills/fusion'); import run_fusion; print('import ok')"
```
Expected: `import ok`

- [ ] **Step 3: 跑全量单元测试确认未回归**

Run:
```bash
python3 -m pytest skills/fusion/test_run_fusion.py -v
```
Expected: 7 passed

- [ ] **Step 4: Commit**

```bash
git add skills/fusion/run_fusion.py
git commit -m "add fusion integration layer: call_panel/run_panel/main/CLI"
```

---

## Task 8: SKILL.md（触发 + 流程指令）

**Files:**
- Create: `skills/fusion/SKILL.md`

- [ ] **Step 1: 写 SKILL.md**

写入 `skills/fusion/SKILL.md`：

````markdown
---
name: fusion
description: 多模型审议。对复杂/争议问题，用 omp 并行调多个不同模型盲评，再由当前会话 Claude 做五维裁判并合成终稿。比较而非合并。触发词：多模型审议 / fusion / 多视角 / 专家组 / 跨模型审议。
---

# Fusion：多模型审议

把一个复杂/争议问题扇出给多个不同模型**盲评**，裁判产出五维结构化对比，主编合成终稿。哲学：**比较，而非合并**。

> ⚠️ 成本警示：每次运行并发调用多个真实模型（默认 3 个），按各模型计费之和。仅用于值得多视角的难题，别拿简单问题浪费。

## ① Panel（盲评）— 跑脚本

用 omp 并行 fan-out 默认三人组（glm-5.2 / minimax-m3 / mimo-v2.5-pro），各自独立作答、互不可见：

```bash
python3 skills/fusion/run_fusion.py "<问题>"
```

想换模型就传 `--models "a,b,c"`。结果落盘 `tmp/fusion_<时间戳>.json` 并打印到 stdout。读取 `panel[].content` 与 `failed_models`。

## ② Judge（五维裁判）— 你来做

你是裁判。读全部 panel 原答，按 `prompts/judge.md` 的 schema 产出五维 JSON（consensus / contradictions / partial_coverage / unique_insights / blind_spots）。**比较，不要合并**；分歧辩证呈现。

可选自检五键齐全：

```bash
python3 -c "import sys; sys.path.insert(0,'skills/fusion'); from run_fusion import validate_judge_json; import json; print(validate_judge_json(json.loads(sys.argv[1])))" '<你的JSON>'
```

## ③ Synthesis（合成终稿）— 你来做

基于五维 JSON 写最终答案：以 consensus 为高置信根基；辩证呈现 contradictions；织入 unique_insights / partial_coverage；**主动补 blind_spots** 或坦承未知。单一口吻、干净 Markdown。

## 降级

- panel 部分失败 → 看 `failed_models`，用成功的继续。
- panel 全失败 → 如实报告，**不编**。
- judge JSON 残缺 → 标注"裁判降级"，直接从 panel 原答合成。

## 何时用

研究型、跨领域批判、容错成本高的决策、单模型答不好的难题。简单事实查询别用。
````

- [ ] **Step 2: Commit**

```bash
git add skills/fusion/SKILL.md
git commit -m "add fusion SKILL.md: trigger + three-stage flow"
```

---

## Task 9: 端到端验证（spec 第 9 节，精准、不全量、花钱）

> 每步只跑与该步直接相关的验证，禁止批量。以下会真实调用模型，产生费用。

- [ ] **Step 1: 验证①三模型 fan-out 跑通**

Run:
```bash
python3 skills/fusion/run_fusion.py "用一句话解释什么是闭包"
```
Expected: stdout 输出 JSON，`status` 为 `ok` 或 `partial`，`panel` 含 3 个（或部分）模型的 `content`，并提示 `saved_to: tmp/fusion_<ts>.json`。确认落盘文件存在且内容一致。

- [ ] **Step 2: 验证②judge 五键（当前会话 Claude 产出并自检）**

读取 Step 1 的 panel 原答，按 `prompts/judge.md` 产出五维 JSON，然后跑自检：

```bash
python3 -c "import sys; sys.path.insert(0,'skills/fusion'); from run_fusion import validate_judge_json; import json; print(validate_judge_json(json.loads(sys.argv[1])))" '<产出的JSON>'
```
Expected: `True`

- [ ] **Step 3: 验证③failed 降级路径**

故意指定一个不存在的模型，验证降级：

```bash
python3 skills/fusion/run_fusion.py "测试题" --models "xiaomi/mimo-v2.5-pro,nonexistent/fake-model-xyz"
```
Expected: `status: partial`，`failed_models` 含 `nonexistent/fake-model-xyz`，`panel` 仍含 mimo 的成功回答（流程不阻塞）。

- [ ] **Step 4: 收尾**

确认 `tmp/` 已被 git 忽略（Task 1 已加），落盘结果不进版本库。无需额外 commit（验证不产生源码改动）。

---

## Self-Review 记录

（写计划后自审，结果见下方；已据实修正。）

- **Spec 覆盖**：三段式（panel/judge/synthesis）→ Task 7/8/9；默认三人组 → Task 4 常量 + Task 9 验证；judge 默认当前会话 → Task 8 SKILL.md；`--no-skills` 防递归 → Task 4 build_omp_cmd + 测试；降级矩阵 → Task 7 main + Task 9 Step3；落盘留痕 → Task 7 + Task 1 gitignore。✅ 全覆盖。
- **占位符扫描**：无 TBD/TODO；Task 4 的桩是显式 TDD 中间态，已注明 Task 5/6 替换。✅
- **类型/签名一致**：`build_omp_cmd(model, question, panel_prompt)`、`validate_judge_json(data)`、`filter_panel_results(results) -> (responses, failed)` 全程一致。✅
- **风险**（spec 第 10 节）：glm-5.2 / minimax-m3 未实测可达——Task 9 Step1 默认三人组会一并验证，若某个不可达则 `partial` 降级暴露，再据实调整 `DEFAULT_PANEL`。
