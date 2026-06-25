---
name: import-chapter
description: 多格式章节导入——源文件接收→AI扫描设定摘要→草稿迁移→评审队列注册
---

# Import Chapter Skill — 章节导入

## Identity

章节导入编排器——接受作者已有成稿（.md / .txt / .docx / .epub 或直接粘贴），纳入三层稿件体系（原稿→草稿），AI 辅助扫描生成设定摘要，注册评审队列。

**Router 范式**：本 Skill 是薄封装层——做格式识别 + 分派调用 + 文件迁移，不重复实现分析/扫描逻辑（按需调 `settings-manager` / `chapter-review`）。

**核心原则**：
- **文本原样保留**：导入不修改正文
- **先入原稿再进草稿**：原始文件存 `novel/_reference/`，转换 .md 进草稿 `chapters/`
- **设定回填需作者确认**：扫描摘要一律 `🤖 待确认`
- **导入后必须评审**：未 `chapter-review` 的导入章节不能 `publish-chapter`
- **草稿优先**：目标为活跃草稿；无活跃草稿时先 `file-manager`（ensure-draft）

**与 adaptation-workflow 区别**：

| 维度 | import-chapter | adaptation-workflow |
|------|---------------|-------------------|
| 目的 | 纳入已有成稿 | 改写/润色 |
| 文本处理 | 原样保留 | 会修改 |
| 产出 | 设定摘要 + 评审队列 | 改编版（深度可变）|

## Contract

| Aspect | Detail |
|--------|--------|
| **Calls** | `file-manager`（ensure-draft / save-reference）, `settings-manager`（record-settings / record-character-state）|
| **Produces** | `{draft}/chapters/chapter-NN.md`, `{draft}/_changes-draft.md`, `{draft}/_character-state-draft.md`, `{draft}/_thread-map-draft.md`, `{draft}/_character-arcs-draft.md`, `{draft}/_import-analysis/_review-queue.md`, `novel/_reference/{源文件}` |
| **Called by** | 用户入口（"导入章节" / "导入第X章"），`bootstrap-project`（步骤 2 复用）|

## Triggers

- "导入章节" / "导入第X章" / "导入这些章节" / "导入原稿" / "导入 manuscript"
- "把这章导入" / "帮我把这个 docx 导入"

## Flow

### 步骤 1：源文件接收 + 格式转换

**1.1 识别输入类型**：

| 输入 | 处理 |
|------|------|
| `.docx` 文件 | `python3 .claude/scripts/docx2md.py "{input}" --output-dir "{draft}/import-temp/"` |
| `.epub` 文件 | `python3 .claude/scripts/epub2md.py "{input}" --output-dir "{draft}/import-temp/"` |
| `.md` / `.txt` 文件 | 直接 Read + 按章节标题（`第X章` / `Chapter X` / `# 第X章`）拆分 |
| 直接粘贴文本 | 保存为 `{draft}/import-temp/pasted.md` 后同上拆分 |

**1.2 保存原始文件**：`cp {源文件} novel/_reference/`

**1.3 生成导入清单**：写入 `{draft}/import-temp/_import-manifest.md`

**1.4 [门禁] 作者确认**：展示导入清单（每来源检测章节数 + 边界 + 编号），作者确认或修正（编号偏移 → `--start-num`；边界错误 → 手动调整；缺失 → 补充）

### 步骤 2：AI 内容扫描

**2.1 草稿就绪检查**：

```
{draft} 不存在 → 调 file-manager(ensure-draft) 初始化
{draft} 存在 → 直接使用
```

**2.2 逐章扫描**（每个章节 .md 文件 Read 全文）：

| 维度 | 产出文件 | 标记 |
|------|---------|------|
| 角色状态（9 维：位置/身体/心理/能力/关系/目标/情绪/持续行动/关键物品）| `_character-state-draft.md` | `📖 原文明确` / `🤖 AI推断` |
| 设定变更 | `_changes-draft.md` | `🤖 待确认` |
| 伏笔（已埋 / 已回收 / 推进）+ 支线 | `_thread-map-draft.md` | `🤖 AI推断` / `📖 原文明确`，状态 `🌱 待确认` |
| 弧光事件（行为/认知/关系/状态变化）+ 关系里程碑 | `_character-arcs-draft.md` | 置信度标注 |
| 一句话情节摘要 | 内嵌评审队列 | — |

**2.3 扫描质量门禁**：展示摘要统计（X 角色 / Y 设定 / Z 伏笔 / W 弧光 / V 推断）→ 进入步骤 3

### 步骤 3：草稿迁移

```
1. cp import-temp/chapter-NN.md {draft}/chapters/
   冲突处理：作者选 覆盖/跳过/保留两者（重命名 chapter-NN-imported.md）
2. mv import-temp/import-analysis/ {draft}/import-analysis/
3. 更新 {draft}/notes.md 追加导入记录
4. 生成 {draft}/_import-analysis/_review-queue.md（格式见 framework/templates/_review-queue-template.md）
```

### 步骤 4：作者确认 + 写入正式设定

**4.1 逐条确认**（优先展示 `🤖 AI推断` 项）：

- ✅ 确认 → 标记 `🟢 确认`
- ✏️ 修正 → 用作者提供的新值
- ❌ 拒绝 → 丢弃

**4.2 写入正式追踪文件**：调 `settings-manager` 完成

| 数据 | settings-manager 操作 |
|------|---------------------|
| 设定变更 | `record-settings`（追加到 `{draft}/_changes.md`）|
| 角色状态 | `record-character-state`（按章节组织到 `{draft}/_character-state.md`）|
| 伏笔/支线/主线 | `append-thread-map`（不存在则从 `framework/templates/thread-map.md` 复制）|
| 弧光事件 | `append-character-arc`（不存在则从模板复制）|

**4.3 完成提示**：

```
导入完成。
- {N} 个章节已放入草稿 {draft}/chapters/
- {X} 条设定变更 / {Y} 条角色状态 / {V} 条伏笔 / {A} 条弧光 已写入追踪文件
- 评审队列已就绪：{draft}/_import-analysis/_review-queue.md

下一步：
- 逐章评审：说"评审第X章"
- 批量评审：说"批量评审导入章节"
- 继续写作：说"写第X章"（plan-chapter 会自动检测已导入章节）
```

## Completion Criterion

- ✅ Checkable：返回 `{imported_chapter, settings_extracted, review_queued}` 给用户
- ✅ Exhaustive：4 步骤执行完毕，评审队列文件已落盘，settings-manager 写入完成
- 🚫 Stop：不调 chapter-review——让用户自己触发

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `file-manager` Skill | 步骤 2.1（ensure-draft）| 🚫 硬阻断——草稿不可用则导入无法完成 |
| `settings-manager` Skill | 步骤 4.2 | 🚫 硬阻断——设定写入不可降级 |
| `.claude/scripts/docx2md.py` | 步骤 1.1（.docx）| 🟡 提示 `pip install python-docx` 或手动粘贴 |
| `.claude/scripts/epub2md.py` | 步骤 1.1（.epub）| 🟡 提示 `pip install ebooklib` 或手动粘贴 |
| `framework/templates/_import-manifest-template.md` | 步骤 1.3 | ⚠️ 降级为内嵌最小清单 |
| `framework/templates/_review-queue-template.md` | 步骤 3 | ⚠️ 降级为内嵌最小队列 |
| `framework/templates/{thread-map,character-arcs}.md` | 步骤 4.2 | ⚠️ 降级为内嵌最小表头 |
