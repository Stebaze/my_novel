# 小说写作项目

AI 辅助长篇小说写作工程。Claude Code 载体，21 个 Skill 协作完成规划→简报→AI 生成章节→评审→发布。**4-Skill 对称架构**将单 session 长流程切分为 4 阶段：`plan → handoff → generate → review → publish`。

- **核心机制**：AI 产出"写作简报"引导作者执笔，**或启用 AI 生成整章模式**（4 session）
- **架构**：单层 Skill 架构（运行在当前会话）+ 显式 handoff 协议（多 session 衔接）
- **稿件管理**：两层体系（正式层机械写入/草稿层自由）+ 临时中转 + 设定变更追踪
- **架构规范**：[`framework/_specs/interaction-spec.md`](framework/_specs/interaction-spec.md)
- **当前作品**：[见 `novel/project-config.md`]

## ⚠️ 强制规则

1. **写作规划强制规则**：任何写作规划请求（写新章节/续写/重写前的规划）**必须通过 `plan-chapter` Skill 执行工作流（阶段 0-5：前置检查→设定快照→草稿初始化→[条件]头脑风暴→启发式交谈→Handoff 输出），产出方向卡与 handoff 文件后方可进入生成**。plan-chapter 不内部完成简报生成——简报生成已迁入 `generate-chapter` Step 1。没有例外。

2. **Handoff 强制规则**：任何章节进入 `generate-chapter` 生成阶段之前，**必须存在有效的 `_briefs/chapter-{N}-handoff.md` 文件**。`plan-chapter` 完成后会自动写出 handoff；用户在新 session 输入 `/generate-chapter {N}` 触发后续生成。`generate-chapter` 在 pre-flight-check C8 验证 handoff 缺失时直接 🚫 硬阻断。没有例外。

3. **改编项目自动路由规则**：在收到写作请求时，**必须先读取 `novel/project-config.md` 的「创作模式」字段**。若 `创作模式 = 改编`，则所有写作请求（写新章节/续写/重写）**必须通过 `adaptation-workflow` Skill 发起**（而非直接调用 `plan-chapter`）。`adaptation-workflow` 是写作工作流的薄封装层——在标准工作流基础上增加原作感知（阶段 0 原作画像提取 + 改编简报 §0 源文对照层 + 评审对齐级别选择）。原作来源路径从 `project-config.md` 的「原作来源」字段读取。改编流经 adaptation-workflow 阶段 0 → 0.5（outline-tingle mode="adaptation"）→ 逐章循环。

4. **写后评审强制规则**：章节评审请求**必须通过 `chapter-review` Skill 执行**——`mode="writing"`（人工写章节）/ `mode="ai-content"`（AI 生成章节）/ `mode="adaptation"`（改编章节），每轮产出独立修改报告。**旧 plan-chapter 5c 参考示例评审已迁移到 `chapter-review`，不再独立运行**。没有例外。

5. **作者风格档案强制规则**：写作规划时如用户指定对标某作者风格，而 `profiles/authors/` 中不存在该作者档案，**必须先执行 `qing-novelist`（作者分析模式）的七维分析流程**，建立档案并写入磁盘后，方可进入简报生成阶段。没有例外。

6. **文件路径强制规则**：草稿优先。草稿固定路径 `novel/_drafts/`（单份、扁平化、贯穿全书，无日期目录无 `_index.md`）。草稿**只存工作产物 + 增量日志**（`_changes.md` / `_character-state.md` / `_edit-history.md`，append-only），**不镜像设定文件**——设定读写一律走 `settings-manager read-settings`（双源合并 `novel/` + `{draft}/_changes.md`），禁止直接 `Read({draft}/characters/...)` / `Read({draft}/world/...)`（草稿无副本，直接读会读空）。**Handoff 模式同样适用：handoff 文件（`_briefs/chapter-{N}-handoff.md`）、简报、章节正文、评审报告一律落盘到草稿对应子目录**。无活跃草稿时降级使用 `novel/` 路径。

7. **改编原作画像强制规则**：任何改编规划请求**必须先在 `adaptation-workflow` 阶段 0 完成六维原作画像提取**（`reference/manuscripts/_analysis/{作品名}.md`），原作画像不存在时禁止进入改编规划。注意：此处的 `reference/manuscripts/` 是**改编原作分析目录**（项目根下，存原作画像），与稿件体系中已删除的 `novel/_reference/` 原"原稿层"无关——两者同名但完全独立，不要混淆。没有例外。

8. **工作流进度追踪规则**：每次会话启动时**必须**检查当前活跃草稿下的工件文件（`_briefs/`、`chapters/`、`_reviews/`），根据工件存在性确定各章节所处阶段，检测异常（跳过步骤），在会话初始化摘要中呈现给用户。**章节阶段判定标志**：`_briefs/chapter-{N}-direction.md` 存在 → plan-chapter 阶段 3 完成；`_briefs/chapter-{N}-handoff.md` 存在 → plan-chapter 全部完成（可进入 generate-chapter）；`_briefs/chapter-{N}-brief.md` 存在 → generate-chapter Step 1 完成；`_exchanges/scene-summaries.json` 存在 → generate-chapter Step 2 完成（per-scene 生成完成）；`chapters/chapter-{N}.md` 存在 → 章节已写；`_reviews/chapter-{N}-review.md` 存在 → 评审已做；`_reviews/chapter-{N}-fix-log.md` 存在 → Fix 循环已执行。**书级阶段判定标志**：`outline.md` frontmatter `workflow_position = outline-tingle-step1-done` → outline-tingle Session 1 完成；`= outline-tingle-l1-confirmed` → L1 已确认；`= outline-tingle-step2-done` → 大纲形成完成（可进 plan-chapter）；`book_settings_dispatched = true` → outline-tingle 2.8.5 书级设定派发完成（characters/character-arcs/world/thread-map 已含骨架）。**禁止**在不满足前置条件时进入下一阶段。没有例外。

9. **书级大纲形成强制规则**：原创项目首次规划请求时，`pre-flight-check` C9 检测 `novel/outline.md` L1-L3 实质填充度——含 `（待定）` 占位 / frontmatter `workflow_position` 非 `outline-tingle-step2-done`/`bootstrap-completed` 时报 **🟡 软阻断**（尊重网文边写边定，不硬阻断，用户可确认放行继续写）。C9 修复路径指向 `outline-tingle`（正向）/ `bootstrap-project`（逆向）。改编流由 `adaptation-workflow` 阶段 0.5 强制调用 `outline-tingle mode="adaptation"`——**改编流大纲未达门禁为 🚫 硬阻断**（adaptation-workflow 阶段 0.5 门禁，禁止进逐章循环）。原创软阻断 vs 改编硬阻断的不对称是设计意图：改编流以原作为锚，大纲未定则无对齐基准。**C10 提醒**：`book_settings_dispatched ≠ true`（且 L1-L3 已填实）→ 书级设定未派发到 characters/character-arcs/world/thread-map，下游 plan-chapter 设定快照这些文件返回空，仅 outline.md 可读（⚠️ 软提醒不阻断）。**C11 提醒**：`novel/` 设定文件 mtime 晚于 `novel/_changes.md` 最后 `merged_at` → 正式层设定文件被人工手改（违反"正式层不可手改"约束），⚠️ 软提醒不阻断，提示从 _backup/ 恢复或回填 _changes.md。没有例外。

## 工作流

### 4 Skill 对称架构

> **书级前置（Session 0）**：`outline-tingle`（2 session：premise→L3）是 plan-chapter 的前置阶段——产出 `outline.md`（L1-L3 填实 + frontmatter `workflow_position: outline-tingle-step2-done`）后才进入下方 4-Skill 章节级循环。改编流由 `adaptation-workflow` 阶段 0.5 编排 outline-tingle (mode="adaptation")。

```
SESSION 1 — plan /plan-chapter {N}
  阶段 0：前置检查（C0-C8）→ 1：设定快照 → 2：草稿初始化（如需）
  阶段 3：[条件] 头脑风暴 → 4：启发式交谈（五更→琉璃校验）→ 方向卡
  阶段 5：Handoff 输出 → 6：输出 handoff 提示
  → _briefs/chapter-{N}-handoff.md
[HANDOFF] 用户开新对话，输入 /generate-chapter {N}
SESSION 2 — generate /generate-chapter {N}
  Step 0：pre-flight-check C8（🚫 硬阻断若无 handoff）
  Step 1：mo-writer → 简报；Step 2：sensory-writer（per-scene）→ 章节
  Step 3：chapter-review (mode="ai-content", auto) → 评审报告
  Step 4：[条件] Fix 循环（最多 2 轮）→ 重写受影响场景
  → chapters/chapter-{N}.md + _reviews/
[USER 轻编辑 — 可选 /chapter-review {N} 复审]
SESSION 3 — publish /publish-chapter {N}
  settings-manager(merge) → 设定更新；ping-critic(publish-verify) → 发布前校验
  → 正式稿
```

### 改编流

`adaptation-workflow` 编排全循环：`plan-chapter` 用 `mode="adaptation"`，加原作画像（阶段 0）+ 原作对齐检查（严格/平衡/宽松）。逐章循环：`plan-chapter → /generate-chapter → /chapter-review → /publish-chapter`，每步产物同 4 session 架构。

## 用户入口

| Skill | 触发词 | 功能 |
|------|--------|------|
| `plan-chapter` | 写第X章 / 续写 | 规划（方向卡 + handoff） |
| `generate-chapter` | `/generate-chapter {N}` | 生成（简报 + AI 章节 + auto 评审） |
| `chapter-review` | 评审第X章 | 评审（3 mode） |
| `publish-chapter` | 发布第X章 | 发布（设定合并 + 校验） |
| `adaptation-workflow` | 改编这个作品 | 薄封装层（原作感知 + 4 Skill 循环） |
| `outline-tingle` | 从零写新书 / 形成大纲 | 大纲形成（premise→L3，2 session） |
| `bootstrap-project` | 冷启动 | 编排入口（批量导入→逆向分析→工件生成） |
| `import-chapter` | 导入章节 | 编排（源文件→草稿迁移→评审队列） |

## 单场景模式

`novel/project-config.md`「节拍配置」的 **`每章场景数`** 字段控制每章场景数。设为 `1` 时启用**单场景模式**——为移动端阅读与决策减负：

- `qing-novelist` 启发交谈 D2 场景清单固定长度 1，D4b（场景衔接）不激活
- `mo-writer` 简报 §1 只列 1 个场景（无「衔接计划」字段）、§3 作为该唯一场景的完整节拍层、`asymmetry_weight` 固定 1.0
- `generate-chapter` / `chapter-review` / `sensory-writer` **不动**——per-scene 机器照跑，`scene-summaries.json` 仅 1 条，`scene_index` 恒为 0，评审/Fix 循环链路保住

配置缺失或值 > 1 时按原多场景协议。

## 关键入口

| 路径 | 作用 |
|------|------|
| `framework/_specs/interaction-spec.md` | 架构规范（Skill 命名/调用/handoff 协议） |
| `framework/guides/` / `framework/templates/` | 方法论文档（21 篇）/ 初始化模板 |
| `novel/project-config.md` | 项目配置（创作模式/原作来源/输出格式） |
| `novel/_drafts/notes.md` | 项目状态（活跃期间唯一真相源） |
| `novel/_drafts/session-context.md` | 跨 session Skill 交接上下文 |
| `novel/chapters/` / `novel/_import/{ts}/` | 正式稿 / 临时中转（流程结束可删） |
| `profiles/authors/` | 作者风格档案（`qing-novelist` 作者分析模式产出）— 个体档案不入版本管理，本地保留 + `_index` 重建 |

`novel/` 不在版本管理中。完整文件列表用 `ls framework/ novel/` 获取。

## 文件读取优化：YAML Sections Frontmatter

`framework/` 和 `novel/` 下的 .md 文件均添加 YAML frontmatter，含 `sections` 字段。Skill 读取两步走：(1) `Read(file, limit=40)` → 获取 sections 列表；(2) 匹配所需章节 → `grep` 获取 heading 行号 → `Read(file, offset=N, limit=M)` 精准读取。**字段约定**：`framework/guides/*.md` 用 `agents:`；`framework/templates/*.md` 和 `novel/**/*.md` 用 `skills:`。节省 60-90% 上下文消耗。frontmatter 缺失由 `pre-flight-check` C3.3 检测并自动调 `file-manager` 补齐。

## 产出物即状态

| 产出物 | 含义 |
|--------|------|
| `_briefs/chapter-{N}-direction.md` | 阶段 3 完成，方向卡已产出 |
| `_briefs/chapter-{N}-exploration.md` | 阶段 3.5 头脑风暴完成 |
| `_briefs/chapter-{N}-handoff.md` | handoff 落盘，**可进入 generate-chapter** |
| `_briefs/chapter-{N}-brief.md` | 写作简报已产出 |
| `chapters/chapter-{N}.md` | AI 生成章节已落盘 |
| `_reviews/chapter-{N}-review.md` | 综合评审完成 |
| `_reviews/chapter-{N}-fix-log.md` | Fix 循环记录（最多 2 轮） |
| `_exchanges/scene-summaries.json` | 200 字结构化场景摘要 |
| `_exchanges/call-params.md` / `agent-result.md` | 复杂参数 / 结构化结果磁盘传递 |

所有产物含 frontmatter 版本标记（`format_version` / `produced_by` / `produced_at` / `chapter`）。handoff 8 字段契约见 [`interaction-spec.md` §2.4](framework/_specs/interaction-spec.md)。

## 稿件两层体系

| 层 | 目录 | 性质 | 修改权限 |
|----|------|------|---------|
| 临时中转 | `novel/_import/{ts}/` | 导入外部成稿暂存 | 流程结束可删，不备份 |
| 正式层 | `novel/` 根设定 + `novel/_changes.md` + `novel/_character-state.md` + `novel/chapters/` | 静态设定 + 正式增量日志 + 已发布章节正文 | 机械写入（publish/merge）/ 人工慎改 |
| 草稿层 | `novel/_drafts/`（扁平化，单份，贯穿全书） | 工作产物 + 草稿增量 | 自由 |

草稿**不镜像设定文件**——只存工作产物 + 增量日志（`_changes.md` / `_character-state.md` / `_edit-history.md`，append-only，merge 打 `merged_at` 不清空）。设定读写全部走 `settings-manager read-settings`（双源合并 `novel/` + `{draft}/_changes.md`），草稿无设定副本。单草稿约束：固定路径 `novel/_drafts/`，无日期目录无 `_index.md`，贯穿全书复用。publish 是正式层的单次合并写入（章节 sync + 设定 merge + 日志追加），用两阶段暂存-提交保证原子性；publish 后草稿章节正文删除，伴生工件 + `_edit-history.md` 归档到 `_archive/chapter-{N}/`。正式层 `_changes.md` 与设定文件双轨：文件存当前状态，日志存变更历史；**正式层设定文件不可手改**，pre-flight-check C11 检测 mtime 一致性。**设定时间线**：每条设定标注"引入章节"；评审/修改第 N 章时只参考引入章节 ≤ N 的条目；修改时向前扫描章节号 > 旧引入章节的章节是否冲突。冲突分级：🔴 必须修 / 🟡 应修。详细操作见 `settings-manager` Skill。

## 降级策略

所有 Skill 在发现所需文件缺失时：(1) 先补齐——调 `file-manager` (ensure-draft / ensure-novel) 尝试从上层补齐；(2) 补齐失败才降级——明确标注"⚠️ 文件 X 缺失：能力 Z 已降级为 Y"；(3) 降级不静默——每次降级在阶段输出中体现。**阻断等级**：🚫 硬阻断（`author-voice.md` 缺失→禁止进入简报生成）/ 🟡 软阻断（角色档案大面积缺失→警告+用户确认放行）/ ⚠️ 提醒（参考指南缺失→标注影响范围，不阻断）。`ask-yiyi` 会话启动自动调 `migration-keeper` 执行格式检测 + 兼容性检查，发现旧格式时引导一键迁移。

## 当前状态

> 项目状态（章节进度/活跃草稿/工作流阶段）由 `ask-yiyi` Skill 每次会话启动时自动加载：执行 detect-format → check-compat → sync-enrich → 读取进度 + 扫描工件；返回草稿目录路径 + 当前进度 + 工作流状态 + 格式/兼容性警告；项目未初始化则自动触发 `file-manager` (ensure-novel)。**不要在 CLAUDE.md 硬编码状态**——会 stale，与 ask-yiyi 冲突。
