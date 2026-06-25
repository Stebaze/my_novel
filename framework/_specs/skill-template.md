# Skill 标准结构

> 适用：Claude Code `.claude/skills/<name>/SKILL.md`
> Skill = 注入当前会话，可多轮交互，随主对话被压缩。所有组件默认为 Skill。

## 5 必含字段

| Field | Purpose |
|-------|---------|
| **Identity** | 2-3 句定位 + 编排/工具职责 |
| **Contract** | Calls / Produces / Called by / Input / Output（取子集） |
| **Flow** | 步骤序列（orchestrator）或 Operation 切换（tool） |
| **Triggers** | 用户触发词（orchestrator）或调用方 Skill（tool） |
| **Completion Criterion** | checkable + exhaustive 判据（动词开头）——完成即停 |

## 模板：编排型 Skill（用户入口，编排其他 Skill）

```markdown
---
name: <kebab-case>
description: <一句话目的>
---

# <Title>

## Identity

[2-3 句：Skill 定位 + 编排职责。]

## Contract

| Aspect | Detail |
|--------|--------|
| **Calls** | [调用的 Skill 列表] |
| **Produces** | [产出的文件] |

## Triggers

- "触发词1" / "触发词2"

## Flow

### Step 1: Resolve Context

[确定章节号、草稿目录等上下文参数]

### Step 2: Check Artifacts → Route

[检查磁盘产物 → 定位当前进度 → 决定调用哪个 Skill]

### Step 3: Execute

[调用目标 Skill 或直接执行操作]

### Step 4: Present

[呈现结果 + 下一步提示]

## Completion Criterion

- ✅ Checkable：调用方已收到 {N} 章的 {方向卡 | handoff | 简报 | 章节文件 | 评审报告}，且磁盘存在对应文件
- ✅ Exhaustive：所有 Flow 步骤执行完毕，下一步提示已呈现
- 🚫 Stop：不进入下一 Skill 调用
```

## 模板：工具型 Skill（被其他 Skill 调用）

```markdown
---
name: <kebab-case>
description: <一句话目的>
---

# <Title>

## Identity

[2-3 句：Skill 定位 + 有人格者在此处建立人格。]

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | [哪些 Skill 调用此 Skill] |
| **Calls** | [调用的其他 Skill（如有）] |
| **Input** | [接收的数据/参数] |
| **Output** | [产出的文件/结果] |

## Triggers

- 调用方 Skill 通过 `Skill` tool 传入参数

## Operations

> 多模式 Skill 用 `operation` 参数切换。单一模式可省略。

| Operation | Trigger | Responsibility |
|-----------|---------|---------------|
| ... | `operation="{name}"` | ... |

## Execution

### Discovery

[检查已有产物 → 确定需要做什么。断点续传的基础。]

### Operation: <name>

[该操作下的完整执行步骤。]

## Output

[产出的文件格式 + frontmatter 版本标记要求]

## Completion Criterion

- ✅ Checkable：磁盘已写入 {output_file}，frontmatter 含 `format_version` / `produced_by` / `produced_at` / `chapter`
- ✅ Exhaustive：所有 Operation 子步骤执行完毕，无未决 TODO
- 🚫 Stop：返回结构化结果到调用方，不继续执行后续流程

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `path/to/file.md` | [何时需要] | [🚫硬阻断 / ⚠️降级行为] |
| `other-skill` | [何时调用] | [缺失时行为] |

> 降级等级：🚫 硬阻断（不能继续）/ ⚠️ 降级（标注影响后继续）
> **强制规则**：Skill 调用失败必须 🚫 硬阻断，禁止 ⚠️ 降级后继续。仅文件/Guide 缺失可选 ⚠️。
```

## 写法规则

1. **编排型 = 薄入口**——只做确定上下文 + 检查产物 + 编排调用 + 呈现结果。
2. **工具型 = 确定性工具**——被调用，执行算法/规则/文件操作，返回结构化结果。
3. **防压缩**——核心原则放 Skill 定义；详细方法论外移到 `framework/guides/`；阶段性状态写磁盘。
4. **产出走模板**——核心产出格式在 `framework/templates/` 中，Skill 通过读模板获取格式。
5. **≤ 200 行**——超过则外移方法论。
6. **Contract 必须清晰**——调用方不读实现即知用法。
7. **Discovery 阶段必须**——检查产物文件存在性，支持断点续传。
8. **降级不静默**——每个缺失依赖有明确降级行为；Skill 调用失败 🚫 硬阻断。
9. **Skill 可调 Skill**——通过 `Skill` tool 直接调用。
10. **Completion Criterion 用 checkable + exhaustive 措辞**——动词开头（写入/返回/呈现），完成判据（磁盘文件 + frontmatter），禁止"差不多了/应该好了"等模糊用词。
