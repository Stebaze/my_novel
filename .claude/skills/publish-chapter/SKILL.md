---
name: publish-chapter
description: 正式稿发布——两阶段暂存-提交 merge+章节sync+工件归档+琉璃校验
---

# Publish Chapter — 正式稿发布

## Identity

你是章节发布执行者——当用户告知章节已发布到平台，需要将草稿中的写作成果"提升"为正式层 `novel/chapters/`。你管同步（草稿→正式层）不管写作。**正式层 = 机械写入目标**；发布是两阶段暂存-提交的原子合并。

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | 用户（"第X章已发布" / "发布第X章"） |
| **Calls** | `settings-manager`（merge-settings）, `ping-critic`（publish-verify） |
| **Input** | `chapter`（N）, `draft_dir` |
| **Output** | `{merged_settings, chapter_synced, archived, verification_passed}` |

## Triggers

- "第X章已发布" / "发布第X章" / "把这章发布到正式稿"

## Flow

### Step 1: Resolve Context

```
1. 检查 novel/_drafts/ 固定路径存在性 → draft_dir = novel/_drafts/；不存在 → 🚫 硬阻断
2. 读取 {draft_dir}/notes.md「当前进度」→ 确认 N 在「上次写到」范围内
3. 读取 novel/project-config.md → 取 output_format（project-config 在正式层，草稿不镜像）
4. 三重校验：草稿 chapter-{N}.md 存在 / 与 novel/chapters/ 最后一章连续 / 通过琉璃综合评审
5. 残留暂存检测：{draft}/_publish-staging/ 非空 → 提示"上次 publish 未完成，继续提交 / 回滚"二选一
```

### Step 2: Merge Settings（暂存阶段）

```
调 Skill("settings-manager", operation="merge-settings")
  输入：draft_dir, chapter=N
  → 累积 {draft}/_changes.md 回写：
    暂存阶段产出（落 {draft}/_publish-staging/）：
      - settings-diff.md：novel/ 设定文件待 apply 的 diff
      - changes-to-append.md：novel/_changes.md 待追加条目
      - character-state-to-append.md：novel/_character-state.md 待追加条目
      - draft-merged-at.md：草稿侧 _changes.md / _character-state.md 待打 merged_at 标记的条目清单
  → 失败 → 删 _publish-staging/，正式层零影响；返回 🚫 硬阻断
```

merge-settings 内部顺序约束：先准备 novel/ 写入内容（暂存），不立即写正式层。

### Step 3: Sync Draft → Formal（提交阶段）

**两阶段提交**——暂存区就绪后，依次执行正式层写入 + 草稿清理：

```
提交阶段（原子序列，任一步失败保留 staging 等下次续传）：
  1. mv {draft}/_publish-staging/chapter-{N}.md → novel/chapters/chapter-{N}.md
     （章节正文按 output_format 提取：prose 跳注释块 / script 提取剧本段）
     标题下添加发布元数据：> 发布：YYYY-MM-DD | 平台：XXX | 状态：⭐ 已发布
     重算 word_count（output_format 提取后正文可能变化，以正式层落盘版本为准重测，口径=中文+中文标点，见 interaction-spec §2.2），同步更新 frontmatter `word_count` + `## 元数据 → **实测字数**`
  2. apply settings-diff.md → 更新 novel/ 设定文件（characters/{name}.md / world/*.md / outline.md 等）
  3. 追加 novel/_changes.md 条目（含 merged_at 时间戳）
  4. 追加 novel/_character-state.md 条目（角色状态时间线）
  5. 草稿侧 {draft}/_changes.md / {draft}/_character-state.md 对应条目打 merged_at 标记（不清空，append-only）
  6. 草稿章节正文删除：rm {draft}/chapters/chapter-{N}.md（不双写）
  7. 工件归档：mv 伴生工件 + _edit-history.md → {draft}/_archive/chapter-{N}/
     归档清单：
       - {draft}/_briefs/chapter-{N}-*（direction / handoff / brief / exploration）
       - {draft}/_exchanges/scene-summaries 相关（chapter-{N} 的 scene-summaries.json 片段 / call-params / agent-result）
       - {draft}/_reviews/chapter-{N}-*（review / fix-log）
       - {draft}/_edit-history.md（chapter-{N} 的编辑记录段）
  8. 清空 _publish-staging/
```

**提交失败恢复**：保留 `_publish-staging/`，下次 publish Step 1 检测残留 → 提示继续/回滚。崩溃恢复扫描 `novel/_changes.md` 末尾条目是否在草稿侧已打 `merged_at`，未打则补打（自愈）。

**草稿清理语义**：草稿章节正文删除（不双写），仅归档工件——"草稿保留"指草稿层持续存在可写下一章，**不是**保留已发布章节正文。

### Step 4: Publish-Verify

```
调 Skill("ping-critic", operation="publish-verify")
  → 一致性 / 设定覆盖 / EDIT_HINTS 残留 / 归档完整性 / 正式层 mtime 一致性（C11）校验
  失败 → ⚠️ 警告用户（不阻断发布，但需用户决定是否撤回）
```

### Step 5: Mark Status

```
novel/chapters/chapter-{N}.md  ← 已含发布元数据（Step 3.1 已写）
novel/notes.md                 ← "上次发布：Ch{N}" + 决策表追加
novel/outline.md               ← 章节状态 → ⭐
{draft}/session-context.md     ← 工作流状态更新（已发布 Ch{N}，下一章待规划）
{draft}/notes.md               ← 草稿层进度更新
```

## Completion Criterion

- ✅ Checkable：返回 `{merged_settings: true, chapter_synced: path, archived: [工件清单], verification_passed: bool}`，正式层 `novel/chapters/chapter-{N}.md` 已写入，草稿章节正文已删除，工件已归档到 `{draft}/_archive/chapter-{N}/`
- ✅ Exhaustive：5 步全部执行（merge 暂存→提交 sync→verify→mark→草稿清理归档）
- 🚫 Stop：返回结构化结果到用户，不调用其他 Skill

## 已发布章节锁定

| 操作 | 已发布章节（novel/chapters/） | 草稿章节（{draft}/chapters/） |
|------|----------|---------|
| 修改正文 | ❌ 禁止 | ✅ 允许（未发布时） |
| 错别字/标点 | ✅ 允许 | ✅ 允许 |
| 设定时间线 | 每条标注"引入章节"；修改时向前扫描 | — |

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `settings-manager` Skill | Step 2（merge-settings） | 🚫 硬阻断——设定合并不可跳过 |
| `ping-critic` Skill | Step 4（publish-verify） | 🚫 硬阻断——发布前校验不可跳过 |
| `{draft}/chapters/chapter-{N}.md` | Step 1 / Step 3.1 | 🚫 硬阻断——无草稿正文无法发布 |
| `{draft}/_publish-staging/` | Step 2-3 | 🚫 硬阻断——暂存区不可用则两阶段提交无法保证原子性 |
