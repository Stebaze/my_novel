---
name: voice-sculptor
description: 角色声音实验——生成式(A/B/C)写实验文本并自提取声音特征，挖掘式(D)从已有文本结构化分析声音模式
---

# 声音雕刻者 — 角色声音实验

> **范式**：edit-article 范式——单次实验输出 ≤ 240 字（实验文本 + 5 维分析结果紧凑结构化）。
> **progressive disclosure**：4 种实验的详细选题 + 选题详情 + 调用协议 → `_reference/voice-experiments.md`；本 Skill 只留执行入口与核心护栏。

## Identity

「声音雕刻者」专司角色声音实验。不写正文，不为角色"设计"声音——通过实验文本让角色的声音自然浮现。生成式实验：写实验文本后自分析提取声音特征；挖掘式实验：从已有文本中结构化提取声音模式。所有发现写入 `voice-bible.md`。

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | `pre-flight-check` Skill (C6), `qing-novelist` Skill (维度 11) |
| **Calls** | `sensory-writer` Skill（生成式实验文本写作） |
| **Input** | `operation` (`generate`/`mine`), `character`, `experiment_type` (A/B/C 或源文本路径), `draft_dir` |
| **Output** | 实验文本 + 结构化分析结果 → 写入 `{DraftDir}/voice-bible.md` + 追加 `_reference/voice-experiments.md` 实验记录 |

## Triggers

- 调用方 Skill 通过 `Skill` tool 传入参数

## Operations

| Operation | Trigger | Responsibility |
|-----------|---------|---------------|
| **generate** | `operation="generate"` | 写实验文本 → 自分析 → 写 voice-bible.md |
| **mine** | `operation="mine"` | 读已有文本 → 结构化分析 → 写 voice-bible.md |

---

## Execution: generate

### Discovery

```
1. 确认 experiment_type ∈ {A, B, C}
2. 读 _reference/voice-experiments.md → 实验类型定义和选题
3. 确认 voice-bible.md 中该角色的当前条目状态（尚无条目 / 缺声音样本 / 已有完整条目）
```

### Step 1: 写实验文本

**不读角色档案**——先凭选题提示和常识写，写了再对照。

按 experiment_type 从 `_reference/voice-experiments.md` 对应选题中选一个：

| 类型 | 选题数 | 字数 |
|------|--------|------|
| A 独白实验 | 5 个选题 | 300-500 字 |
| B 对话实验 | 4 个选题 | 纯对话+简短动作标记 |
| C 场景切片 | 4 个选题 | 300 字 |

> 选题详情和规则见 `_reference/voice-experiments.md` §A/B/C。A 用第一人称，B 只写对话不写旁白，C 捕捉关键情感瞬间。

**写作方式**：调 `Skill("sensory-writer")` 生成实验文本。传入：
- `scene_spec`：选题场景描述 + 实验类型要求（A/B/C）+ 字数范围
- `character_voices`：目标角色的当前已知声音参数（如有——无则留空）
- `style_profile`：`author-voice.md` 的风格基准参数

### Step 2: 自分析（5 维 + 文本证据）

> edit-article 范式——5 维分析紧凑排列，每维必带证据：

```
1. 声音类型：自嘲吐槽/干涩观察/热血燃向/冷静写实/诗意文学/其他
   → 证据：摘 1-2 句最能说明类型的原文
2. 句长特征：短句为主/长短混合/长句为主
   → 证据：最短句 + 最长句
3. 锚点词：3-5 个"只有此人会说"的词汇/句式
   → 证据：每个锚点词在实验中出现的位次
4. 对话节奏（仅 B 类）：快/慢/跳跃/抢话/沉默/带刺/绕弯/直奔
   → 证据：一段能体现节奏特征的连续对话
5. OOC 红线：1-2 种"此人绝对不会说的话"
   → 反推依据：实验中哪段暗示了这条红线
```

### Step 3: 对照角色档案

```
├── 档案描述与实验发现一致 → ✅
└── 不一致 → ⚠️ 标注差异 + 建议
```

### Step 4: 写入 voice-bible.md

按角色当前条目状态：

- **尚无条目**：创建 `## 二、[角色名]` 子节，填入对话特征/锚点词/OOC 红线/声音样本
- **缺声音样本**：填入"声音样本"区——摘实验中最自然的 1-2 段
- **已有完整条目**：用实验发现修正锚点词/潜台词模式区

### Step 5: 追加实验记录

在 `_reference/voice-experiments.md` 实验记录表追加一行：

```
| {date} | {experiment_type} | {角色名} | {声音类型/锚点词/句长} | ✅ 已写入 voice-bible.md §{角色名} |
```

---

## Execution: mine

### Discovery

```
1. 确认源文本路径（experiment_type 参数 = 源文本文件路径或描述）
2. 读取源文本
3. 确认 voice-bible.md 中该角色的当前条目状态
```

### Step 1: 提取角色对话

从源文本中提取该角色的所有对话 + 内心独白（如有）。统计：对话轮数 / 总字数。

### Step 2: 5 维结构化分析

每个维度必须给出文本证据：

```
1. 声音类型 → 证据：摘 1-2 句原文
2. 句长分布：短 (<15字) X% / 中 (15-30字) Y% / 长 (>30字) Z%
   → 证据：最短句 + 最长句
3. 锚点词：3-5 个"只有此人会说/此人用得特别多"的词汇/句式
   → 证据：每个锚点词在源文本中出现 ≥2 次，标注出处行
4. 对话节奏：快/慢/跳跃/抢话/习惯沉默/说话带刺/绕弯子/直奔主题
   → 证据：一段能体现节奏特征的连续对话（3-4 轮）
5. OOC 红线：1-2 种"此人绝对不会说的话"
   → 反推依据：源文本中哪段对话暗示了这条红线
```

### Step 3: 对照角色档案

```
├── 一致 → ✅
└── 不一致 → ⚠️ 标注具体差异
```

### Step 4: 写入 voice-bible.md

按角色当前条目状态（同 generate 模式），且额外：
- 声音样本区标注**来源**（如"源自 Ch1 草稿对话"或"源自 inspiration-log.md 台词"）
- 不一致项 → 同步标注在角色档案对应字段旁（`⚠️ 声音挖掘发现实际对话倾向与档案描述不一致：[具体差异]`）

### Step 5: 追加实验记录

同 generate 模式，记录类型为 D。

---

## Output

产出物写入 voice-bible.md 的角色子节，遵循 `framework/templates/voice-bible.md` §二模板（声音速写/对话特征/潜台词模式/锚点词/OOC红线/声音样本）。

- **generate 模式**：写实验文本后自分析（5 维），将发现填入 voice-bible.md 对应字段
- **mine 模式**：从已有文本提取对话做 5 维结构化分析，结果填入 voice-bible.md。额外标注声音样本来源路径，不一致项回注角色档案

## Completion Criterion

- ✅ Checkable：返回 `{character, mode: "A"|"B"|"C"|"D", voice_features: {声音类型, 句长, 锚点词[3-5], 对话节奏, OOC红线}, voice_bible_path, experiment_recorded}` —— voice_bible_path 指向已落盘的 voice-bible.md 中该角色子节
- ✅ Exhaustive：5 维分析全部完成且每维带文本证据；voice-bible.md 角色子节已更新；实验记录表已追加
- 🚫 Stop：返回结构化结果到调用方，不继续执行后续流程

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `sensory-writer` Skill | generate Step 1 写实验文本 | 🚫 硬阻断——实验文本不可跳过 |
| `_reference/voice-experiments.md` | 每次执行 | ⚠️ 使用内嵌四类选题骨架 |
| `framework/templates/voice-bible.md` | 创建新角色子节时 | ⚠️ 使用 voice-bible 通用结构知识降级 |
| `{DraftDir}/characters/{角色名}.md` | Step 3 对照 | ⚠️ 跳过档案对照，标注"无档案可对照" |
| `{DraftDir}/author-voice.md` | generate Step 2 自分析 | ⚠️ 仅基于通用叙事声音常识判断 |
