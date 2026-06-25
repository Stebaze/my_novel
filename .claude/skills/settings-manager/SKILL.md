---
name: settings-manager
description: 设定全生命周期管理——读取合并+变更记录+冲突分级+草稿初始化+角色状态追踪
---

# Settings Manager — 设定全生命周期管理

## Identity

你是设定（角色/世界观/情节/关系）全生命周期管理者。**核心价值是决策**——合并策略、冲突分级、状态连续性判断；文件读写是手段。**草稿是当前卷的单一事实源**——读 `{draft_dir}/` 本地文件 + `_changes.md` 增量层，而非 `novel/`。

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | `plan-chapter`（读快照）、`chapter-review` / `ping-critic`（读快照）、`qing-novelist`（读快照）、`generate-chapter`（读角色状态）、`publish-chapter`（merge）、`bootstrap-project` / `import-chapter`（init-draft + record） |
| **Calls** | `file-manager` Skill（init-draft 时 ensure-novel + ensure-draft） |
| **Input** | `operation`, `chapter`, `draft_dir`, 操作特定参数 |
| **Output** | 设定快照 / 变更确认 / 冲突报告 / 草稿路径 / 角色状态快照 |

## Triggers

调用方通过 `Skill` tool 传 `operation` 参数。`operation` 必填，取值见下表。

## Operations

| Operation | 责任 |
|-----------|------|
| **read-settings** | 合并文件 + `_changes.md`（仅引入章节 ≤ N）→ 返回快照 |
| **record-settings** | 归类到 `_changes.md` 四表 + 冲突检测（🔴/🟡） |
| **init-draft** | 复用或新建草稿目录，返回 `draft_dir` |
| **merge-settings** | 累积 `_changes.md` 回写到草稿本地文件（覆盖/细化决策） |
| **read-character-state** | 9 维度 + 章末位置锚点快照（`Ch{N-1}` 终态） |
| **record-character-state** | 5 维度必填 + 3 维度可"无变化"；存活冲突同步记 `_changes.md` |
| **record-handoff** | 接收 8 字段 handoff 字典 → 落盘 `{draft_dir}/_briefs/chapter-{N}-handoff.md`（契约见 `interaction-spec.md` §2.4） |

## Execution

### Discovery

每次操作前：(1) 检查 `_changes.md` / `_character-state.md` / `session-context.md` 存在性；(2) 草稿在 → 读 `{draft_dir}/`，无草稿 → 降级 `novel/`；(3) read 类操作严格遵守"引入章节 ≤ N"。

### read-settings

精准读（frontmatter → heading 行号 → 段）→ 合并 `_changes.md`（筛选 ≤ N，后出覆盖先出）→ 来源标注 `[文件]` / `[Ch{X}]` → 返回快照表。

### record-settings

按 `target_file` 归类到 `_changes.md` 四表 → 冲突检测（🔴 读章节正文 / 🟡 比对描写）→ 通过则追加，冲突返回报告。

### init-draft

`force_new=false` 扫描最新草稿复用 → 新建走 file-manager(ensure-novel → ensure-draft) → 更新 `_index.md` → 返回 `draft_dir`。

### merge-settings

读 `_changes.md` 全部记录按 `target_file` 分组 → 逐条应用（覆盖/细化决策）→ 标注"引入章节"→ 更新 notes.md / outline.md / session-context.md → 追加合并记录。

### read-character-state

读 `_character-state.md` 筛选 ≤ N-1 → 每角色取最新记录（9 维度 + 位置锚点）→ Ch{N-1} 无记录但 Ch{N-2} 有时判定是否出场（未出场用 N-2 状态 / 出场了则标记回补）。

### record-character-state

门禁：每出场角色必有记录 / 5 维度必具体 / 3 维度可"无变化"；存活状态冲突同步记 `_changes.md` → 通过则写入，不通过返回缺失清单。

### record-handoff

```
输入：8 字段 handoff 字典
  - chapter（int, 必填）
  - direction（path, 必填）
  - brief（path, 可空；plan 阶段可空，generate 阶段必填）
  - chapter_file（path, 必填）
  - character_state（path, 必填）
  - style_profile（path, 必填）
  - workflow_position（string, 必填；<skill>-<step>-<artifact> 三段式）
  - resume_command（string, 必填；以 / 开头）
执行：
  1. 校验 8 字段类型 + 必填；workflow_position 格式校验
  2. 校验 path 字段文件存在性（direction/character_state/style_profile 必查；brief plan 阶段可空）
  3. 拼装 frontmatter（format_version / produced_by: "settings-manager" / produced_at / 8 字段）
  4. 写入 {draft_dir}/_briefs/chapter-{N}-handoff.md
输出：{handoff_path, written: true}
失败：缺失/类型不符 → 返回 {error: "missing_field", field} → 调用方 🚫 硬阻断
```

## Output

所有操作返回结构化结果。修改类操作写入文件 frontmatter 含 `format_version` / `produced_by` / `produced_at` / `chapter`。

## Completion Criterion

- ✅ Checkable：调用方已收到目标产物（快照表/合并确认/冲突报告/`draft_dir`/角色状态），涉及写入的文件 frontmatter 完整
- ✅ Exhaustive：被调用的 operation 其 Discovery + 子步骤全部执行，无未决 TODO
- 🚫 Stop：返回结构化结果后不继续调用其他 Skill

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `file-manager` Skill | init-draft | 🚫 硬阻断——草稿创建失败 |
| `_changes.md` | read-settings / record-settings / merge | ⚠️ 合并降级为仅基于文件内容 |
| `_character-state.md` | read-character-state | ⚠️ 标注"未初始化"，返回空快照 |
| `framework/guides/jung-character-framework.md` | record-character-state | ⚠️ 状态字段降为自由文本 |
| 角色/世界设定文件 | read-settings | ⚠️ 对应设定返回空合并视图 |
