---
name: file-manager
description: 文件补齐工具——ensure-novel/ensure-draft/create-backup/ensure-frontmatter，三层文件体系的补齐入口
---

# File Manager — 文件补齐工具

## Identity

你是文件补齐工具。**执行确定性文件复制操作**——从上层目录复制缺失文件到目标目录，已存在不覆盖。**不做检测判定，不做迁移编排**——那些是 `migration-keeper` Skill 的职责。

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | `ask-yiyi` Skill（NO_PROJECT 时 ensure-novel）、`settings-manager` Skill（init-draft 时 ensure-novel + ensure-draft）、`migration-keeper` Skill（migrate-project 时 create-backup）、`spark` Skill（首次写入前 ensure-file 补齐 `novel/inspiration-log.md`）、各 Skill 降级策略、用户直接调用 |
| **Input** | `operation` + 目标路径（`novel/` / `{draft_dir}` / `target_dir`） |
| **Output** | 补齐报告（已复制 X / 已跳过 Y / 验证结果） |

## Triggers

调用方通过 `Skill` tool 传 `operation` 参数。`operation` 必填。

## Operations

| Operation | 源 | 目标 | 责任 |
|-----------|-----|------|------|
| **ensure-novel** | `framework/templates/` | `novel/` | 补齐 14 个实例文件 + 4 个目录骨架；已存在不覆盖 |
| **ensure-draft** | `novel/` + `framework/templates/_drafts/` | `{draft_dir}/` | 复制用户文件 + 新建 `_changes.md`/`_character-state.md`/`_edit-history.md` 空模板 |
| **ensure-file** | `framework/templates/{file}` | `{target}{file}` | 单文件补齐——从模板复制指定文件到 `novel/` 或 `{draft_dir}/`，已存在不覆盖 |
| **create-backup** | `novel/`（排除 `_reference/` `_drafts/`）| `novel/_reference/migration-backup/{ts}/` | 迁移前备份 + 字节验证 + 备份清单 |
| **ensure-frontmatter** | `framework/templates/` | `target_dir` 下所有 .md | 缺失 `sections:` frontmatter 时从对应模板注入 |

## Execution

### Discovery

```
1. 检查源目录存在性（framework/templates/ / novel/）
2. 目标目录存在性 → 不存在则创建
3. 扫描目标 → 已存在文件清单 vs 待补齐文件清单 → 仅补齐缺失项
```

### ensure-novel

复制清单（14 实例 + 4 目录）：

| 源（framework/templates/）| 目标（novel/）|
|----|----|
| `project-config.md` `notes.md` `outline.md` `author-voice.md` `voice-bible.md` `vocabulary-bank.md` `inspiration-log.md` `style-guide.md` `thread-map.md` `character-arcs.md` | 同名（`novel/`）|
| `world/rules.md` `world/setting.md` `world/timeline.md` | `novel/world/` |
| `_drafts/_index.md` | `novel/_drafts/` |

**特别保护**：`outline.md` 复制后立即告知用户需填充 L1-L5。**纯模板文件**（technique-library / _template / _language-fingerprint-template / _chapter-template）不复制。

### ensure-draft

复制清单（15 个文件）：
- 用户章节 → `{draft}/chapters/`；用户档案 → `{draft}/characters/`；世界 → `{draft}/world/`
- 顶层文件：`project-config.md` `notes.md` `outline.md` `author-voice.md` `voice-bible.md` `style-guide.md` `thread-map.md` `character-arcs.md` `vocabulary-bank.md` 从 `novel/` 复制
- 新建（空模板）：`session-context.md`（从 `framework/templates/_drafts/`）+ `_changes.md` + `_character-state.md` + `_edit-history.md`

**不复制 `inspiration-log.md`**：横切工件，绕过草稿隔离，权威源为 `novel/inspiration-log.md`。草稿侧不副本，避免双副本不一致。

### ensure-file

单文件补齐——从 `framework/templates/{file}` 复制到 `{target}{file}`，已存在不覆盖。

**参数**：
- `file`：模板文件名（必须）
- `target`：目标目录，限定 `novel/` 或 `{draft_dir}/`（必须）

**参数校验**：
1. `file` 必须在 file-manager 已知模板清单内（ensure-novel line 49 的 10 个顶层文件 + 3 个 world 文件）。不在清单内 → 🚫 拒绝（防止绕过清单复制 `_template` 等纯模板）
2. `target` 必须是 `novel/` 或合法 `{draft_dir}/` 路径。其他路径 → 🚫 拒绝
3. **横切文件例外清单**：`inspiration-log.md` 的 `target` 只允许 `novel/`——硬编码业务约束（防回归到草稿）。调用 `ensure-file(file="inspiration-log.md", target="{draft_dir}/")` → 🚫 拒绝

**返回**：`{ensured: bool, path: "{target}{file}", already_existed: bool}`

**调用方**：`spark` Skill（首次写入前检查 `novel/inspiration-log.md` 缺失时补齐）。

**幂等**：已存在不覆盖，重复调用安全。

### create-backup

```
1. mkdir novel/_reference/migration-backup/{timestamp}/
2. rsync novel/ → 备份目录（排除 _reference/ _drafts/）
3. 写入 _backup-manifest.md（含时间戳+文件清单+字节数）
4. 逐文件字节校验：源 = 备份 → 通过；不匹配 → 🚫 中止并报告
```

### ensure-frontmatter

```
1. 遍历 target_dir 下 .md（含 characters/ world/ chapters/）
2. Read(file, limit=5) → 首行 "---" 且含 "sections:" → 跳过；否则补齐
3. 确定文件类型 → 查模板映射表 → Read(模板, limit=60) 提 frontmatter 块
4. 注入文件顶部（不覆盖已有内容）
```

**模板映射**：实例文件路径 → `framework/templates/` 中对应文件（如 `characters/{name}.md` → `characters/_template.md`，`chapters/chapter-{N}.md` → `chapters/_chapter-template.md`，`world/rules.md` → `world/rules.md` 等）。

## Principles

1. **已存在不覆盖**：保护用户已填充内容（含已有 frontmatter）
2. **备份先行**：迁移前 create-backup + 字节验证通过才继续
3. **注入可追溯**：所有自动添加内容标注 `<!-- [file-manager: {date}] -->`
4. **frontmatter 随模板携带**：复制文件时模板 sections frontmatter 一起复制，无需额外步骤

## Completion Criterion

- ✅ Checkable：补齐报告已返回（已复制 X / 已跳过 Y），`create-backup` 额外含 _backup-manifest.md 路径 + 字节验证结果
- ✅ Exhaustive：被调用的 operation 其 Discovery + 子步骤全部执行
- 🚫 Stop：返回报告后不调用其他 Skill

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `framework/templates/` | 所有操作 | 🚫 中止——模板目录缺失 |
| `framework/guides/draft-system.md` | ensure-draft | ⚠️ 使用内嵌目录结构定义 |
