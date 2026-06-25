# Framework Specs

本目录包含 framework 层面的正式规范文档。与 `guides/`（方法论指南）不同，`specs/` 定义的是**系统架构规则**——组件间如何交互、调用遵循什么约定、文件格式如何定义。

## 规范文件索引

| 文件 | 定位 |
|------|------|
| `interaction-spec.md` | Skill-Skill 交互规范——单层 Skill 模型、handoff 8 字段契约、稿件三层、调用约定、废弃引用 |
| `skill-template.md` | Skill SKILL.md 写法模板——5 必含字段（Identity/Contract/Flow/Triggers/Completion Criterion）|
| `agent-template.md` | Agent 写法模板——可选优化组件，仅在 Skill 不适合时使用 |
| `refactor-2026-06-24-skills-rewrite.md` | 重构方案文档——25 commit 6 阶段执行计划 |

## 核心架构：单层 Skill 模型

系统采用**单层 Skill 模型**。所有组件默认为 Skill，运行在当前会话，支持多轮交互，Skill 之间可直接调用。Agent 降级为可选优化手段——仅在 Skill 不适合时（>500 行纯文本/需并行/需上下文隔离）使用。

详细规范见 [`interaction-spec.md`](interaction-spec.md) §1.1。

## 与 guides/ 的区别

| 维度 | guides/ | specs/ |
|------|---------|--------|
| 内容类型 | 方法论（怎么做） | 规则（必须怎么做） |
| 受众 | Agent/Skill 的行为逻辑 | 系统架构和组件定义 |
| 强制性 | 参考指导（缺失可降级） | 架构约束（不可违背） |
| 示例 | "心流五维评估方法" | "Skill 必须使用单层模型" |

## 规范的生命周期

1. **草稿**：新规范以 proposal 形式提出，标注 `status: draft`
2. **生效**：经审阅确认后，标注 `status: active`，CLAUDE.md 引用
3. **修订**：架构变更时更新规范，变更记录在文件末尾的修订历史节
4. **废弃**：不再适用的规范标注 `status: deprecated`，保留 30 天后删除
