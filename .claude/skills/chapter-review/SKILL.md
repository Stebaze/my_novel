---
name: chapter-review
description: 章节评审与修改引导——3 mode 编排：writing（人工写章节）/ ai-content（AI 生成章节+场景级机器化校验）/ adaptation（改编章节）。edit-article 范式：评审报告按「问题段落 → 问题类型 → 修复指令」信息流图组织
---

# Chapter Review — 章节评审编排

> **edit-article 范式**：评审报告以「问题段落 → 问题类型 → 修复指令」三列流式呈现；每个问题描述不超过 240 字（避免 context 堆积）。场景级定位字段 `scene_index` 是 ai-content 模式 Fix 循环精准重写单场景的依据。
>
> **本 Skill 与 ping-critic 的合并关系**：自 2026-06-24 起，AI 指纹检测 + 校对（ling-reader 原能力）已并入 ping-critic。本 Skill 调 ping-critic 一次完成指纹+校对+心流+三维评审。

## Identity

章节评审流程的编排入口。负责确定评审目标、检查产出物状态、获取设定快照、调用 ping-critic 执行评审、呈现结果。**不直接执行评审算法**——评审逻辑（心流五维 18 项、AI 指纹归因、5 项机器化校对、三维评审、DoD 检查）全部由 ping-critic 完成。

## Contract

| Aspect | Detail |
|--------|--------|
| **Calls** | `settings-manager`（read-settings）, `ping-critic`（comprehensive-review） |
| **Produces** | `_reviews/chapter-{N}-review.md` |
| **Modes** | `"writing"`（人工写章节）/ `"ai-content"`（AI 生成章节+机器化校验）/ `"adaptation"`（改编章节） |

## Triggers

- "评审第X章" / "检查第X章" / "review第X章"
- "第X章写完了" / "改好了"（评审继续）

## Flow

### Step 1: Resolve Context

```
0. 扫描 novel/_drafts/ → 最新日期 → draft_dir
   ├── 有草稿 → draft_dir = 最新日期目录
   └── 无草稿 → 使用 novel/ 路径（降级）
1. 从 notes.md「当前进度」节提取「上次写到」字段 → 交叉验证用户指定 N
2. 解析 mode（默认 "writing"；从 generate-chapter 调用时为 "ai-content"）
```

### Step 2: Check Artifacts → Route

```
1. {draft_dir}/chapters/chapter-{N}.md 无正文？
   → "请先完成写作。" → 返回
2. {draft_dir}/_reviews/chapter-{N}-review.md 已存在？
   → 呈现报告概要 + 提示"回复「改好了」重新评审 /「定稿」"
3. 不存在 → 调 settings-manager (read-settings, target_chapter={N})
   → 写入 {draft_dir}/_exchanges/settings-snapshot.md
   → 失败 → 🚫 硬阻断（无设定快照无法做一致性检查）
4. [mode="ai-content"] 解析 {draft_dir}/_exchanges/scene-summaries.json
   → 不存在 → ⚠️ 标注"AI 专项检查降级为纯文本评审（Fix 循环无法精准定位）"
5. [mode="adaptation"] 加载 {source_portrait_path} 作为额外评审基准
   → 对齐级别（严格/平衡/宽松）由用户在评审前选择
```

### Step 3: Call ping-critic

调 `Skill("ping-critic", operation="comprehensive-review", mode={mode})` 一次完成：

- **基础能力**（所有 mode）：心流五维 18 项检测 + 加载指纹归因 + 加载校对结果 + 三维评审（结构/角色设定/文本质地） + DoD 检查
- **mode="ai-content" 额外**：5 项机器化校验（事件落地 / 场景连贯 / 突兀收束 / POV 连续 / 伏笔核对）——🔴 项必须含 `scene_index` 字段供 generate-chapter Step 4 Fix 循环精准定位
- **mode="ai-content" 额外**：opus-dna 5 自检（删减 / 替换 / 出声 / So-what / AI 味）——与 18 项心流检测解耦，不污染心流评级；AI 味行直接引用上方指纹区不重复检测
- **mode="adaptation" 额外**：原作对齐检查（结构/设定/风格 fidelity）——按对齐级别判定

详细执行步骤、阈值表、检测算法、修复策略见 `ping-critic/_reference/flow-review-methodology.md` + `ling-detection-methodology.md`。

### Step 4: Present Result

```
评审报告路径：{draft_dir}/_reviews/chapter-{N}-review.md

呈现概要：
- 心流评级：顺畅 / 有摩擦 / 断裂 / 无法进入
- 🔴 项数量 + 关键问题摘要
- 🟡 项数量
- 校对统计（语病/错别字/标点/分段）
- DoD 状态（5 条）
- 🆕 新指纹候选（如有）

报告组织（edit-article 范式）：
| 问题段落（scene/line）| 问题类型 | 修复指令 |
|---------------------|---------|---------|
| scene 2, para 4 | 叙述者解码（指纹 5）| 入身改写：脚底→胸口→动作 |
| ... | ... | ... |

🆕 新指纹候选区（如有候选）：
| 位置 | 候选模式 | 置信度 | 读者效应 | 触发信号 |
|------|---------|--------|----------|---------|
| scene 2, para 4 | AI 总结式叙述 | 🟢 0.78 | 读起来像 AI 写的总结 | V7, 描述独特 |
| ... | ... | ... | ... | ... |

opus-dna 5 自检（**仅 mode="ai-content"** 渲染）：

| 自检项 | 状态 | 引用段落 | 修复指令 |
|-------|-----|---------|---------|
| 删减 | pass / partial / fail | scene X para Y | [具体删除哪句] |
| 替换 | pass / partial / fail | scene X para Y | [改用什么更短的方式] |
| 出声 | pass / partial / fail | scene X para Y | [哪句不像人话] |
| So-what | pass / partial / fail | scene X para Y | [读者会卡在哪个"然后呢"] |
| AI 味 | pass | 参见上方指纹区 | — |

> 5 自检 fail 项生成新的 `fix_issues` 列表注入 generate-chapter Step 4——sensory-writer 重写时通过元认知层显式对冲。

提示作者：
  "根据报告修改后回复「改好了」重新评审。
   确认无误后回复「定稿」更新设定。
   对新指纹候选：
   - 回复「确认指纹 N 是新模式」→ 一键调用 fingerprint-discovery analyze，evidence 自动传入
   - 回复「这不是 AI 问题」→ 标记 dismissed，关闭候选"
```

### Step 5: Finalize（用户回复「定稿」时触发）

```
1. 调 settings-manager (record-settings) → 更新 _changes.md
2. 调 settings-manager (record-character-state) → 更新 _character-state.md
3. 更新 notes.md 进度 + outline.md 状态
4. 同步更新 thread-map.md（伏笔/支线/线索交汇操作）
   ├── 伏笔操作：埋设（新增 🌱）/ 推进（更新"最近推进"）/ 回收（状态→✅）
   ├── 支线操作：新增 / 推进
   └── 线索交汇：新增行（如本章多线交汇）
   → thread-map.md 不存在 → ⚠️ 跳过，不阻断定稿
5. 提示："设定已更新。可以发布了吗？"
```

---

## Author Self-Service

| 操作 | 触发 | 效果 |
|------|------|------|
| 局部重审 | "只查场景三" | ping-critic 仅对指定范围执行评审 |
| 问题展开 | "问题 3 展开说说" | 对单个问题给更详细修改方向 |
| 放弃修改 | "这个问题不改了" | 标记"作者确认不修改"，不阻塞定稿 |
| 直接定稿 | "可以了，定稿" | 调 Step 5 finalize |
| **确认新指纹** | "确认指纹 N 是新模式" | 调 `Skill("fingerprint-discovery", input_mode="from-candidate", candidate={location, evidence, reader_effect, suggested_pattern, confidence, triggering_signals})` — evidence 自动传入 |
| **关闭候选** | "这不是 AI 问题" | 在评审报告标记该候选 dismissed，关闭候选不阻塞定稿 |

---

## Completion Criterion

- ✅ Checkable：返回 `{review_file, red_count, yellow_count, flow_rating, dod_pass_rate, new_fingerprint_candidates_count, fingerprint_candidates_dismissed_count}` + 评审报告落盘至 `_reviews/chapter-{N}-review.md`
- ✅ Exhaustive：所有 Flow Step 执行完毕；mode-specific 校验（ai-content 5 项 / adaptation 原作对齐）已执行
- 🚫 Stop：呈现报告概要后不调用其他写作/生成 Skill——等用户输入「改好了」/「定稿」

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `ping-critic` Skill | Step 3（综合评审，含原 ling-reader 指纹+校对能力） | 🚫 硬阻断——评审算法已完全并入 ping-critic |
| `settings-manager` Skill | Step 2（设定快照）、Step 5（定稿） | 🚫 硬阻断——无设定快照无法做一致性检查 |
| `{draft_dir}/chapters/chapter-{N}.md` | Step 2 | 🚫 硬阻断——无正文无法评审 |
| `{draft_dir}/_briefs/chapter-{N}-brief.md` | Step 2 | ⚠️ 标注"无简报基准"，仅基于常识判断 |
| `{draft_dir}/_exchanges/scene-summaries.json` | Step 2（mode="ai-content"） | ⚠️ AI 专项检查降级为纯文本评审（Fix 循环无法精准定位单场景） |
| `{source_portrait_path}` | Step 2（mode="adaptation"） | 🚫 硬阻断——原作画像缺失无法做对齐检查 |
