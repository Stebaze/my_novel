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

### 2.3 Handoff 协议——4 Session 工作流

长工作流拆分多 Session。`plan-chapter` 末→`generate-chapter` 首为 handoff 切分点。

```
SESSION 1: plan-chapter  → _briefs/chapter-{N}-handoff.md
SESSION 2: generate-chapter (C8 硬阻断验证 handoff) → chapter + review
SESSION 3: publish-chapter  → 设定合并 + 正式稿
```

所有章节统一走 4-Skill 对称架构：plan-chapter 阶段 5 写 handoff 后退出，不内联简报/参考示例生成；mo / yin / 5c 在 generate-chapter Session 2 内执行。

### 2.4 Handoff 字段契约

`{draft_dir}/_briefs/chapter-{N}-handoff.md` frontmatter 必含 8 字段：

| 字段 | 类型 | 必填 | 说明 |
|------|------|:---:|------|
| `chapter` | int | ✅ | 章节号 N |
| `direction` | path | ✅ | 方向卡路径（`chapter-{N}-direction.md`，相对 `{draft_dir}`） |
| `brief` | path | 🟡 | 简报路径（`chapter-{N}-brief.md`；planning 阶段可空，generate 阶段必填） |
| `chapter_file` | path | ✅ | 目标章节路径（`chapters/chapter-{N}.md`） |
| `character_state` | path | ✅ | 角色状态快照（`{draft_dir}/_character-state.md`） |
| `style_profile` | path | ✅ | 作者文风档案（`{draft_dir}/author-voice.md`） |
| `workflow_position` | string | ✅ | 工作流位置（如 `"plan-step4-direction"` / `"generate-step2-brief"`） |
| `resume_command` | string | ✅ | 新 Session 启动命令（如 `/generate-chapter {N}`） |

- `path` 字段以 `{draft_dir}` 为根的相对路径
- `workflow_position` 用 `<skill>-<step>-<artifact>` 三段式

入口硬检查（`generate-chapter` 启动时）：✅ 必填字段缺失或 handoff 文件不存在 → 🚫 硬阻断；`workflow_position` 前缀为 `generate-` 时 `brief` 必填。

## 3. 稿件三层体系 + 设定时间线

| 层 | 目录 | 性质 | 修改权限 |
|----|------|------|---------|
| 原稿 | `novel/_reference/` | 上传原始素材 | 只读 |
| 草稿 | `novel/_drafts/{latest}/` | 实验性写作 | 自由 |
| 正式稿 | `novel/chapters/` | 已发布 | 谨慎 |

迁移：`原稿 → author-voice.md → 草稿 → 正式稿`。草稿管理由 `settings-manager` 处理（初始化/写作期/合并/废弃）。

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
- `{draft}/author-voice.md` 不存在 → 🚫 硬阻断（仅 pre-flight-check + mo-writer 执行此检查）
- `{draft}/characters/{name}.md` 不存在 → ⚠️ 角色{能力}检查已降级为{降级后行为}

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
