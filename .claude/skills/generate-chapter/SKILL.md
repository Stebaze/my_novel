---
name: generate-chapter
description: 章节生成编排（4-Skill 对称架构 Session 2）——plan 阶段 handoff 之后，串接 mo-writer（简报）→ sensory-writer per-scene（场景生成 + 200字摘要 + 自动拼装）→ chapter-review ai-content（自动评审）→ 最多 2 轮 Fix 循环，一气呵成产出 AI 章节
---

# Generate Chapter — 章节生成编排

## Identity

你是 4-Skill 对称架构的 Session 2 编排入口。`plan-chapter` 阶段 5 写完 handoff 后，用户在新会话中输入 `/generate-chapter {N}` 触发本 Skill。**你只编排不创作**——串接 3 个工具型 Skill：mo-writer（简报）→ sensory-writer（per-scene）→ chapter-review（ai-content 评审）→ 最多 2 轮 Fix 循环。

**入口硬检查**：启动时必须先验证 `{draft_dir}/_briefs/chapter-{N}-handoff.md` 存在并 8 字段契约完整。缺失或字段无效 → 🚫 硬阻断。

## Contract

| Aspect | Detail |
|--------|--------|
| **Trigger** | `/generate-chapter {N}` / `--resume`（断点续跑）/ `--resume-from={step}`（显式跳步） |
| **Calls** | `pre-flight-check`（C8 handoff 验证）, `settings-manager`（read-character-state）, `mo-writer`（Step 1 简报）, `sensory-writer`（Step 2 + Step 4 per-scene）, `chapter-review`（Step 3, mode="ai-content"）, `file-manager`（Step 0 兜底） |
| **Produces** | `_briefs/chapter-{N}-brief.md` + `chapters/chapter-{N}.md` + `_reviews/chapter-{N}-review.md` + `_reviews/chapter-{N}-fix-log.md`（条件）+ `_exchanges/scene-summaries.json` |

## Triggers

- `/generate-chapter {N}`（handoff 提示引导的主入口）

**前置条件**：`{draft_dir}/_briefs/chapter-{N}-handoff.md` 已由 plan-chapter 阶段 5 落盘。

## Flow

### 5-Step Pipeline

```
Step 0: Pre-Flight C8    → 验证 handoff 契约（🚫 硬阻断）+ 角色状态快照 + 续跑路由
Step 1: Brief Generation → mo-writer → _briefs/chapter-{N}-brief.md
Step 2: Per-Scene + Assemble → sensory-writer per-scene + 200字摘要 + 自动拼装 → chapters/chapter-{N}.md
Step 3: Auto Review      → chapter-review (mode="ai-content", auto=true) → _reviews/chapter-{N}-review.md
Step 4: Fix Loop (≤2)    → 仅 🔴 项时进入；精准重写受影响场景 → _reviews/chapter-{N}-fix-log.md
Step 5: Finalize         → 落盘 4 文件 + handoff.workflow_position = "generate-step5-done"
```

**硬约束**：Fix 循环 ≤ 2 轮（spec 锁定）—— 2 轮后仍有 🔴 → 强制退出，提示人工修订。

### Step 0: Pre-Flight C8 + Resolve Handoff

```
0. 解析命令参数：
   ├── {N}             → 首次（走完整 Step 1-5）
   ├── {N} --resume    → 读 handoff.workflow_position 自动定位目标 Step
   └── {N} --resume-from={step} → 强制从 step ∈ {0,1,2,3,4,5} 开始（调试用）

1. 扫描 novel/_drafts/ → 最新日期 → draft_dir（无草稿 → 调 file-manager ensure-draft 兜底）

2. 验证 handoff 存在：
   ├── 缺失 → 🚫 硬阻断"Ch{N} handoff 缺失——必须先调 plan-chapter"
   └── 存在 → 进入步骤 3

3. 调 Skill("pre-flight-check") → 必跑 C8 handoff 字段契约（其余 C0-C7.5 按需）
   → 🚫 硬阻断：列出 🚫 项 + 修复路径

4. 调 Skill("settings-manager", operation="read-character-state") → 截止 Ch{N-1} 角色状态

5. 续跑路由（仅 --resume / --resume-from）：
   ├── 首次 → 走完整 Step 1-5
   ├── --resume → 查续跑路由表 → 跳到目标 Step（workflow_position 异常 → 🚫）
   └── --resume-from={step} → 验证 step ∈ {0,1,2,3,4,5} → 强制从该 step 开始
```

**续跑路由表**（`--resume` 自动定位）：

| handoff.workflow_position | 续跑目标 | 跳过 |
|--------------------------|---------|------|
| `plan-step5-handoff` | Step 1 | 无 |
| `generate-step1-brief` | Step 2 | Step 1 |
| `generate-step2-scenes` | Step 3 | Step 1-2 |
| `generate-step3-reviewed` | Step 4 | Step 1-3 |
| `generate-step4-fix1` | Step 4 Round 2 | Step 1-3 + Round 1 |
| `generate-step4-fix2` | Step 5 | Step 1-4 |
| `generate-step5-done` | 流程结束 → 提示 `/chapter-review {N}` | 全部 |

### Step 1: Brief Generation

```
调 Skill("mo-writer")
  传入：chapter={N}, draft_dir, direction_file（从 handoff.direction 读取）, output_format
  → 产出 _briefs/chapter-{N}-brief.md + chapters/chapter-{N}.md（骨架）
  → 更新 handoff.brief + workflow_position = "generate-step1-brief"

判断：简报已存在（plan 阶段生成）→ 跳过本步骤直接进入 Step 2
降级：mo-writer 不可用 → 🚫 硬阻断
```

### Step 2: Per-Scene Generation + Auto Assembly

```
2a: 解析简报场景清单（§1 + §3）→ 提取 场景名/POV/时间地点/事件/对话/情绪节拍 + §2 角色声音 + author-voice.md
2b: 对每个场景调 Skill("sensory-writer", mode="per-scene")
    → 返回 prose + summary_200（结构化 JSON：scene_index/name/pov/core_event/key_actions/key_dialogue/pov_state_change/ending_state/next_link/foreshadow_touched）
    → 写入 _exchanges/scene-summaries.json
    → 单场景失败 → 重试一次，仍失败 → 🚫 硬阻断（不允许部分章节）
2c: 自动拼装 → chapters/chapter-{N}.md（保留元数据头 + 场景按 §1 顺序拼接 + 200 字摘要折叠块）
    → 更新 scene-summaries.json "assembled": true
```

### Step 3: Auto Review (ai-content mode)

```
调 Skill("chapter-review", mode="ai-content", auto=true)
  传入：chapter={N}, draft_dir, scene_summaries={draft_dir}/_exchanges/scene-summaries.json
  → 内部执行：ping-critic（指纹+校对+心流五维18项+三维评审）
  → AI 专项检查：事件落地 / 场景连贯 / 突兀收束 / POV 连续 / 伏笔核对
  → 产出 _reviews/chapter-{N}-review.md + 🔴 项场景定位列表

解析评审：
├── 无 🔴 项 → ✅ 通过，跳过 Step 4
├── 🔴 ≤ 2 且定位明确 → 进入 Step 4
└── 🔴 > 2 或定位模糊 → ⚠️ 警告 + 用户选择"进入 Fix 循环" / "人工修订"

降级：chapter-review 不可用 → 🚫 硬阻断
降级：mode="ai-content" 未实现 → ⚠️ 降级为 mode="writing" + 跳过 AI 专项检查
```

### Step 4: Fix Loop（最多 2 轮，spec 锁定）

```
Round 1（修复）：
  1. 从评审报告提取 🔴 项 + 场景定位（scene_index）
  2. 标记 scenes[scene_index].needs_rewrite = true + 记录原因
  3. 重调 Skill("sensory-writer", mode="per-scene") → 仅针对 needs_rewrite=true 的场景
     → 传入：上一版本 prose + 评审问题列表 + 上一版本 200 字摘要
  4. 更新 scene-summaries.json + 重新拼装章节
  5. 写 _reviews/chapter-{N}-fix-log.md：Round 1 修复（{ts}）+ 受影响场景/问题摘要/修复方式
  6. 触发 Step 3 重新评审

Round 2（验证）：
  1. 重新执行 Step 3
  2. 仍有 🔴 → 仅记录到 fix-log.md，不再次重写（已达 2 轮上限）→ 标记"进入人工修订阶段"
  3. 无 🔴 → ✅ 标记"Fix 循环完成"

退出条件：
  ├── ✅ 评审通过（无 🔴）
  ├── ⚠️ 2 轮已达上限仍有 🔴
  └── ⏹️ 用户中断
```

### Step 5: Finalize

```
1. 确认产出物完整：
   ├── _briefs/chapter-{N}-brief.md ✅
   ├── chapters/chapter-{N}.md ✅（含完整正文）
   ├── _reviews/chapter-{N}-review.md ✅
   ├── _exchanges/scene-summaries.json ✅
   └── _reviews/chapter-{N}-fix-log.md ✅（仅 Fix 循环执行时）

2. 更新 handoff：workflow_position = "generate-step5-done" + brief / chapter_file 路径

3. 呈现：章节正文路径 + 简报路径 + 评审报告路径 + Fix 轮次 + 提示
   "轻编辑后输入「定稿」或运行 /chapter-review {N} 复审。
    若需重新生成整章，输入 /generate-chapter {N} --resume"
```

## 跨 Session 状态外部化

每个 Step 完成后更新 `handoff.workflow_position`（`<skill>-<step>-<artifact>` 三段式），使断点续跑可定位。**双重保护**：主防线（路由表跳过已完成 Step）+ 副防线（Step 内部检查产出物存在性）。

## Completion Criterion

- ✅ Checkable：返回 4 落盘文件路径字典 `{brief, chapter, review, fix_log_or_null}` + fix 轮次数 `{rounds: 0|1|2}`
- ✅ Exhaustive：5 Step 全部执行（含条件 Fix），handoff.workflow_position 已更新为 "generate-step5-done"
- 🚫 Stop：呈现最终摘要后不调用任何写作或评审 Skill——等用户输入 `/chapter-review {N}` 进入人工复审

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `pre-flight-check` Skill | Step 0 | 🚫 硬阻断——C8 handoff 验证是入口门禁 |
| `settings-manager` Skill | Step 0 | 🚫 硬阻断——无角色状态无法保证连续性 |
| `mo-writer` Skill | Step 1 | 🚫 硬阻断——简报必须产出 |
| `sensory-writer` Skill | Step 2 + Step 4 | 🚫 硬阻断——章节正文必须产出 |
| `chapter-review` Skill | Step 3 | 🚫 硬阻断——无评审无法判定质量 |
| `file-manager` Skill | Step 0（兜底） | ⚠️ 草稿初始化失败时手动执行 |
| `{draft_dir}/_briefs/chapter-{N}-handoff.md` | Step 0 | 🚫 硬阻断 |
| `{draft_dir}/author-voice.md` | Step 2 | 🚫 硬阻断——无风格基准无法生成 |
| `framework/guides/ai-risk-mitigation.md` | Step 2 方法论 | ⚠️ 方法已内置，标注缺失 |
| `framework/guides/jung-character-framework.md` | Step 2 角色心理 | ⚠️ 降为基于档案常识判断 |
