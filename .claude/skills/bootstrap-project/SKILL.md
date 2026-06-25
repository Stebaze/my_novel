---
name: bootstrap-project
description: 项目冷启动工作流——检测已有素材→批量导入→全文逆向分析→作者确认→工件生成，使项目就绪 plan-chapter 续写
---

# Bootstrap Project Skill — 冷启动工作流

## Identity

项目冷启动编排器——从 0 到 1 把已有成稿纳入系统，逆向产出全部规划工件（大纲/声音/角色/设定/伏笔），使 `plan-chapter` → `chapter-review` 标准流水线可运行。

**Router 范式**：本 Skill 是薄封装层——做判定、分派、串联，不重复实现分析方法论。每一步调下层 Skill 完成具体任务。

## Contract

| Aspect | Detail |
|--------|--------|
| **Calls** | `file-manager`（ensure-novel/ensure-draft/backup）, `import-chapter`（多格式导入）, `settings-manager`（init-draft/record-settings/record-character-state）, `pre-flight-check`（Phase 4 验证）, `qing-novelist`（作者分析模式 — Phase 1 七维提取）, `ping-critic`（指导者差距诊断 — 条件）, `technique-selector`（高潮机制识别 — 条件） |
| **Produces** | `novel/outline.md`, `novel/author-voice.md`, `novel/voice-bible.md`, `novel/vocabulary-bank.md`, `novel/style-guide.md`, `novel/thread-map.md`, `novel/character-arcs.md`, `novel/world/{rules,setting,timeline}.md`, `novel/characters/{角色}.md`, `novel/project-config.md`, `{draft}/_changes.md`, `{draft}/_character-state.md`, `{draft}/_bootstrap/_completion.md` |
| **Called by** | 用户入口（"初始化项目" / "冷启动" / "bootstrap"）|

## Triggers

- "启动项目" / "冷启动" / "bootstrap"
- "我有一些章节，帮我初始化项目"
- "从已有章节开始规划" / "导入全书并开始规划"

## Flow

> **断点续传**：所有阶段通过 `{draft}/_bootstrap/_progress.md` 跟踪状态。已完成的阶段跳过；新会话可从断点继续。

### Pre-flight：备份已有 novel/

```
检查 novel/ 目录（排除 .gitkeep）
  → 不存在或为空 → 继续 Phase 0
  → 存在且有内容：
    mv novel/ reference/novel_{YYYY-MM-DD_HHmmss}/
    告知作者"已备份到 reference/novel_{datetime}/"
```

### 6 步冷启动流程

#### 步骤 1：检测已有素材 + 备份（Pre-flight）

调 `file-manager`（backup-existing-novel）——若 `novel/` 已存在非空内容则备份到 `reference/novel_{datetime}/`，再继续。

#### 步骤 2：批量导入 + 三层分派（Phase 0）

1. **[用户交互]** 收集来源结构（已发布/原稿/脑内设定/指导者）→ 写入 `_bootstrap/_project-input.md`
2. 调 `import-chapter` 完成多格式导入（md / txt / docx / epub 格式转换 + 章节拆分 + 原稿保存）
3. 调 `file-manager`（ensure-novel）建立目录骨架
4. 调 `settings-manager`（init-draft）创建草稿目录
5. 三层分派：已发布 → `novel/chapters/`（锁定）；原稿 → `{draft}/chapters/`；脑内设定 → Phase 3 处理
6. **[门禁]** 展示导入清单 → 作者确认 → 写 `_import-manifest.md` + `_progress.md` Phase 0 ✅

#### 步骤 3：全书综合分析（Phase 1）

调各 Skill 串行执行，每项产出落盘到 `_bootstrap/`：

| 子项 | 调用的 Skill / 方法论 | 产出 |
|------|---------------------|------|
| 1a 大纲逆向（L1-L3） | 内联分析（参考 `framework/guides/bootstrap-workflow-guide.md`）| `_outline-draft.md` |
| 1b 节拍+高潮诊断 | `technique-selector`（技法匹配）| `_beat-analysis.md` |
| 1c 作者声音七维提取 | `qing-novelist`（分析模式 → 7 维作者分析协议）| `_author-voice-draft.md` |
| 1d 设定+角色+伏笔+弧光全量扫描 | 内联 Read 逐章 + 标记 `📖 原文明确` / `🤖 AI推断` | `_character-state-draft.md` + `_settings-draft.md` + `_thread-map-draft.md` + `_character-arcs-draft.md` |
| 1e [条件] 指导者差距诊断 | `ping-critic` + `technique-selector` | `_mentor-gap-report.md` |
| 1d 角色完整度检测 | 内联评分（10 维 / 角色 0-20）| `_character-completeness.md` |

**降级**：< 3 章 → ⚠️ 风格未稳定；3-9 章 → L3 跳过；≥ 10 章 → 全分析

**[门禁]** 1a-1e 产出就位 → `_progress.md` Phase 1 ✅

#### 步骤 4：作者脑内设定 + 角色丰富（Phase 2）

1. **设定访谈**（对话式）：逐类展示原文明确 / AI 推断 / 作者补充三类设定 → 作者确认/修正/拒绝
2. **单薄角色丰富**：调 qing-novelist 五步访谈协议（唤起 → 拆解 → 映射 → 填充 → 差异化）— 详细方法论见 `framework/guides/character-enrichment-guide.md`

**[门禁]** 访谈日志 + 单薄角色处理（前 3 个）→ `_progress.md` Phase 2 ✅

#### 步骤 5：交叉验证 + 逐项确认（Phase 3）

[对话式] 按顺序逐项确认：L1-L3 大纲 → 高潮布局 → 角色完整度 → 三层设定合并视图 → author-voice.md。每项可"暂缓确认"（不阻塞）。

**[门禁]** 至少 L1 大纲 + author-voice.md 已确认 → `_progress.md` Phase 3 ✅

#### 步骤 6：工件生成 + 验证（Phase 4）

1. 调 `file-manager`（ensure-novel）补齐缺失模板
2. 写入 `novel/` 全部工件（`outline.md` / `author-voice.md` / `voice-bible.md` / `thread-map.md` / `character-arcs.md` / `world/*.md` / `project-config.md` / 角色档案）
3. 调 `settings-manager`（record-settings + record-character-state）写入草稿追踪文件
4. 调 `pre-flight-check` 验证 C2-C3 关键门禁（设定快照可读 + 角色档案就绪）
5. 写入 `_bootstrap/_completion.md` → `_progress.md` Phase 4 ✅

**完成提示**：

> "项目已就绪。说「写第 X 章」即可开始 plan-chapter 流程。"

## Completion Criterion

- ✅ Checkable：返回 `{draft_path, analysis_report, ready_for_plan_chapter: true}` 给用户
- ✅ Exhaustive：6 步全部执行完毕，`_completion.md` 已落盘，pre-flight-check C2-C3 验证通过
- 🚫 Stop：不调 plan-chapter——让用户自己触发下一章

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `file-manager` Skill | 步骤 1/2/6 | 🚫 硬阻断——目录结构无法建立 |
| `import-chapter` Skill | 步骤 2 | 🚫 硬阻断——批量导入不可跳过 |
| `settings-manager` Skill | 步骤 2/6 | 🚫 硬阻断——设定写入不可降级 |
| `pre-flight-check` Skill | 步骤 6 | 🚫 硬阻断——验证不可跳过 |
| `qing-novelist`（分析模式） | 步骤 3 1c | 🚫 硬阻断——作者七维分析不可降级 |
| `technique-selector` Skill | 步骤 3 1b | 🚫 硬阻断——技法识别不可降级为手动 |
| `ping-critic` Skill | 步骤 3 1e（条件）| 🚫 硬阻断——指导者差距诊断不可跳过 |
| `framework/guides/bootstrap-workflow-guide.md` | 步骤 3 1a/1d | ⚠️ 内嵌简化规则——置信度降级为常识 |
| `framework/guides/character-enrichment-guide.md` | 步骤 4 角色丰富 | ⚠️ 内嵌四步流程——方法论深度降级 |
| `profiles/authors/{mentor}.md` | 步骤 3 1e | 🟡 提示运行 qing-novelist（分析模式）建档，拒绝则跳过 |
