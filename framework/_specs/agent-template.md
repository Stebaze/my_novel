# Agent 标准结构

> **Agent 是可选优化手段，不是默认架构组件。**
> 适用：Claude Code `.claude/agents/<name>.md`
> Agent = 独立子会话，一次性执行，上下文隔离。不能中途与用户交互。

## 何时使用 Agent

仅在以下条件满足时使用：

1. **执行逻辑 > 500 行纯文本**——Skill 中加载会严重占用上下文窗口
2. **需要并行独立执行**——多个互不依赖的子任务需要同时运行
3. **需要完全上下文隔离**——如处理不可信输入、实验性代码

**默认选择是 Skill**——支持多轮交互，运行在当前会话中。详细规范见 [`interaction-spec.md`](interaction-spec.md) §1.1。

## 必含字段

| Field | Purpose |
|-------|---------|
| **Identity** | 2-3 句定位 + 核心职责 |
| **Contract** | Input / Output / Called by |
| **Execution** | Discovery + Steps 序列（Agent 一次性执行，不中途等待用户输入）|
| **Completion Criterion** | checkable + exhaustive 判据（动词开头）——完成即停 |
| **Dependencies** | 缺失依赖 + 降级行为（🚫 / ⚠️） |

## 模板

```markdown
---
name: <kebab-case>
description: <一句话目的>
tools: Read, Write, Edit, Bash, Grep, Glob
permissionMode: bypassPermissions
---

# <Title>

## Identity

[2-3 句：角色定位 + 核心职责。]

## Contract

| Aspect | Detail |
|--------|--------|
| **Input** | [接收的参数 + 文件路径] |
| **Output** | [产出的文件路径 + 决策结果] |
| **Called by** | [哪个 Skill 分派此 Agent] |

## Execution

### Discovery

[检查已有产物 → 确定需要做什么。断点续传的基础。]

### Steps

[完整执行步骤。Agent 一次性执行完毕，不中途等待用户输入。]

## Output

[产出的文件格式 + frontmatter 版本标记要求]

## Completion Criterion

- ✅ Checkable：磁盘已写入 {output_file}，frontmatter 含 `format_version` / `produced_by` / `produced_at` / `chapter`
- ✅ Exhaustive：所有 Execution 步骤执行完毕，无未决 TODO
- 🚫 Stop：返回结构化结果到调用方，不继续执行后续流程

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `path/to/file.md` | [何时需要] | [🚫硬阻断 / ⚠️降级行为] |
| `other-skill` | [何时调用] | [缺失时行为] |

> 降级等级：🚫 硬阻断（不能继续）/ ⚠️ 降级（标注影响后继续）
> **强制规则**：Skill/Agent 调用失败必须 🚫 硬阻断，禁止 ⚠️ 降级后继续。仅文件/Guide 缺失可根据严重性选择 ⚠️。
```

## 写法规则

1. **Agent 是例外，不是默认**——优先 Skill；只有 Skill 不适合（上下文过大/需并行/需隔离）时才用 Agent
2. **≤ 200 行**——超过则把详细方法论外移到 `framework/guides/`
3. **Contract 必须清晰**——调用方不读实现即知用法
4. **Discovery 阶段必须**——检查产物文件存在性，支持断点续传
5. **Completion Criterion 用 checkable + exhaustive 措辞**——动词开头，完成判据（磁盘文件 + frontmatter），禁止模糊用词
6. **降级不静默**——每个缺失依赖有明确降级行为描述
7. **产出格式走模板**——核心产出格式在 `framework/templates/` 中，通过读模板获取，不内联结构定义
