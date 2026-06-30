---
format_version: "2.0"
produced_by: "settings-manager"（被 plan-chapter 阶段 5 调用落盘）
produced_at: "{ISO 8601 timestamp}"
chapter: {N}
direction: "_briefs/chapter-{N}-direction.md"
brief: "_briefs/chapter-{N}-brief.md"  # plan 阶段可空
chapter_file: "chapters/chapter-{N}-md"
character_state: "_character-state.md"
# 5 维正交风格档案（替代 v1.0 的单 style_profile 字段——breaking change）
# 注：字段值=文件物理名（无 v 后缀）；版本号保留在文件 frontmatter profile_id
style_profile_type: "japanese-light-novel-base"  # 必填 1 个：基底 (japanese-light-novel-base / chinese-webnovel-base)
style_profile_themes:  # 必填 1-N 个：主题叠加（theme-daily-life/romance/mystery/scifi-fantasy/doomsday/system/ensemble/cross-time）
  - "daily-life"
  - "romance"
style_profile_variant: "kuiguannan-style"  # 可选 0-1 个：作家风格 (kuiguannan/amamorin/shiniki/yuantong/fengyue/buluofeng-style)
style_profile_subvariant: "biyang-conference"  # 可选 0-1 个：子变体
style_profile_specialization: "translation-ja"  # 可选 0-1 个：题材特化
workflow_position: "plan-step5-handoff"
resume_command: "/generate-chapter {N}"
---

# 章节 Handoff — Ch{N}

> **用途**：plan-chapter 阶段 5 落盘 → generate-chapter Session 2 入口硬检查（pre-flight-check C8）→ 跨 Session 状态交接。所有章节统一走 4-Skill 对称架构。
>
> **契约定义**：`framework/_specs/interaction-spec.md` §2.4
> **生成方式**：由 `settings-manager` Skill (`record-handoff` operation) 自动落盘。本文件为手动修复/复制时的模板。
> **字段类型**：path 字段值以 `{draft_dir}` 为根的相对路径。

## 字段契约（12 字段，v2.0）

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `chapter` | int | ✅ | 章节号 N（与文件名一致） |
| `direction` | path | ✅ | 方向卡文件路径（`_briefs/chapter-{N}-direction.md`） |
| `brief` | path | 🟡 | 简报路径（plan 阶段可空；generate 阶段必填） |
| `chapter_file` | path | ✅ | 目标章节文件路径（`chapters/chapter-{N}.md`） |
| `character_state` | path | ✅ | 角色状态快照（`{draft_dir}/_character-state.md`） |
| `style_profile_type` | string | ✅ | 基底（必填 1 个）——`framework/templates/_style-bases/` 下的基底文件 ID |
| `style_profile_themes` | list[string] | ✅ | 主题叠加（必填 1-N 个）——`framework/templates/_themes/` 下的主题族文件 ID |
| `style_profile_variant` | string | 🟡 | 作家风格（可选 0-1 个）——`framework/templates/_styles/` 下的风格层文件 ID |
| `style_profile_subvariant` | string | 🟡 | 子变体（可选 0-1 个）——嵌入风格层文件中 |
| `style_profile_specialization` | string | 🟡 | 题材特化（可选 0-1 个）——`framework/templates/_style-bases/specializations/` 下 |
| `workflow_position` | string | ✅ | `<skill>-<step>-<artifact>` 三段式（例：`plan-step5-handoff`） |
| `resume_command` | string | ✅ | 新 Session 启动命令（`/generate-chapter {N}` 或 `/chapter-review {N}`） |

### 5 维正交加载路径

```
基底：framework/templates/_style-bases/{style_profile_type}.md
主题：framework/templates/_themes/{style_profile_theme}.md（多主题叠加）
风格：framework/templates/_styles/{style_profile_variant}.md
子变体：嵌入 {style_profile_variant} 风格层文件中
题材特化：framework/templates/_style-bases/specializations/{style_profile_specialization}.md
```

5 维完全独立可叠加——4 个 Skill 按 5 维字段组合消费对应文件。**字段值=文件物理名（无 v 后缀）**——v 后缀仅作为文件 frontmatter profile_id 标识版本。

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
- `style_profile_type` 缺失或对应 `_style-bases/` 文件不存在 → 🚫
- `style_profile_themes` 缺失（空列表）或任一对应 `_themes/` 文件不存在 → 🚫
- `style_profile_variant` 如非空但对应 `_styles/` 文件不存在 → 🚫
- `style_profile_subvariant` 如非空但对应子变体文件不存在 → 🚫
- `style_profile_specialization` 如非空但对应文件不存在 → 🚫
- `workflow_position` 缺失或格式不符 → 🚫
- `resume_command` 缺失或格式不符（不以 `/` 开头）→ 🚫
- `brief` 条件：`workflow_position` 前缀为 `generate-*` 时必填，否则可选
- 任一 🚫 → 修复路径："调 plan-chapter {N} 重跑阶段 5"或复制本模板填写

## 修复路径

1. **推荐**：调 `plan-chapter {N}` 重跑阶段 5（settings-manager record-handoff）— 自动重写
2. **手动**：复制本模板 → 填写 12 字段 → 保存到 `{draft_dir}/_briefs/chapter-{N}-handoff.md`
3. **5 维字段参考**：
   - `style_profile_type` 选自 `framework/templates/_style-bases/japanese-light-novel-base.md` 或 `chinese-webnovel-base.md` 的 profile_id
   - `style_profile_themes` 选自 `framework/templates/_themes/` 下 8 个主题族文件
   - `style_profile_variant` 选自 `framework/templates/_styles/` 下 6 个作家风格层文件
   - `style_profile_subvariant` 选自风格层文件中的子变体
4. **检查点**：完成后再跑一次 pre-flight-check C8 验证

## 示例（已落盘 handoff 的最小有效结构）

```yaml
---
format_version: "2.0"
produced_by: "settings-manager"
produced_at: "2026-06-30T19:00:00+08:00"
chapter: 47
direction: "_briefs/chapter-47-direction.md"
brief: ""  # plan 阶段可空
chapter_file: "chapters/chapter-47.md"
character_state: "_character-state.md"
# 5 维正交风格档案（v2.0）——字段值=文件物理名（无 v 后缀）
style_profile_type: "japanese-light-novel-base"
style_profile_themes:
  - "daily-life"
  - "romance"
style_profile_variant: "kuiguannan-style"
style_profile_subvariant: "biyang-conference"
style_profile_specialization: ""  # 可选
workflow_position: "plan-step5-handoff"
resume_command: "/generate-chapter 47"
---
```
