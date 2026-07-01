---
description: 22 个 Skill 的 1 行简介 + 路径索引——避免 Skill tool 返回完整 SKILL.md 占用 context
---

# Skill 索引（2026-07-01 修复 #9）

> **问题**：每次调 Skill tool，平台返回完整 SKILL.md（数千字）——22 skill × 多次调用 = context 大量消耗。
> **解决**：本文件提供 1 行简介 + 路径，agent 优先看本文件判断 skill 是否需要，调时再读完整 SKILL.md。

## Skill 22 个（按使用场景分组）

### 写作链（plan → generate → review → publish）

| Skill | 一句话 | 路径 |
|-------|--------|------|
| `ask-yiyi` | 会话入口 + 状态扫描 + 菜单路由 | `.claude/skills/ask-yiyi/SKILL.md` |
| `plan-chapter` | 章节规划（pre-flight + 设定快照 + qing-novelist + handoff）| `.claude/skills/plan-chapter/SKILL.md` |
| `generate-chapter` | 章节生成（mo-writer → sensory-writer → chapter-review + Fix 循环）| `.claude/skills/generate-chapter/SKILL.md` |
| `chapter-review` | 章节评审（ping-critic 综合 + 5 维评审基线 + opus-dna 5 自检）| `.claude/skills/chapter-review/SKILL.md` |
| `publish-chapter` | 发布（settings-manager merge + ping-critic publish-verify）| `.claude/skills/publish-chapter/SKILL.md` |
| `qing-novelist` | 12 维启发式交谈（方向卡产出）| `.claude/skills/qing-novelist/SKILL.md` |

### 内容生产

| Skill | 一句话 | 路径 |
|-------|--------|------|
| `mo-writer` | 7 层写作简报生成 | `.claude/skills/mo-writer/SKILL.md` |
| `sensory-writer` | 写作执行（4 Step 协议——agent 自己执行）| `.claude/skills/sensory-writer/SKILL.md` |
| `idea-explorer` | 头脑风暴（7 种发散方法）| `.claude/skills/idea-explorer/SKILL.md` |
| `voice-sculptor` | 角色声音实验（A/B/C/D 4 模式）| `.claude/skills/voice-sculptor/SKILL.md` |
| `technique-selector` | 技法智能匹配 | `.claude/skills/technique-selector/SKILL.md` |
| `yin-illustrator` | 场景图像设计 | `.claude/skills/yin-illustrator/SKILL.md` |

### 评审/分析

| Skill | 一句话 | 路径 |
|-------|--------|------|
| `ping-critic` | 编辑顾问/综合评审（心流五维 18 项 + AI 指纹 + 校对）| `.claude/skills/ping-critic/SKILL.md` |
| `fingerprint-discovery` | AI 指纹发现（人机协同）| `.claude/skills/fingerprint-discovery/SKILL.md` |

### 系统管理

| Skill | 一句话 | 路径 |
|-------|--------|------|
| `pre-flight-check` | 前置就绪检查（C0-C11 门禁）| `.claude/skills/pre-flight-check/SKILL.md` |
| `settings-manager` | 设定全生命周期管理（read/record/init/merge）| `.claude/skills/settings-manager/SKILL.md` |
| `file-manager` | 文件补齐（ensure-novel / ensure-draft / ensure-frontmatter）| `.claude/skills/file-manager/SKILL.md` |
| `migration-keeper` | 文件体系检测与迁移 | `.claude/skills/migration-keeper/SKILL.md` |

### 编排/特殊

| Skill | 一句话 | 路径 |
|-------|--------|------|
| `outline-tingle` | 大纲形成（2 session）| `.claude/skills/outline-tingle/SKILL.md` |
| `xuanji` | 碎片收敛 grilling | `.claude/skills/xuanji/SKILL.md` |
| `bootstrap-project` | 冷启动工作流 | `.claude/skills/bootstrap-project/SKILL.md` |
| `import-chapter` | 多格式章节导入 | `.claude/skills/import-chapter/SKILL.md` |
| `adaptation-workflow` | 改编项目工作流 | `.claude/skills/adaptation-workflow/SKILL.md` |
| `spark` | 碎片想法捕获 | `.claude/skills/spark/SKILL.md` |

## 可执行脚本（.claude/skills/scripts/）

> **2026-07-01 修复 #1**：以下 skill 已有可执行 Python 脚本，agent 可直接 `python3 scripts/X.py` 调用，不必通过 Skill tool。

| 脚本 | 等价 Skill | 用法 |
|------|-----------|------|
| `pre-flight-check.sh` / `.py` | pre-flight-check | `python3 .claude/skills/scripts/pre-flight-check.py <draft_dir> <chapter> [scope]` |
| `settings-manager-record-handoff.py` | settings-manager record-handoff | `python3 .claude/skills/scripts/settings-manager-record-handoff.py <handoff_path>` |
| `fingerprint-tracker.py` | generate-chapter 2b-gate | `python3 .claude/skills/scripts/fingerprint-tracker.py <chapter_md> [output_json]` |

## 何时用 Skill vs 何时用脚本

| 场景 | 优先用 | 原因 |
|------|--------|------|
| **判断/门禁**（pre-flight / record-handoff / fingerprint）| **脚本** | 纯逻辑判断，0 LLM 推理消耗，结果可重复 |
| **创作/生成**（sensory-writer per-scene / qing-novelist 12 维）| **Skill（agent 推理执行）**| 需要 LLM 创作判断，脚本化意义不大 |
| **需要审阅/决策**（chapter-review / 评审）| **Skill（agent 推理执行）**| 需 LLM 解释 + 决策，agent 比脚本更灵活 |
| **E2E 验证/自动化** | **脚本** | 可重复执行，输出可断言 |

## 修复历史

- **2026-07-01 修复 #9**：原 22 个 skill 全部通过 Skill tool 调用，每次返回完整 SKILL.md 描述。22 skill × 多次调用 = 大量 context 消耗。修复：本 `_loader.md` 提供 1 行简介 + 路径，agent 优先查本文件判断。
- 已知限制：本文件是**提示**，不是 Skill tool 行为的硬约束。Skill tool 仍会返回 SKILL.md。要真正减少 context，需要平台层支持（未实现）。
