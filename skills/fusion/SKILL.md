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
