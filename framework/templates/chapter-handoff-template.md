---
format_version: "1.0"
produced_by: "settings-manager"（被 plan-chapter 阶段 5 调用落盘）
produced_at: "{ISO 8601 timestamp}"
chapter: {N}
direction: "_briefs/chapter-{N}-direction.md"
brief: "_briefs/chapter-{N}-brief.md"  # plan 阶段可空
chapter_file: "chapters/chapter-{N}.md"
character_state: "_character-state.md"
style_profile: "author-voice.md"
workflow_position: "plan-step5-handoff"
resume_command: "/generate-chapter {N}"
---

# 章节 Handoff — Ch{N}

> **用途**：plan-chapter 阶段 5 落盘 → generate-chapter Session 2 入口硬检查（pre-flight-check C8）→ 跨 Session 状态交接。所有章节统一走 4-Skill 对称架构。
>
> **契约定义**：`framework/_specs/interaction-spec.md` §2.4
> **生成方式**：由 `settings-manager` Skill (`record-handoff` operation) 自动落盘。本文件为手动修复/复制时的模板。
> **字段类型**：path 字段值以 `{draft_dir}` 为根的相对路径。

## 字段契约（8 字段）

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `chapter` | int | ✅ | 章节号 N（与文件名一致） |
| `direction` | path | ✅ | 方向卡文件路径（`_briefs/chapter-{N}-direction.md`） |
| `brief` | path | 🟡 | 简报路径（plan 阶段可空；generate 阶段必填） |
| `chapter_file` | path | ✅ | 目标章节文件路径（`chapters/chapter-{N}.md`） |
| `character_state` | path | ✅ | 角色状态快照（`{draft_dir}/_character-state.md`） |
| `style_profile` | path | ✅ | 作者文风档案（`{draft_dir}/author-voice.md`） |
| `workflow_position` | string | ✅ | `<skill>-<step>-<artifact>` 三段式（例：`plan-step5-handoff`） |
| `resume_command` | string | ✅ | 新 Session 启动命令（`/generate-chapter {N}` 或 `/chapter-review {N}`） |

## workflow_position 取值

| 取值 | 含义 | 续跑命令 |
|------|------|----------|
| `plan-step5-handoff` | plan 阶段完成，handoff 已写 | `/generate-chapter {N}` |
| `generate-step1-brief` | 简报已生成 | `/generate-chapter {N} --resume` |
| `generate-step2-scenes` | 场景已生成 + 拼装完成 | `/generate-chapter {N} --resume` |
| `generate-step3-reviewed` | 自动评审完成 | `/generate-chapter {N} --resume` |
| `generate-step4-fix1` | Fix Round 1 完成 | `/generate-chapter {N} --resume` |
| `generate-step4-fix2` | Fix Round 2 完成 | `/generate-chapter {N} --resume` |
| `generate-step5-done` | 全部完成 | `/chapter-review {N}` |

## 验证规则（pre-flight-check C8 执行）

- `chapter` 缺失或值 ≠ N → 🚫
- `direction` 缺失或文件不存在 → 🚫
- `chapter_file` 缺失或路径不以 `chapters/` 开头 → 🚫
- `character_state` 缺失或文件不存在 → 🚫
- `style_profile` 缺失或文件不存在 → 🚫
- `workflow_position` 缺失或格式不符 → 🚫
- `resume_command` 缺失或格式不符（不以 `/` 开头）→ 🚫
- `brief` 条件：`workflow_position` 前缀为 `generate-*` 时必填，否则可选
- 任一 🚫 → 修复路径："调 plan-chapter {N} 重跑阶段 5"或复制本模板填写

## 修复路径

1. **推荐**：调 `plan-chapter {N}` 重跑阶段 5（settings-manager record-handoff）— 自动重写
2. **手动**：复制本模板 → 填写 8 字段 → 保存到 `{draft_dir}/_briefs/chapter-{N}-handoff.md`
3. **检查点**：完成后再跑一次 pre-flight-check C8 验证

## 示例（已落盘 handoff 的最小有效结构）

```yaml
---
format_version: "1.0"
produced_by: "settings-manager"
produced_at: "2026-06-24T18:30:00+08:00"
chapter: 47
direction: "_briefs/chapter-47-direction.md"
brief: ""  # plan 阶段可空
chapter_file: "chapters/chapter-47.md"
character_state: "_character-state.md"
style_profile: "author-voice.md"
workflow_position: "plan-step5-handoff"
resume_command: "/generate-chapter 47"
---
```
