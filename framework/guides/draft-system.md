---
sections:
  - heading: "## 两层体系"
    agents: [file-manager, settings-keeper, ask-yiyi]
    desc: "正式层/草稿层+临时中转——目录/性质/修改权限"
  - heading: "## 目录结构"
    agents: [file-manager]
    desc: "草稿目录树标准结构（单草稿扁平化）"
  - heading: "## 草稿内容清单"
    agents: [file-manager, settings-keeper]
    desc: "草稿只存工作产物+增量日志，不镜像设定文件"
  - heading: "## 设定读写约定"
    agents: [file-manager, settings-keeper, plan-chapter, chapter-review, qing-novelist, ping-critic]
    desc: "所有 Skill 读设定走 settings-manager read-settings，禁止直接 Read 草稿设定"
  - heading: "## 迁移到正式层"
    agents: [file-manager, settings-keeper, publish-chapter]
    desc: "publish 两阶段暂存-提交——草稿章节删除+工件归档"
---

# 草稿

> **定位**：两层稿件体系中的**草稿层**。单份、扁平化、贯穿全书复用——无日期目录、无会话索引。`session-context.md` 常驻判断当前阶段。

## 两层体系

| 层 | 目录 | 性质 | 修改 |
|----|------|------|------|
| **临时中转** | `novel/_import/{ts}/` | 导入外部成稿暂存 | 流程结束可删，不备份 |
| **正式层** | `novel/` 根设定 + `novel/_changes.md` + `novel/_character-state.md` + `novel/chapters/` | 静态设定 + 正式增量日志 + 已发布章节正文 | 机械写入（publish/merge）/ 人工慎改 |
| **草稿** | `novel/_drafts/` ← 本目录 | 工作产物 + 草稿增量 | 自由 |

层划分按修改路径与权限，而非文件分布。`chapters/` 与 `novel/` 根设定文件是正式层内的文件分布，不是子层。

## 目录结构

```
_drafts/                          # 单份草稿，无日期目录、无 _index.md
├── notes.md                      # 草稿层总体摘要
├── session-context.md            # 工作流状态/琉璃交接/下一步——常驻判断当前阶段
├── _changes.md                   # 草稿侧设定增量（append-only，merge 后打 merged_at 不清空）
├── _character-state.md           # 草稿侧角色状态增量（append-only）
├── _edit-history.md              # 编辑历史（append-only）
│
├── _briefs/                      # 方向卡 / handoff / 简报
├── _exchanges/                   # settings-snapshot / scene-summaries / call-params / agent-result
├── _reviews/                     # 评审报告 / Fix log
├── chapters/                     # 仅未发布章节正文
├── _archive/                     # publish 后归档：_archive/chapter-{N}/（伴生工件 + _edit-history）
│   └── chapter-{N}/
└── _publish-staging/             # publish 暂存区（两阶段提交的中转）
```

## 草稿内容清单

草稿**只存**以下内容，**不镜像设定文件**（角色档案 / 世界观 / 大纲 / author-voice / style-guide 等一律不复制）：

- **工件**：`_briefs/` / `_exchanges/` / `_reviews/` / `chapters/`（仅未发布）
- **增量日志**（append-only）：`_changes.md` / `_character-state.md` / `_edit-history.md`——merge 后打 `merged_at` 标记，不清空
- **元数据**：`session-context.md` / `notes.md`
- **归档**：`_archive/chapter-{N}/`——publish 后伴生工件 + `_edit-history.md` 移入
- **暂存**：`_publish-staging/`——publish 两阶段提交的中转区

## 设定读写约定

**所有 Skill 读设定必须走 `settings-manager read-settings`**——双源合并 `novel/` 设定文件 + `{draft}/_changes.md`（筛选未合并条目，引入章节 ≤ N）。**禁止直接 `Read({draft}/characters/{name}.md)` / `Read({draft}/world/...)`**——草稿无设定副本，直接读会读空。

`read-character-state` 同理：双源合并 `novel/_character-state.md`（全部已发布）+ `{draft}/_character-state.md`（已合并+未合并），筛选 ≤ N-1。

## 迁移到正式层

草稿章节通过 `publish-chapter` 两阶段暂存-提交写入正式层：

1. **暂存阶段**：所有写入先落 `{draft}/_publish-staging/`（章节副本 + 设定 diff + 待追加条目）。失败删 staging，正式层零影响。
2. **提交阶段**：依次 mv 章节到 `novel/chapters/`、apply 设定 diff、追加 `novel/_changes.md` / `novel/_character-state.md` 条目、草稿侧打 `merged_at` 标记。
3. **草稿清理**：草稿 `{draft}/chapters/chapter-{N}.md` 删除（不双写）；伴生工件（`_briefs/chapter-{N}-*` / `_exchanges/scene-summaries 相关` / `_reviews/chapter-{N}-*`）+ `_edit-history.md` 移到 `{draft}/_archive/chapter-{N}/`。

正式层 `_changes.md` 与设定文件双轨：文件存当前状态（写作时直接读），日志存变更历史（评审/追溯用）。**正式层设定文件不可手改**——pre-flight-check C11 检测 mtime 一致性。
