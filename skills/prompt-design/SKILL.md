---
name: prompt-design
description: 设计高效的 LLM Prompt 或 Dify 编排。当用户要求"写Prompt"、"优化提示词"或"配置Dify"时使用。
---

# Prompt 设计与工程规范

## 1. KV Cache 优化原则 (Context Caching)
为了最大化利用 KV Cache 并降低推理延迟，必须严格遵守**静态在前，动态在后**的结构：

- **结构要求**:
  1. **System/Instruction** (静态): 任务定义、角色设定、输出格式。
  2. **Few-Shot Examples** (静态): 固定的示例库。
  3. **Reference Context** (静态): 知识库内容、固定文档。
  4. **User Input/Query** (动态): 用户当前的问题或变量 -> **必须放在最后**。

- **理由**: 这样设计可以确保前 90% 的 Context 被缓存，只有最后一部分需要重新计算。

## 2. 结构化思维
- 使用 Markdown 标题 (`#`, `##`) 清晰分隔模块。
- 复杂逻辑必须使用 `<thinking>` 或 `Steps` 引导模型思维链。
- 变量引用使用清晰的定界符 (如 `{{variable}}` 或 XML tags)。