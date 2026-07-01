---
name: settings-manager
description: 设定全生命周期管理——读取合并+变更记录+冲突分级+草稿初始化+角色状态追踪
---

# Settings Manager — 设定全生命周期管理

## Identity

你是设定（角色/世界观/情节/关系）全生命周期管理者。**核心价值是决策**——合并策略、冲突分级、状态连续性判断；文件读写是手段。**双源真相**——正式层 `novel/` 设定文件存当前状态 + 草稿侧 `{draft}/_changes.md` 存未合并增量；`read-settings` 双源合并返回快照。草稿**不镜像**设定文件，无设定副本。

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
| **read-settings** | 双源合并 `novel/` 设定文件 + `{draft}/_changes.md`（筛选未合并且引入章节 ≤ N）→ 返回快照，来源标注 `[文件]` / `[Ch{X}]` |
| **record-settings** | 归类到 `{draft}/_changes.md` 四表 + 冲突检测（🔴/🟡） |
| **init-draft** | 固定路径 `novel/_drafts/`——全书首次调用建空模板+目录，后续章节直接复用 |
| **merge-settings** | 累积 `{draft}/_changes.md` 回写到 `novel/` 设定文件 + `novel/_changes.md` + `novel/_character-state.md`；草稿侧条目打 `merged_at` 标记不清空（append-only 历史日志） |
| **read-character-state** | 双源合并 `novel/_character-state.md`（全部已发布）+ `{draft}/_character-state.md`（已合并+未合并）→ 筛选 ≤ N-1，每角色取最新记录（9 维度 + 位置锚点） |
| **record-character-state** | 5 维度必填 + 3 维度可"无变化"；存活冲突同步记 `{draft}/_changes.md` |
| **record-handoff** | 接收 8 字段 handoff 字典 → 落盘 `{draft_dir}/_briefs/chapter-{N}-handoff.md`（契约见 `interaction-spec.md` §2.4） |

## Execution

### Discovery

每次操作前：(1) 检查 `{draft}/_changes.md` / `{draft}/_character-state.md` / `{draft}/session-context.md` 存在性；(2) 草稿固定路径 `novel/_drafts/`——草稿不存在时调 `file-manager`(ensure-draft) 补齐后再读，**不再降级 `novel/`**（草稿是固定单份，必然存在）；(3) read 类操作严格遵守"引入章节 ≤ N"。

### read-settings

精准读 `novel/` 设定文件（frontmatter → heading 行号 → 段）→ 合并 `{draft}/_changes.md`（筛选 `merged_at` 为空 且 引入章节 ≤ N，后出覆盖先出）→ 来源标注 `[文件]` / `[Ch{X}]` → 返回快照表。

**双源合并顺序**：`novel/` 文件为基线（已合并的当前状态），草稿侧 `_changes.md` 未合并条目叠加其上（同字段后出覆盖先出）。已合并条目（`merged_at` 非空）跳过——其效果已体现在 `novel/` 文件中。

### record-settings

按 `target_file` 归类到 `{draft}/_changes.md` 四表 → 冲突检测（🔴 读章节正文 / 🟡 比对描写）→ 通过则追加，冲突返回报告。

### init-draft

`draft_dir` 固定为 `novel/_drafts/`：

```
1. 检查 novel/_drafts/ 存在性
   - 不存在 → 调 file-manager(ensure-novel → ensure-draft) 建空模板+目录
   - 存在 → 直接复用（单草稿贯穿全书，无 _index.md 维护）
2. 返回 draft_dir = "novel/_drafts/"
```

**无 force_new 参数**——单草稿约束下不存在"新建另一份草稿"语义。全书首次调用建骨架，后续章节直接复用同一份草稿。

### merge-settings

回写目标从"草稿本地文件"改为 `novel/` 正式层。支持两种模式：

**直接模式**（默认，独立调用）：直接写 `novel/` + 草稿侧打标记。
**暂存模式**（`staging=true`，由 publish-chapter 调用）：产出落 `{draft}/_publish-staging/`，不写正式层——由 publish-chapter 提交阶段执行实际写入。

```
1. 读 {draft}/_changes.md 全部记录按 target_file 分组
2. 逐条应用（覆盖/细化决策）→ 标注"引入章节"
3. 直接模式：写入 novel/ 对应设定文件 + 追加 novel/_changes.md + novel/_character-state.md 条目
   暂存模式：产出落 {draft}/_publish-staging/：
     - settings-diff.md（novel/ 设定文件待 apply diff）
     - changes-to-append.md（novel/_changes.md 待追加条目）
     - character-state-to-append.md（novel/_character-state.md 待追加条目）
     - draft-merged-at.md（草稿侧待打 merged_at 标记条目清单）
4. 草稿侧 {draft}/_changes.md / {draft}/_character-state.md 对应条目打 merged_at 标记（不清空，append-only 历史日志）
   - 直接模式：步骤 3 写 novel/ 成功后立即打标记
   - 暂存模式：由 publish-chapter 提交阶段执行打标记（步骤 5）
5. 更新 {draft}/notes.md / {draft}/session-context.md
```

**merge 顺序约束**（直接模式）：先写 `novel/`（步骤 3），成功后再给草稿侧打 `merged_at` 标记（步骤 4）。崩溃恢复时扫描 `novel/_changes.md` 末尾条目是否在草稿侧已打标记，未打则补打（自愈）。

**暂存模式崩溃恢复**：暂存产出落 `_publish-staging/`，正式层零影响；publish-chapter 提交阶段失败时保留 staging，下次 publish 检测残留提示继续/回滚。

### read-character-state

双源合并：
1. 读 `novel/_character-state.md`（全部已发布条目，即正式层角色状态时间线）
2. 合并 `{draft}/_character-state.md`（已合并 + 未合并条目）
3. 筛选章节 ≤ N-1 → 每角色取最新记录（9 维度 + 位置锚点）
4. Ch{N-1} 无记录但 Ch{N-2} 有时判定是否出场（未出场用 N-2 状态 / 出场了则标记回补）

### record-character-state

门禁：每出场角色必有记录 / 5 维度必具体 / 3 维度可"无变化"；存活状态冲突同步记 `{draft}/_changes.md` → 通过则写入 `{draft}/_character-state.md`，不通过返回缺失清单。

### record-handoff

```
输入：12 字段 handoff 字典（v2.0，5 维正交风格档案）
  - chapter（int, 必填）
  - direction（path, 必填）
  - brief（path, 可空；plan 阶段可空，generate 阶段必填）
  - chapter_file（path, 必填）
  - character_state（path, 必填）
  - style_profile_type（string, 必填 1 个——基底；对应 framework/templates/_style-bases/{type}.md）
  - style_profile_themes（list[string], 必填 1-N 个——主题叠加；每个对应 framework/templates/_themes/{theme}.md）
  - style_profile_variant（string, 可选 0-1 个——作家风格；对应 framework/templates/_styles/{variant}.md）
  - style_profile_subvariant（string, 可选 0-1 个——子变体；嵌入在 {variant} 风格层文件中）
  - style_profile_specialization（string, 可选 0-1 个——题材特化；对应 framework/templates/_style-bases/specializations/{specialization}.md）
  - workflow_position（string, 必填；<skill>-<step>-<artifact> 三段式）
  - resume_command（string, 必填；以 / 开头）
执行：
  1. 校验 12 字段类型 + 必填；workflow_position 格式校验
     - **必填字段**（缺/None 即报缺失）：chapter / direction / chapter_file / character_state / style_profile_type / style_profile_themes
     - **必填但允许空字符串**：style_profile_variant（variant 字段为空=走 fallback 风格层；不为空时必须对应文件存在）
     - **可选字段**（空字符串=合法）：style_profile_subvariant / style_profile_specialization
     - 空集合判定：空 list [] = 缺失；非空 list 合法
  2. 校验 path 字段文件存在性：
     - direction/character_state 必查
     - brief plan 阶段可空，generate 阶段必查
     - style_profile_type 必查（对应 _style-bases/{type}.md）
     - style_profile_themes 任一必查（对应 _themes/{theme}.md）
     - style_profile_variant 如非空必查（对应 _styles/{variant}.md）
     - style_profile_subvariant 如非空必查（嵌入在 {variant} 风格层文件——可省略具体路径校验）
     - style_profile_specialization 如非空必查（对应 _style-bases/specializations/{specialization}.md）
  3. 拼装 frontmatter（format_version: "2.0" / produced_by: "settings-manager" / produced_at / 12 字段）
  4. 写入 {draft_dir}/_briefs/chapter-{N}-handoff.md
输出：{handoff_path, written: true}
失败：缺失/类型不符 → 返回 {error: "missing_field", field} → 调用方 🚫 硬阻断

## 5 维降级规则（2026-07-01 修复）

3 维档案重构（v2.0）后，部分字段从"必填"改为"可选"。降级规则：

| 字段 | 必填？ | 空字符串=合法？ | 缺/None=报缺失？ |
|------|:---:|:---:|:---:|
| chapter | ✅ | — | ✅ |
| direction | ✅ | — | ✅ |
| chapter_file | ✅ | — | ✅ |
| character_state | ✅ | — | ✅ |
| style_profile_type | ✅ | — | ✅ |
| style_profile_themes | ✅（非空 list）| — | ✅ |
| style_profile_variant | ✅（非空时对应文件必须存在）| ✅ | ❌ |
| style_profile_subvariant | ❌ | ✅ | ❌ |
| style_profile_specialization | ❌ | ✅ | ❌ |
| workflow_position | ✅ | — | ✅ |
| resume_command | ✅ | — | ✅ |

> **修复历史**：v1.0 spec 把 `style_profile_subvariant` 标"必填（空字符串=缺失）"，与 3 维档案重构（无子变体）冲突。
> 2026-07-01 验证 Ch2 时 record-handoff 写入 3 维档案（subvariant=""），按 v1.0 应报缺失，但 C8 接受空 subvariant。
> 修复：统一为 subvariant/specialization 都为可选，与 C8 行为一致。

### variant 字段空字符串的语义

```
style_profile_variant = "" 时：
├── 不检查 _styles/{variant}.md（variant 为空无对应文件）
├── record-handoff 写入空 variant（合法）
├── C8 接受空 variant
├── generate-chapter Step 2 加载风格层时：
│   ├── 退化到 framework/templates/_styles/{variant-fallback}.md
│   │   （fallback 风格层由 project-config.md「风格」字段提供，例：kuiguannan-style-fallback-v3）
│   └── 5 维评审基线 chapter-review Step 2.7c 走 fallback 默认
└── 与 C3 联动：project-config.md 作家="" → C3 走条件性降级（不要求 author-voice.md）
```

> 此降级路径与 C8 spec 一致——C8 spec 同样接受空 variant 但要求"非空时文件存在"。
```

## Output

所有操作返回结构化结果。修改类操作写入文件 frontmatter 含 `format_version` / `produced_by` / `produced_at` / `chapter`。`merge-settings` 写入 `novel/` 时附加 `merged_at` 时间戳；草稿侧打 `merged_at` 标记保留历史。

## Completion Criterion

- ✅ Checkable：调用方已收到目标产物（快照表/合并确认/冲突报告/`draft_dir`/角色状态），涉及写入的文件 frontmatter 完整
- ✅ Exhaustive：被调用的 operation 其 Discovery + 子步骤全部执行，无未决 TODO
- 🚫 Stop：返回结构化结果后不继续调用其他 Skill

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `file-manager` Skill | init-draft | 🚫 硬阻断——草稿创建失败 |
| `{draft}/_changes.md` | read-settings / record-settings / merge | ⚠️ 合并降级为仅基于 `novel/` 文件内容 |
| `{draft}/_character-state.md` | read-character-state | ⚠️ 标注"未初始化"，返回空快照（仅 `novel/_character-state.md` 已发布部分）|
| `novel/_character-state.md` | read-character-state | ⚠️ 已发布角色状态缺失，仅返回草稿侧增量 |
| `framework/guides/jung-character-framework.md` | record-character-state | ⚠️ 状态字段降为自由文本 |
| `novel/` 角色档案 / 世界设定文件 | read-settings | ⚠️ 对应设定返回空合并视图（草稿无副本兜底） |
