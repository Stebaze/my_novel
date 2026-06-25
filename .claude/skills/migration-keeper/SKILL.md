---
name: migration-keeper
description: 文件体系检测与迁移——格式检测+兼容性检查+内容盘点+完整迁移管道
---

# Migration Keeper — 文件体系检测与迁移

## Identity

你是文件体系检测与迁移的执行者。**职责是检测判定 + 多步骤迁移编排**——格式状态分级、兼容性 gap 分级、内容盘点、迁移管道驱动。**不做补齐**——补齐是 `file-manager` Skill 的职责。

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | `ask-yiyi` Skill（会话启动管道）、`file-manager` 降级路径、用户直接调用 |
| **Calls** | `file-manager` Skill（migrate-project 时 create-backup + ensure-novel + ensure-frontmatter） |
| **Input** | `operation`, `target`（`novel` / `draft:{dir}` / `both`） |
| **Output** | 检测报告 + 分级判定 + 迁移报告文件 |

## Triggers

- `ask-yiyi` 会话启动时调 detect-format / check-compat / sync-enrich
- 文件结构异常时（`migration-keeper` 任何操作都可被用户直接调用）
- `migrate-project` 触发完整迁移管道

## Operations

| Operation | 责任 |
|-----------|------|
| **detect-format** | 六维加权检测 → CURRENT / CURRENT_UNMARKED / VERSION_GAP / PARTIAL_MIGRATION / FULL_MIGRATION_NEEDED / NO_PROJECT |
| **check-compat** | 结构签名对比 → 🔴/🟡/🟢 gap 分级报告 |
| **analyze-content** | 章节/角色/世界/草稿/游离文件清单（用于迁移前评估） |
| **migrate-project** | 备份→盘点→结构迁移→草稿迁移→验证（6 阶段管道） |

## Execution

### Discovery

```
1. 读 framework/.framework-version → FORMAT_VERSION（缺失视 v2 + ⚠️）
2. 查 novel/.novel-version → 匹配则走快速路径；否则启发式六维评分
3. 草稿在 → target 可含 draft:{dir}
```

### detect-format

六维加权评分（结构 25% / 核心文件 30% / 世界设定 15% / 草稿管理 15% / 章节命名 10% / 追踪文件 5%）：

| composite | 状态 | 处理 |
|-----------|------|------|
| ≥ 0.85 + 未标记 | CURRENT_UNMARKED | 写 `novel/.novel-version` 后通过 |
| 0.50–0.85 | PARTIAL_MIGRATION | 输出摘要 + 询问 Y/V/N |
| < 0.50 | FULL_MIGRATION_NEEDED | 同上 |
| 0.85 + 已标记 | CURRENT | 静默通过 |
| novel/notes.md 不存在 | NO_PROJECT | 返回供 ask-yiyi 调 ensure-novel |

### check-compat

```
1. 对每个实例文件：从 framework/templates/ 提结构签名（##/###/字段名/表格头）
2. 从实例文件提签名 → 对比（模板有/实例无 = GAP）
3. 分级：
   🔴 Breaking — 活跃 Skill 硬依赖
   🟡 Degradation — 有功能引用但可降级
   🟢 Nice-to-have — 模板新增无活跃强依赖
4. 输出分级清单 + 建议操作
```

### analyze-content

扫描 6 类：章节（命名/字数/编号）/ 角色（数量/格式）/ 世界（分类）/ 草稿（VALID/INCOMPLETE/LEGACY）/ 游离文件（不在标准清单的 .md）/ 追踪文件（thread-map/character-arcs 存在性）→ 结构化清单。

### migrate-project

完整 6 阶段管道：

```
1. 展示迁移计划（类型/源格式/目标格式/缺失维度/备份位置）→ 用户确认
2. create-backup（调 file-manager）→ 验证通过才继续；失败 🚫 中止
3. analyze-content（用本 skill 内部分析逻辑）
4. migrate-structure：
   Case A（composite ≥ 0.85）→ ensure-novel + check-compat + ensure-compat + sync-enrich
   Case B（composite < 0.85）→ 全新初始化 + 内容映射
     - 章节迁移（重命名+边界检测，调 import-chapter）
     - 角色档案迁移（格式对齐）
     - 世界观文件迁移
     - 配置/笔记/大纲迁移（大纲永不自动合并）
     - 追踪数据从旧 outline.md 提取
5. migrate-drafts：修复草稿目录结构
6. validate-migration：结构（15 实例文件）+ 兼容（check-compat）+ 内容（章节/角色/世界数量一致）+ 写 .novel-version
7. 输出迁移报告
```

## Output

所有模式返回结构化报告。`migrate-project` 额外产出迁移报告文件，frontmatter 含 `format_version` / `produced_by` / `produced_at` / `chapter`。

## Completion Criterion

- ✅ Checkable：被调用的 operation 已返回结构化报告（detect-format 状态分类 / check-compat 分级清单 / analyze-content 结构化清单 / migrate-project 迁移报告文件已落盘）
- ✅ Exhaustive：migrate-project 6 阶段全部执行（任一中断需报告原因），其他 op 的 Discovery + 子步骤完整
- 🚫 Stop：返回报告后不继续调用其他 Skill（除非 migrate-project 内部编排 file-manager）

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `file-manager` Skill | migrate-project（备份+补齐） | 🚫 迁移中止 |
| `import-chapter` Skill | migrate-structure Case B（章节拆分） | 🚫 硬阻断——Case B 不可用 |
| `framework/.framework-version` | detect-format | ⚠️ 视为 v2，标注缺失 |
| `framework/guides/reference-material.md` | sync-enrich | ⚠️ 内容富化跳过 |
