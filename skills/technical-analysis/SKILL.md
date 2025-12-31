---
name: technical-analysis
description: 执行深度的五层技术分析和决策评估。当用户要求"分析"、"设计方案"或进行"技术决策"时使用此技能。
---

# 五层技术分析法 (Five-Layer Analysis)

按照以下五个维度进行深度分析，并在最后输出标准化的决策模板。

## 1. 数据结构 (Data Structure)
Bad programmers worry about the code. Good programmers worry about data structures.
- 核心数据是什么？谁拥有它？谁修改它？
- 可以在数据结构层面消除复杂度吗？

## 2. 特殊情况 (Special Cases)
好代码没有特殊情况。
- 识别所有的 if/else 分支。
- 哪些是糟糕设计的补丁？能否通过重构数据结构消除这些分支？

## 3. 复杂度审查 (Complexity Review)
如果实现需要超过3层缩进，重新设计它。
- 这个功能的本质是什么？（一句话说清）
- 当前方案用了多少概念？能否减半？

## 4. 破坏性分析 (Breaking Analysis)
Never break userspace.
- 列出所有受影响的现有功能。
- 如何在不破坏向后兼容性的前提下改进？

## 5. 实用性验证 (Practicality Verification)
Theory and practice sometimes clash. Theory loses.
- 这个问题在生产环境真实存在吗？
- 解决方案的复杂度是否与问题的严重性匹配？

## 输出模板

### 决策分析报告
- **【核心判断】** ✅ 值得做 / ❌ 不值得做 (基于 Linus 式直接判断)
- **【关键洞察】** (关于数据结构、复杂度或风险点的核心发现)
- **【技术方案】** (基于四大哲学的具体实现步骤)
- **【方案评分】** 🟢 A级 | 🟡 B级 | 🔴 C级 (附带理由)