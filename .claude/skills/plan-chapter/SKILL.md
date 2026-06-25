---
name: plan-chapter
description: 章节规划——系统管道(前置检查+设定快照)+启发式交谈+方向卡产出；阶段 5 写 handoff 切出到 generate-chapter Session 2
---

# Plan Chapter — 章节规划编排

## Identity

你是章节规划的编排入口。你负责系统管道（前置就绪检查、设定快照、草稿初始化），分派到 `qing-novelist` 做启发式交谈，最后在阶段 5 写 handoff 切出到 generate-chapter Session 2。**不做创意判断**——只管管道和分派。

## Contract

| Aspect | Detail |
|--------|--------|
| **Calls** | `pre-flight-check`, `settings-manager`（read-settings / init-draft / read-character-state / record-handoff）, `idea-explorer`（条件·阶段 3）, `qing-novelist`（阶段 4） |
| **Produces** | `_briefs/chapter-{N}-direction.md`（阶段 4 必）/ `_briefs/chapter-{N}-handoff.md`（阶段 5 必）/ `_briefs/chapter-{N}-exploration.md`（阶段 3 条件） |

## Triggers

- "写第X章" / "规划第X章" / "准备写第X章"
- "续写" / "继续写" / "下一章"
- "重写第X章"（规划阶段）

## Flow

### 6-Stage Pipeline

```
阶段 0: Pre-Flight        → 解析上下文 + pre-flight-check C0-C7.5 + 工件路由
阶段 1: Settings Snapshot → settings-manager read-settings + read-character-state
阶段 2: Init Draft        → settings-manager init-draft（按需）
阶段 3: [条件] Brainstorm → idea-explorer（无方向时激活）
阶段 4: Heuristic Conv.   → qing-novelist（方向卡产出）
阶段 5: Handoff          → settings-manager record-handoff + Present
```

各阶段详细动作见 [`_stages/{N}-{name}.md`](_stages/)。

### 阶段 0 工件路由规则

```
所有章节统一走 4-Skill 对称架构：
  阶段 5 → settings-manager (record-handoff) 落盘 handoff
  → 提示用户开新会话输入 /generate-chapter {N}
  → 退出
```

### Handoff 8 字段契约

`{draft_dir}/_briefs/chapter-{N}-handoff.md` frontmatter 必含 8 字段。完整定义见 `framework/_specs/interaction-spec.md` §2.4：

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `chapter` | int | ✅ | 章节号 N |
| `direction` | path | ✅ | 方向卡路径（相对 `{draft_dir}`） |
| `brief` | path | 🟡 | 简报路径；planning 阶段可空，generate 阶段必填 |
| `chapter_file` | path | ✅ | `chapters/chapter-{N}.md` |
| `character_state` | path | ✅ | `{draft_dir}/_character-state.md` |
| `style_profile` | path | ✅ | `{draft_dir}/author-voice.md` |
| `workflow_position` | string | ✅ | `<skill>-<step>-<artifact>` 三段式 |
| `resume_command` | string | ✅ | `/generate-chapter {N}` |

`path` 字段以 `{draft_dir}` 为根的相对路径。

## Completion Criterion

- ✅ Checkable：返回阶段进度字典 `{stage: 0|1|2|3|4|5, 状态: done/skipped, 产出物: [...路径]}`
- ✅ Exhaustive：6 阶段全部执行（含条件项 skip），handoff 落盘
- 🚫 Stop：阶段 5 Present 提示用户开新会话后退出——不进入生成

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `pre-flight-check` Skill | 阶段 0 | 🚫 硬阻断 |
| `settings-manager` Skill | 阶段 1 / 阶段 5 | 🚫 硬阻断——设定快照 + record-handoff 不可跳过 |
| `idea-explorer` Skill | 阶段 3 | ⚠️ 不可用时跳过阶段 3，标注"思源不可用" |
| `qing-novelist` Skill | 阶段 4 | 🚫 硬阻断——方向卡必须产出 |
| `framework/_specs/interaction-spec.md` §2.4 | 阶段 5 | 🚫 硬阻断——handoff 8 字段契约定义缺失则无法写 handoff |
| `framework/templates/chapter-handoff-template.md` | 阶段 5 | 🚫 硬阻断——handoff 模板缺失则字段契约不明确 |
| `{draft_dir}/_briefs/chapter-{N}-direction.md` | 阶段 5 | 🚫 硬阻断——方向卡缺失则无法写 handoff |
