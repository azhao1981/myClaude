请扮演一位基于官方文档 (https://code.claude.com/docs/en/skills) 的 **"Skill 审计专家"**。我要你对我本地的一个 Skill 进行深度技术审计。

目标 Skill 路径：ref/planning-with-files/planning-with-files

请按以下步骤执行操作并生成报告：

1.  **文件结构探查 (Discovery)**
    * 使用 `ls -R` 查看该 Skill 目录下的完整结构。
    * 读取 `SKILL.md` 的全部内容。
    * 检查是否存在 `scripts/` 目录以及任何辅助文件 (`reference.md`, `examples.md` 等)。

2.  **核心质量审计 (Audit Analysis)**
    请基于官方最佳实践，从三个维度进行评判：

    * **维度 A：元数据与触发机制 (The "Description" Check)**
        * *检查点*：读取 YAML Frontmatter 中的 `description`。
        * *评判*：它是否明确回答了“做什么(What)”和“何时用(When)”？是否包含用户自然会说的触发词(Keywords)？（官方强调这是 Claude 决定是否调用 Skill 的唯一依据）。

    * **维度 B：上下文卫生 (Context Hygiene / Progressive Disclosure)**
        * *检查点*：`SKILL.md` 是否简洁（官方建议 < 500 行）？
        * *评判*：它是否利用了“渐进式披露”？即：详细文档/长示例是否被剥离到了外部文件（如 `reference.md`）并在主文件中仅通过链接引用？(检查链接的文件是否真实存在)。

    * **维度 C：执行效率 (Agentic Efficiency)**
        * *检查点*：查看 `scripts/` 目录（如果有）。
        * *评判*：`SKILL.md` 是在指示模型“模拟逻辑”（低效），还是指示模型“运行脚本”（高效）？
        * *验证*：如果存在 Python 脚本，请简单读取脚本开头，确认它是否有明确的输入输出定义。

3.  **最终审计报告 (Output)**
    请输出一份包含以下内容的 Markdown 报告：
    * **⭐ 综合评分 (0-10分)**
    * **✅ 做的好的地方 (Highlights)**：(例如：“Description 设置得非常精准，包含了具体的动作词...”)
    * **⚠️ 改进建议 (Actionable Feedback)**：(例如：“主文件过长，建议将第 50-200 行的 API 列表移动到 reference.md” 或 “检测到复杂的正则验证逻辑，建议封装为 script”)