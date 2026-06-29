# Skill-Skill 交互规范

> 本文件定义 Skill 之间所有交互的权威规范。CLAUDE.md 引用本文件作为调用架构的正式定义。

## 1. 调用架构

### 1.1 单层 Skill 模型

系统采用**单层 Skill 模型**。所有组件均为 Skill，运行在当前会话，支持多轮交互，Skill 之间可直接调用。Agent 降级为**可选优化手段**——仅在以下条件满足时使用：
- 执行逻辑 > 500 行纯文本（加载会严重占用上下文）
- 需要并行独立执行（互不依赖的子任务）
- 需要完全上下文隔离（如不可信输入处理）

其他场景优先使用 Skill→Skill 直接调用。

### 1.2 调用约束

- ✅ Skill→Skill 直接调用（通过 `Skill` tool）
- ✅ Skill→Agent（仅超大计算 / 并行独立 / 上下文隔离场景）
- ❌ Skill 定义中引用不存在的 Skill
- 🚫 **Skill 调用失败 → 🚫 硬阻断，禁止降级**。每个 Skill 的 Dependencies 表必须列出调用的所有 Skill，一律标 🚫 硬阻断。仅文件/Guide 缺失可选 ⚠️。

## 2. 结构化文件交换

### 2.1 核心原则

Skill 之间结构化信息交换优先走磁盘文件。对话上下文仅传递摘要、文件路径、决策结果，不传递完整数据载荷。

### 2.2 产出物文件

| 文件 | 写入者 | 含义 |
|------|--------|------|
| `_briefs/premise-seed.md` | xuanji | 碎片收敛 grilling 产出（`convergence_status: done`）；下游 idea-explorer / qing-novelist 读作工作输入（seed 富材料）；outline-tingle Session 1 前置 |
| `_briefs/chapter-{N}-direction.md` | qing-novelist | 阶段 3 完成，方向卡已产出 |
| `_briefs/chapter-{N}-exploration.md` | idea-explorer | 阶段 3.5 头脑风暴完成 |
| `_briefs/chapter-{N}-handoff.md` | plan-chapter | plan→generate 跨 Session 状态交接（字段契约见 §2.4） |
| `_briefs/chapter-{N}-brief.md` | mo-writer | 写作简报已产出 |
| `chapters/chapter-{N}.md` | sensory-writer | AI 章节已落盘 / 作者修订中 |
| `_reviews/chapter-{N}-review.md` | ping-critic | 综合评审完成 |
| `_reviews/chapter-{N}-fix-log.md` | generate-chapter | Fix 循环记录（最多 2 轮） |
| `_exchanges/scene-summaries.json` | sensory-writer | 200 字结构化场景摘要 |
| `_exchanges/call-params.md` | 调用方 Skill | 复杂参数磁盘传递 |
| `_exchanges/agent-result.md` | 被调 Skill | 结构化结果磁盘传递 |

所有产物 frontmatter 必含 `format_version` / `produced_by` / `produced_at` / `chapter`。`file-manager` 用 `format_version` 判格式迁移。

章节正文（`chapters/chapter-{N}.md`）frontmatter 额外含两个字段：
- `target_word_count`：规划期目标字数（`mo-writer` Step 5b 预填，来自 direction 卡「全章预估字数」）
- `word_count`：实测字数（`generate-chapter` Step 2c/4 + `publish-chapter` Step 3.1 回填）

**字数口径**：中文 + 中文标点。Unicode 范围 = CJK Unified `U+4E00–U+9FFF` + CJK Symbols/Punctuation `U+3000–U+303F` + Halfwidth/Fullwidth Forms `U+FF00–U+FFEF` + 省略号 `U+2026` + 破折号 `U+2014` + 中文引号 `U+2018/2019/201C/201D`。排除空白、英文、数字、西文标点。**测量范围**：仅 `## 正文` 段之后至文件末尾的内容（排除 frontmatter、章节标题、`> 发布：` 行、`## 元数据` 段、场景分隔 `---`、200 字摘要折叠块）。`## 元数据` markdown 段的「目标字数」「实测字数」两行与 frontmatter 同步。

### 2.3 Handoff 协议——写作链工作流

长工作流拆分多 Session。`plan-chapter` 末→`generate-chapter` 首为 handoff 切分点。写作链为线性 3 session；`publish-chapter` 为发布旁路，作者独立触发，与写作链正交（可跨章攒批、可跳过、可乱序），不作为写作链的线性后续。

```
SESSION 1: plan-chapter  → _briefs/chapter-{N}-handoff.md
SESSION 2: generate-chapter (C8 硬阻断验证 handoff) → chapter + review
── 写作链结束 ──
SIDE: publish-chapter（作者决定，独立触发） → 设定合并 + 正式稿
```

所有章节统一走写作链（plan-chapter 阶段 5 写 handoff 后退出，不内联简报/参考示例生成；mo / yin / 5c 在 generate-chapter Session 2 内执行）；publish-chapter 为发布旁路，作者独立触发，不在写作链 session 序列内。

### 2.4 Handoff 字段契约

`{draft_dir}/_briefs/chapter-{N}-handoff.md` frontmatter 必含 8 字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `chapter` | int | ✅ | 章节号 N |
| `direction` | path | ✅ | 方向卡路径（`chapter-{N}-direction.md`，相对 `{draft_dir}`） |
| `brief` | path | 🟡 | 简报路径（`chapter-{N}-brief.md`；planning 阶段可空，generate 阶段必填） |
| `chapter_file` | path | ✅ | 目标章节路径（`chapters/chapter-{N}.md`） |
| `character_state` | path | ✅ | 角色状态快照（`{draft_dir}/_character-state.md`——草稿侧增量；读取走 settings-manager read-character-state 双源合并 novel/ + 草稿侧） |
| `style_profile` | path | ✅ | 作者文风档案（`novel/author-voice.md`——**正式层路径**，草稿不镜像） |
| `workflow_position` | string | ✅ | 工作流位置（如 `"plan-step4-direction"` / `"generate-step2-brief"`） |
| `resume_command` | string | ✅ | 新 Session 启动命令（如 `/generate-chapter {N}`） |

- `path` 字段默认以 `{draft_dir}` 为根的相对路径；**设定文件字段例外**（如 `style_profile`）以 `novel/` 为根——草稿不镜像设定文件
- `workflow_position` 用 `<skill>-<step>-<artifact>` 三段式

入口硬检查（`generate-chapter` 启动时）：✅ 必填字段缺失或 handoff 文件不存在 → 🚫 硬阻断；`workflow_position` 前缀为 `generate-` 时 `brief` 必填。

**书级 handoff 例外**：上述 8 字段契约仅适用于章节级 handoff（`_briefs/chapter-{N}-handoff.md`）。书级大纲形成阶段（premise→L1→L2→L3）以 `outline.md` 本身作为 handoff 载体——不另建 handoff 文件，章节 8 字段契约不适用。

书级状态机改由 `outline.md` frontmatter 的 `workflow_position` 字段表达（状态值流转：`outline-tingle-step1-done` → `outline-tingle-l1-confirmed` → `outline-tingle-step2-done`），由 `outline-tingle` Skill 推进；`format_version: 2` 标识 v2 模板。`plan-chapter` 读 `outline.md` 时多出的 v2 frontmatter 字段忽略，不触发降级。

## 3. 稿件两层体系 + 临时中转 + 设定时间线

| 层 | 目录 | 性质 | 修改权限 |
|----|------|------|---------|
| 临时中转 | `novel/_import/{ts}/` | 导入外部成稿暂存 | 流程结束可删，不备份 |
| 正式层 | `novel/` 根设定 + `novel/_changes.md` + `novel/_character-state.md` + `novel/chapters/` | 静态设定 + 正式增量日志 + 已发布章节正文 | 机械写入（publish/merge）/ 人工慎改 |
| 草稿层 | `novel/_drafts/`（扁平化，单份，贯穿全书） | 工作产物 + 草稿增量 | 自由 |

**层划分本质**：按修改路径与权限划分，而非文件分布。正式层 = 机械写入 + 人工慎改；草稿层 = 工作中自由改。`chapters/` 与 `novel/` 根设定文件只是正式层内的文件分布，不是子层。

**草稿内容清单**：工件（`_briefs/` / `_exchanges/` / `_reviews/` / `chapters/` 仅未发布）+ 增量日志（`_changes.md` / `_character-state.md` / `_edit-history.md`，append-only）+ 元数据（`session-context.md` / `notes.md`）+ 归档（`_archive/chapter-{N}/`）+ 暂存（`_publish-staging/`）。**草稿不镜像设定文件**——设定读写全部走 `settings-manager read-settings`（双源合并 `novel/` + `{draft}/_changes.md`）。

**单草稿约束**：全局只一份 `novel/_drafts/`，无日期目录无 `_index.md`，贯穿全书复用，`session-context.md` 常驻判断当前阶段。

**`novel/_character-state.md`**：正式角色状态时间线，与静态角色档案 `characters/{name}.md` 分离——档案存"这角色是谁"，状态日志存"每章在哪/情绪/能力"。草稿侧 `{draft}/_character-state.md` 是写作期增量，publish 时 merge 进 `novel/_character-state.md`。

**双轨关系**（正式层 `_changes.md` vs 设定文件）：文件存当前状态（写作时直接读），日志存变更历史（评审/追溯用）。职责分离非冗余。强约束：**正式层设定文件不可手改**，只能通过 publish merge 更新——pre-flight-check C11 检测 mtime 一致性。

迁移：草稿章节通过 `publish-chapter` 两阶段暂存-提交写入正式层（章节 sync + 设定 merge + 日志追加 + 工件归档）。草稿管理由 `settings-manager` 处理（初始化/写作期/合并/归档）。

**设定时间线**：每条设定标注"引入章节"。评审/修改第 N 章时只参考引入章节 ≤ N 的条目；修改时向前扫描章节号 > 旧引入章节的已有章节是否冲突。冲突分级：🔴 必须修（直接矛盾/能力越界）/ 🟡 应修（关系跳跃/细节不一致）。

## 4. 调用约定

### 4.1 Skill 调用模板

**简单参数（≤4 个字段）**：
```
Skill tool, skill="{skill-name}"
  args: "chapter={N} draft_dir={path} mode={mode}"
```

**复杂参数**：
```
Skill tool, skill="{skill-name}"
  args: "params_file={draft_dir}/_exchanges/call-params.md"
```

调用方只传标识参数（谁、在哪、做什么），不传执行步骤。执行步骤在目标 Skill 定义中。

### 4.2 Operation 参数

多模式 Skill 通过 `operation` 参数切换：

| Skill | 有效 operation 值 |
|-------|------------|
| settings-manager | `read-settings` / `record-settings` / `init-draft` / `merge-settings` / `read-character-state` / `record-character-state` / `record-handoff` |
| fingerprint-discovery | `analyze` / `scan` |
| migration-keeper | `detect-format` / `check-compat` / `analyze-content` / `migrate-project` |
| voice-sculptor | `generate` / `mine` |
| ping-critic | `comprehensive-review` / `editor-consult` / `defect-marking` / `publish-verify` / `fingerprint-match` |
| yin-illustrator | `scene-design` / `illustration-prompt` |

单一模式 Skill（mo-writer、pre-flight-check）不需要 operation。

### 4.3 渐进披露

Skill 主体 SKILL.md ≤ 200 行；详细方法论外移到 `framework/guides/`（外部引用）或 `framework/_specs/`（架构规则）；阶段性状态写磁盘。Skill 加载时核心原则完整加载，方法论按需 Read。

### 4.4 文件缺失处理统一格式

每个 Skill 的 Dependencies 节统一为：
- `framework/guides/{name}.md` 不存在 → ⚠️ {受影响能力}已降级为{降级后行为}
- `novel/author-voice.md` 不存在 → 🚫 硬阻断（仅 pre-flight-check + mo-writer 执行此检查；author-voice 在正式层，草稿不镜像）
- `novel/characters/{name}.md` 不存在 → ⚠️ 角色{能力}检查已降级为{降级后行为}（角色档案在正式层，草稿不镜像；读取走 settings-manager read-settings 双源合并）

降级等级：🚫 硬阻断 / ⚠️ 降级（标注影响后继续）/ ℹ️ 不影响功能。

## 5. 废弃引用

以下引用已在当前架构中**废弃**，任何 Skill 定义文件中不得出现：

| 废弃引用 | 原因 | 替代 |
|----------|------|------|
| `Agent tool, subagent_type=` 调用 Skill | Agent 已降级为可选 | `Skill` tool |
| `## Mode:` 标记 | 旧 Agent 架构模式标记 | Skill 内部 operation 参数 |
| `settings-service Skill` | 从未实现 | `settings-manager` 直接执行 |
| `novel-memory Skill` | 已重命名 | `project-memory` |
| `project-memory Skill` | 已重命名 | `ask-yiyi` |
| `ai-quality-control Skill` | 已拆分 | `ping-critic` |
| `flow-analyzer` Agent / `fingerprint-analyzer` Agent | 已废弃 | `ping-critic` |
| `migration-workflow Skill` | 已合并 | `migration-keeper` (migrate-project) |
| `flow-assessment Skill` | 已废弃 | `ping-critic` 综合评审 |
| 薄分派器 Skill（仅转发参数不做执行） | 已合并 | 对应 Skill 直接执行 |
| 5c 评审循环 | 已并入 `chapter-review` | `generate-chapter` 内部完成 |
| 两层模型（Skill→Agent） | 已统一 | 单层 Skill 模型 |
| 四指纹 | 已扩展 | 五指纹（过度平滑/声音均化/合理偏置/语境衰减/叙述者解码） |

## 6. 与其他文件的关系

- **CLAUDE.md**：引用本文件为调用架构权威；含 8 条强制规则、产出物表、用户入口表
- **Skill 定义文件**：其 Contract / Dependencies / 文件缺失处理节必须符合本规范
- **file-manager**：补齐入口（ensure-novel/ensure-draft/create-backup/ensure-frontmatter）
- **migration-keeper**：check-compat 检查 `format_version` 字段；migrate-project 按 §2.2 执行
