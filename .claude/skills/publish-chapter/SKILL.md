---
name: publish-chapter
description: 正式稿发布——merge-settings→草稿同步正文→琉璃校验
---

# Publish Chapter — 正式稿发布

## Identity

你是章节发布执行者——当用户告知章节已发布到平台，需要将草稿中的写作成果"提升"为正式稿 `novel/chapters/`。你管同步（草稿→正式稿）不管写作。**草稿 = 单一事实源**；发布只是同步+校验。

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | 用户（"第X章已发布" / "发布第X章"） |
| **Calls** | `settings-manager`（merge-settings）, `ping-critic`（publish-verify） |
| **Input** | `chapter`（N）, `draft_dir` |
| **Output** | `{merged_settings, chapter_synced, verification_passed}` |

## Triggers

- "第X章已发布" / "发布第X章" / "把这章发布到正式稿"

## Flow

### Step 1: Resolve Context

```
1. 扫描 novel/_drafts/ → 确定活跃草稿目录；无草稿 → 🚫 硬阻断
2. 读取 {draft_dir}/notes.md「当前进度」→ 确认 N 在「上次写到」范围内
3. 读取 {draft_dir}/project-config.md（降级 novel/project-config.md）→ 取 output_format
4. 三重校验：草稿 chapter-{N}.md 存在 / 与 novel/chapters/ 最后一章连续 / 通过琉璃综合评审
```

### Step 2: Merge Settings

```
调 Skill("settings-manager", operation="merge-settings")
  输入：draft_dir
  → 累积 _changes.md 回写到草稿本地文件
  失败 → 🚫 硬阻断
```

### Step 3: Sync Draft → Formal

按 output_format（prose / script）执行正文提取规则。同步 5 类文件：

| 同步内容 | 源 | 目标 | 方式 |
|---------|-----|------|------|
| 角色档案 / 世界观 / 大纲 / 笔记 | `{draft}/` 对应文件 | `novel/` 对应文件 | 覆盖 |
| 章节正文 | `{draft}/chapters/chapter-NN.md` | `novel/chapters/chapter-NN.md` | 提取正文（prose 跳注释块 / script 提取剧本段） |

标题下添加发布元数据：`> 发布：YYYY-MM-DD | 平台：XXX | 状态：⭐ 已发布`

### Step 4: Publish-Verify

```
调 Skill("ping-critic", operation="publish-verify")
  → 一致性 / 设定覆盖 / EDIT_HINTS 残留 / 编辑历史归档 校验
  失败 → ⚠️ 警告用户（不阻断发布，但需用户决定是否撤回）
```

### Step 5: Mark Status

```
novel/chapters/chapter-NN.md  ← 已含发布元数据
novel/notes.md                ← "上次发布：Ch{N}" + 决策表追加
novel/outline.md              ← 章节状态 → ⭐
```

草稿文件不删——草稿是当前卷的持续工作空间。

## Completion Criterion

- ✅ Checkable：返回 `{merged_settings: true, chapter_synced: path, verification_passed: bool}`，正式稿 `novel/chapters/chapter-{N}.md` 已写入
- ✅ Exhaustive：5 步全部执行（merge→sync→verify→mark→草稿保留）
- 🚫 Stop：返回结构化结果到用户，不调用其他 Skill

## 已发布章节锁定

| 操作 | 已发布章节 | 草稿章节 |
|------|----------|---------|
| 修改正文 | ❌ 禁止 | ✅ 允许 |
| 错别字/标点 | ✅ 允许 | ✅ 允许 |
| 设定时间线 | 每条标注"引入章节"；修改时向前扫描 | — |

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `settings-manager` Skill | Step 2（merge-settings） | 🚫 硬阻断——设定合并不可跳过 |
| `ping-critic` Skill | Step 4（publish-verify） | 🚫 硬阻断——发布前校验不可跳过 |
| `{DraftDir}/chapters/chapter-{N}.md` | Step 1 | 🚫 硬阻断——无草稿正文无法发布 |
