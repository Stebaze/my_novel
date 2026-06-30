---
title: sensory-writer 内部协议升级 PRD（独立于 5 维 refactor）
date: 2026-06-30
status: 草稿（设计阶段）
version: v1.0
author: 5 维 refactor 流程 Issue 4 派生
source: docs/refactor/5-dim-style-profile-prd.md（5 维决策记录）
related:
  - "profiles/authors/葵关南-默认.md (v2.1)"
  - "profiles/authors/雨森焚火-败犬女主.md (v2.0)"
  - "profiles/authors/杉井光-神的记事本.md (v2.0)"
  - "profiles/authors/远瞳-默认.md (v2.0)"
  - "profiles/authors/风月-天启预报.md (v2.0)"
  - "profiles/authors/不落风-魔女小姐.md (v2.0)"
  - "framework/guides/opus-writing-dna.md"
  - ".claude/skills/sensory-writer/SKILL.md (v2.0.0 已含 5 维 dict 输入)"
---

# sensory-writer 内部协议升级 PRD（独立于 5 维 refactor）

## Problem Statement

`.claude/skills/sensory-writer/SKILL.md` v2.0.0 已完成 5 维 dict 输入接入（Step 2 内心通道按基底分支 / Step 3 per-scene 加主题领域装置 / Step 4 5 维风格档案：禁词按风格白名单），并已通过第 1 章端到端验证（日轻基底 + daily-life+romance + 葵关南 + 碧阳子变体，1816 字符）。

但按 5 维 refactor 决策（PRD Q4+Q5），**sensory-writer 是通用工具**——5 维消费决策在 plan-chapter，sensory-writer 只接收 dict 输入并在 Step 2/3/4 协议级使用，不内置 5 维特定逻辑。**当前 sensory-writer 的核心问题不在 5 维接入，而在 3 个内部协议本身的写作质量瓶颈**：

1. **Step 2 内心通道协议单一**——只把"自由间接引语"作为默认内心通道 + 4b 强调独白 opt-in。但 6 部 works 实证显示至少有 4 种主流模式：
   - 自由间接引语为主（葵关南 60-70% / 远瞳 / 杉井光 / 雨森焚火）
   - 第一人称吐槽（葵关南 15-20% / 雨森焚火温水 / 杉井光鸣海）
   - 叙述者抒情（风月 70-80% / 远瞳深海大场景）
   - 括号补充（远瞳/葵关南 5-8%）
   - 系统/视角化内心（不落风系统提示 / 远瞳 NPC 滤镜）
   **当前协议只覆盖了模式 1+2，模式 3/4/5 无显式协议**——风月/不落风风格的章节下笔时无明确内心通道范式可循，AI 指纹易反弹。

2. **Step 3 per-scene 桥段协议缺失**——per-scene 模式只覆盖了"场景内 6 步协议"（场景锚定→拆节拍→逐节拍写作→末节拍护栏→产出 prose），但**没有显式处理"场景与场景之间的桥段"**。6 部 works 实证：
   - 葵关南「物理小物潜台词」（卡牌/印章/巧克力）—— 跨场景桥段载体
   - 远瞳「视角感染（NPC 滤镜）」—— 跨 POV 桥段机制
   - 风月「末日仪式-启示见证」—— 跨卷级桥段范式
   - 不落风「系统结算面板」—— 跨章节桥段载体
   - 雨森焚火「命运式不可达 + 物理小物转交」—— 关系桥段
   **当前协议只做了单场景内的"承接到 ending_state"**——跨场景桥段（如物理小物转交、视角感染、末日仪式）的协议级映射缺失。

3. **Step 4 自查协议通用**——当前 7 项自查（POV/逻辑/尾部/禁词/指纹/自由间接引语/语法）是**跨作通用底线**。但 6 部 works 各自有"作品特定"自检项：
   - 葵关南：内心独白 vs 出口表达的反差是否到位（双层）
   - 远瞳：视角感染是否建立（NPC 滤镜机制）
   - 风月：末日意象网络是否在场景中复用（光/暗/灰/棋局/深渊）
   - 不落风：系统结算面板是否在场景末出现
   - 雨森焚火：命运式不可达是否被场景推进
   - 杉井光：侦探叙事框架（委托人/死者代言人）是否到位
   **当前 Step 4 不支持作者按作品激活"作品特定自检项"——所有作品共用通用 7 项，作品特定风格特征无版本化检查。**

## Solution

**sensory-writer 内部协议升级 = 3 块独立协议扩展**，不破坏现有 5 维 dict 输入与开放风格兼容（v2.0.0 已 commit 的不变量）。

### 升级 A：Step 2 内心通道协议多模式化

**当前**：第 4 步只有"自由间接引语"为默认 + 4b 强调独白 opt-in；2026-06-29 重构加入 v2.0.0 5 维基底分支（日轻自由间接引语 / 中国网文信息差机制多模式并存）。

**升级后**：

```
Step 2 内心通道协议——按 style_profile.type 加载多模式：
1. [基线] 自由间接引语（默认）—— 跨作通用底线
2. [模式 1] 自由间接引语为主（葵关南 / 远瞳 / 杉井光 / 雨森焚火）
   → 第 4 步走自由间接引语；4b opt-in 强调独白
3. [模式 2] 第一人称吐槽（葵关南 15-20% / 雨森焚火温水 / 杉井光鸣海）
   → 4b 强调独白升级为"独立成段的角色腔调脱口而出"——不需【】标签，
   自由间接引语作为主内心通道，第一人称吐槽作为间断穿插（密度按 variant）
4. [模式 3] 叙述者抒情（风月 70-80% / 远瞳深海大场景）
   → 心理融在叙述者抒情中（"这真是个悲伤的故事"类），腔调温度"hot/scalding"
   → 自由间接引语降级为备选；4b opt-in 强调独白禁用（破坏抒情腔调连续性）
5. [模式 4] 括号补充（远瞳/葵关南 5-8%）
   → 自由间接引语 + 括号注叠加——括号作为"内心停顿/旁注"，
   不可承载关键情节信息（只能补充非关键认知）
6. [模式 5] 系统/视角化内心（不落风系统提示 / 远瞳 NPC 滤镜）
   → 内心通道为"系统面板"或"他人视角下 POV 角色的内心"——腔调温度"cold"
   → 自由间接引语降级为备选；4b opt-in 强调独白禁用
```

**与 5 维 dict 关系**：
- mode 1 / 2 / 4 由 `variant` 字段决定（葵关南 / 远瞳 / 杉井光 / 雨森焚火各自的 variant 风格层声明主导模式）
- mode 3 由 `variant` 决定（风月默认 / 远瞳深海 variant）
- mode 5 由 `themes` 含 `system` 或 `multi-pov` 决定（不落风 system 主题 / 远瞳 multi-pov 主题）
- **mode 之间的密度比例由 `variant` 风格层文件中的 inner_channel_default 字段决定**——与 5 维 style_profile 5 维正交

**修改范围**：
- `.claude/skills/sensory-writer/SKILL.md` Step 2 第 4 步 + 4b 子步骤

### 升级 B：Step 3 per-scene 桥段协议化

**当前**：per-scene 模式只处理"单场景内 6 步协议"，末节拍护栏只做"ending_state 与下场景 first action 衔接"。

**升级后**：

```
Step 3 per-scene 桥段协议——按 style_profile.variant 加载桥段库：
0. [场景锚定]（不变）
   → 额外读 style_profile.variant 风格层文件的 bridge_library 字段
   → 提取本作品候选桥段清单（如葵关南 → [物理小物潜台词, 番长自嘲签名, 翻译腔吐槽]）

1. [拆节拍]（不变）

2. [逐节拍写作]（不变）
   → 每节拍末下笔前自问：本节拍是否触发了 1-2 个桥段？
   → 桥段触发方式：
     · 物理小物：把场景中物件作为下场景的"再现/转交/消失"载体
     · 视角感染：本场景用 NPC 视角旁白过滤，下场景切回主 POV 形成对比
     · 末日仪式：把本场景的人物动作作为下场景仪式的"预演/伏笔"
     · 系统结算：本场景末加系统面板片段（评价/奖励/规则）
     · 命运式不可达：本场景刻意"擦肩而过"或"未说出口"，下场景呼应
   → 桥段密度按 variant 决定（葵关南物理小物 80-130/万字 / 远瞳视角感染按章节分布）

3. [末节拍护栏]（升级）
   → 末节拍必须是下场景桥段的"承接点"——下场景可无缝承接
   → 末节拍无桥段 → ⚠️ 警告（无桥段可承接，下场景可能漂移）

4. [产出 prose]（不变）
   → prose 末尾追加 bridge_anchor 字段（per-scene summary 中体现）
```

**与 5 维 dict 关系**：
- bridge_library 字段在 `framework/templates/_styles/{variant}.md` 风格层文件中声明（如 kuiguannan-style 的"物理小物潜台词 + 自嘲签名 + 翻译腔吐槽"）
- **bridge_library 是 variant 级别**——不进入 5 维，是 variant 风格层文件的扩展字段
- **5 维 dict 签名不变**——只多一个隐式 field（variant 风格层文件的 bridge_library）

**修改范围**：
- `.claude/skills/sensory-writer/SKILL.md` Step 3 第 0 步（场景锚定补读 variant 风格层 bridge_library）+ 第 3 步（末节拍护栏升级）

### 升级 C：Step 4 作品特定自检协议

**当前**：Step 4 是 7 项轻量自查（POV/逻辑/尾部/禁词/指纹/自由间接引语/语法）——跨作通用底线。

**升级后**：

```
Step 4 自查协议——分层：
[层 1] 跨作通用自检（保持 7 项不变——不破坏 v2.0.0 已 commit 的不变量）
1. [POV] 泄露检查
2. [逻辑] 内部一致性
3. [尾部] 不擅自收束
4. [禁词] style-guide.md「禁用词汇清单」扫描
5. [指纹] 强约束摘要最小集白名单扫描
6. [自由间接引语] 心理通道检查
7. [语法] §0 总纲 G1-G6 自查

[层 2] 作品特定自检（按 style_profile.variant 激活）
→ 读 variant 风格层文件的 self_check_protocols 字段
→ 激活本作品的特定自检项：
  · 葵关南：内心独白 vs 出口表达的双层反差是否到位
  · 远瞳：视角感染是否建立（NPC 滤镜机制）
  · 风月：末日意象网络是否在场景中复用（光/暗/灰/棋局/深渊 至少 2 个）
  · 不落风：系统结算面板是否在场景末出现（system 主题下必出）
  · 雨森焚火：命运式不可达是否被场景推进
  · 杉井光：侦探叙事框架（委托人/死者代言人）是否到位
→ 命中 → ⚠️ 警告（不阻断——仅提示）+ 修复建议（来自 variant 风格层文件）
→ 未激活作品特定自检 → 静默跳过
```

**与 5 维 dict 关系**：
- self_check_protocols 字段在 `framework/templates/_styles/{variant}.md` 风格层文件中声明
- **是 variant 级别扩展**——不进入 5 维
- **5 维 dict 签名不变**——只多一个隐式 field（variant 风格层文件的 self_check_protocols）

**修改范围**：
- `.claude/skills/sensory-writer/SKILL.md` Step 4 自查分层（层 1 通用 + 层 2 作品特定）

### 三块升级的协同关系

| 升级块 | 触发点 | 5 维 dict 字段 | 依赖 | 修改复杂度 |
|--------|--------|---------------|------|-----------|
| A（Step 2 多模式内心通道） | 第 4 步 | type（基底）+ variant | variant 风格层 inner_channel_default | 🟡 中（4 步 + 4b 协议扩展）|
| B（Step 3 桥段协议） | 第 0/3 步 | variant | variant 风格层 bridge_library | 🟡 中（场景锚定补读 + 末节拍护栏升级）|
| C（Step 4 作品特定自检） | 自查层 2 | variant | variant 风格层 self_check_protocols | 🟢 低（仅加 1 层）|

**共同依赖**：6 部 variant 风格层文件（`framework/templates/_styles/*.md`）需补充以下 3 个扩展字段：
- `inner_channel_default`（已有——v2.0.0 部分建立）
- `bridge_library`（需新增）
- `self_check_protocols`（需新增）

## Decision Document

### 设计决策

| # | 决策 | 范围 | 实施 |
|---|------|------|------|
| D1 | sensory-writer 内部协议升级 = 3 块独立扩展（A 内心通道 / B 桥段 / C 自检）| sensory-writer | 本 PRD |
| D2 | 与 5 维解耦：升级 A/B/C 都从 variant 风格层文件读取扩展字段，不进 5 维 | 5 维 | 本 PRD 验证 |
| D3 | 升级 A 内心通道模式 = 5 种（自由间接引语基线 + 4 变体），密度由 variant inner_channel_default 决定 | sensory-writer Step 2 | 本 PRD |
| D4 | 升级 B 桥段 = variant 风格层 bridge_library 字段，按 variant 加载候选桥段清单 | sensory-writer Step 3 | 本 PRD |
| D5 | 升级 C 作品特定自检 = variant 风格层 self_check_protocols 字段，命中仅警告不阻断 | sensory-writer Step 4 | 本 PRD |
| D6 | 6 部 variant 风格层文件需补 3 个扩展字段（inner_channel_default / bridge_library / self_check_protocols）| 6 部 variant 风格层文件 | 本 PRD |
| D7 | sensory-writer 5 维 dict 签名不变（v2.0.0 已 commit）——升级只增加隐式 field | 5 维 | 本 PRD 验证 |

### Architectural Principles

1. **5 维 = 消费层最小集**（Q3 决策，重申）：
   - 5 维 = 基底 + 主题叠加 + 风格 + 子变体 + 题材特化
   - 增加维度会破坏正交性
   - 本 PRD 的升级 A/B/C **不进入 5 维**——作为 variant 风格层文件的扩展字段
   - 桥段库 / 内心通道模式 / 作品特定自检 = 6 部 works 的具体特征，**不应作为 5 维维度**

2. **工具与决策分离原则**（Q4 决策，重申）：
   - sensory-writer = 通用工具（不内置 5 维特定逻辑 / 不内置作品特定逻辑）
   - 升级 A/B/C 是**协议级**——按 variant 风格层文件加载，不内置
   - 6 部 works 各自的桥段库 / 内心通道模式 / 作品特定自检 = variant 风格层文件中的数据

3. **协议 vs 数据分离**：
   - 协议 = sensory-writer Step 2/3/4 的执行流程（升级 A/B/C 扩展）
   - 数据 = 6 部 variant 风格层文件的扩展字段（inner_channel_default / bridge_library / self_check_protocols）
   - 数据更新不影响协议——协议更新不影响数据

### 字段定义

**variant 风格层文件扩展字段**（6 部 `_styles/{variant}.md` 需补充）：

```yaml
# 升级 A 依赖——v2.0.0 部分建立
inner_channel_default: "free-indirect-speech" | "first-person-rant" | "narrator-lyrical" | "bracket-supplement" | "system-perspective"
inner_channel_density: {模式名: 占比%}  # 多模式并存时声明密度

# 升级 B 依赖——需新增
bridge_library:
  - name: "物理小物潜台词"  # 桥段名（用于自检报告）
    type: "object-recurrence"  # 桥段类型
    density: "80-130/万字"  # 触发密度
    trigger: "卡牌/印章/巧克力等可转交物件在跨场景出现"  # 触发条件
    sample: "卡牌从番长手转到静希手——下场景静希独自看卡牌"  # 文本示例
  - name: "视角感染"  # 远瞳
    type: "pov-infiltration"
    density: "按章节分布"
    trigger: "NPC 视角旁白过滤 POV 角色的内心"
    sample: "..."
  - name: "末日仪式-启示见证"  # 风月
    type: "ritual-witness"
    density: "卷级"
    trigger: "..."
    sample: "..."

# 升级 C 依赖——需新增
self_check_protocols:
  - name: "内心独白 vs 出口表达的双层反差"  # 葵关南
    check: "本场景中是否有 1+ 个'内心 X / 出口 Y'的反差点"
    warning: "双层反差缺失——葵关南签名弱化"
  - name: "视角感染建立"  # 远瞳
    check: "本场景是否用 NPC 视角旁白"
    warning: "无 NPC 视角旁白——远瞳签名弱化"
  - name: "末日意象网络复用"  # 风月
    check: "场景中末日意象（光/暗/灰/棋局/深渊）是否出现 ≥2 个"
    warning: "末日意象密度不足——风月签名弱化"
  - name: "系统结算面板出现"  # 不落风
    check: "场景末是否有系统结算面板片段"
    warning: "无系统结算面板——不落风签名弱化"
  - name: "命运式不可达推进"  # 雨森焚火
    check: "本场景是否有'擦肩而过'或'未说出口'"
    warning: "无命运式不可达推进——雨森焚火签名弱化"
  - name: "侦探叙事框架到位"  # 杉井光
    check: "场景是否有委托人/死者代言人元素"
    warning: "无侦探框架元素——杉井光签名弱化"
```

**6 部 variant 风格层文件补字段**（D6 决策）：

| 变体文件 | 需补 inner_channel_default | 需补 bridge_library | 需补 self_check_protocols |
|---------|--------------------------|-------------------|--------------------------|
| `kuiguannan-style.md` v2.0 | ✅（已有："free-indirect-speech"）| 🆕 物理小物潜台词 + 番长自嘲签名 | 🆕 内心独白 vs 出口表达双层反差 |
| `amamorin-style.md` v2.0 | ✅（已有："free-indirect-speech"）| 🆕 命运式不可达 + 物理小物转交 | 🆕 命运式不可达推进 |
| `shiniki-style.md` v2.0 | ✅（已有："first-person-rant" 推测）| 🆕 侦探叙事框架 + 委托-死者代言人 | 🆕 侦探叙事框架到位 |
| `yuantong-style.md` v2.0 | ✅（已有："free-indirect-speech" 推测）| 🆕 视角感染 + 信息差机制 + 标签→谜题 | 🆕 视角感染建立 |
| `fengyue-style.md` v2.0 | ✅（已有："narrator-lyrical" 推测）| 🆕 末日仪式-启示见证 + 元叙事收束 | 🆕 末日意象网络复用 |
| `buluofeng-style.md` v2.0 | ✅（已有："system-perspective" 推测）| 🆕 系统结算面板 + 模拟型反英雄 | 🆕 系统结算面板出现 |

### Schema 变化

| 文件 | 修改类型 | 字段 |
|------|---------|------|
| `.claude/skills/sensory-writer/SKILL.md` | 升级 A | Step 2 第 4 步 + 4b 协议（5 种内心通道模式 + 按 variant 加载）|
| `.claude/skills/sensory-writer/SKILL.md` | 升级 B | Step 3 第 0 步（场景锚定补读 variant bridge_library）+ 第 3 步（末节拍护栏升级）|
| `.claude/skills/sensory-writer/SKILL.md` | 升级 C | Step 4 自查分层（层 1 通用 + 层 2 作品特定）|
| `framework/templates/_styles/kuiguannan-style.md` | 补字段 | bridge_library + self_check_protocols |
| `framework/templates/_styles/amamorin-style.md` | 补字段 | bridge_library + self_check_protocols |
| `framework/templates/_styles/shiniki-style.md` | 补字段 | bridge_library + self_check_protocols |
| `framework/templates/_styles/yuantong-style.md` | 补字段 | bridge_library + self_check_protocols |
| `framework/templates/_styles/fengyue-style.md` | 补字段 | bridge_library + self_check_protocols |
| `framework/templates/_styles/buluofeng-style.md` | 补字段 | bridge_library + self_check_protocols |

**5 维 dict 签名不变**——sensory-writer 接收的 style_profile 仍为 `{type, themes[], variant, subvariant, specialization}` 五字段。

### 命名约定

- **bridge_library 字段值** = 桥段名（中文，便于人类阅读）
- **bridge_library.type 字段值** = 英文枚举（object-recurrence / pov-infiltration / ritual-witness / system-settlement / fate-inaccessible / detective-frame / self-deception / double-layer / temporal-resonance / 跨时空呼应 / 信息差叙述 等）
- **self_check_protocols 字段值** = 自检项名（中文）

## Testing Decisions

### 端到端验证（每个升级块后跑一次）

**什么算好验证**：
- 协议升级后 sensory-writer 真的能读 variant 风格层扩展字段
- 5 维 dict 输入签名不变（向后兼容）
- 5 维 dict 字段在升级后能正确路由到不同模式（A/B/C 内部协议分支）
- 6 部 works 风格案例下，写作质量比升级前更贴近原作品风格

**验证步骤**（每个升级块 commit 后）：

1. **升级 A 验证**：
   - 输入 5 维 handoff：chinese-webnovel-base + scifi-fantasy+ensemble + fengyue-style
   - 跑 sensory-writer per-scene 一次（generate-chapter Step 2 调用）
   - 验证：第 4 步内心通道走"叙述者抒情"模式（风月 hot/scalding）
   - 验证：4b opt-in 强调独白被禁用（破坏抒情腔调连续性）
   - 对照未升级前相同输入的输出

2. **升级 B 验证**：
   - 输入 5 维 handoff：japanese-light-novel-base + daily-life+romance + kuiguannan-style
   - 跑 sensory-writer per-scene 一次（2-3 场景连续）
   - 验证：场景 1 末的"卡牌"物件在场景 2 出现（物理小物潜台词桥段）
   - 验证：summary_200 含 bridge_anchor 字段
   - 对照未升级前相同输入的输出

3. **升级 C 验证**：
   - 输入 5 维 handoff：chinese-webnovel-base + doomsday + fengyue-style
   - 跑 sensory-writer per-scene 一次
   - 验证：场景中末日意象（光/暗/灰/棋局/深渊）出现 ≥2 个——命中自检通过
   - 对照：若场景中末日意象 <2 个——命中自检警告（"末日意象密度不足——风月签名弱化"）

**自动化测试**：**不做**——工程无 pytest/单元测试框架（与 5 维 refactor PRD 决策一致），端到端验证足够。

### 回归测试

每次升级后跑"原葵关南+碧阳子变体"端到端——确保 5 维 dict 签名不变 + 现有 1816 字符第 1 章产物可复现。

## Out of Scope

### 不在本 PRD 范围

1. **5 维正交风格档案 refactor**（已 commit 5 维框架）—— 独立 commit chain `af534ed` / `6743ced` / `dda8afe` / `e3c7fde` / `fe83d3f`
2. **chapter-review 5 维评审基线差异化**——保留为可选层（PRD Q6+Q7 决策）
3. **CLAUDE.md 规则 6 更新**（author-voice.md → 5 维风格档案）—— 独立 refactor
4. **climax-patterns / reference-material / voice-bible 模板更新**—— 独立 refactor
5. **mo-writer 简报生成升级**—— 5 维 dict 消费在 plan-chapter 阶段 4 已做，mo-writer 仅接收 dict
6. **outline-tingle Session 2 5 维主题软对应**——已 commit in 5 维 refactor
7. **6 部 works 风格档案的进一步扩展**（v2.1 → v2.2）——独立 refactor

### 后续 refactor 候选（不在本 commit）

- **Refactor G**：sensory-writer Step 2.5 opus-dna 5 层写作契约的 6 部适配（按 variant 调整感知层/结构层/语言层/元认知层/高级能力）
- **Refactor H**：6 部 works 的"叙述者距离"作为新维度（v6）——独立评估
- **Refactor I**：variant 风格层文件升级到 v3.0——补 inner_channel_default 完整声明 + bridge_library 完整声明 + self_check_protocols 完整声明
- **Refactor J**：sensory-writer 升级 A/B/C 后做端到端 6 部 works 风格 case 全验证（每部 1 章 = 6 章）

## Commits

按 ask-matt 主流程，本 PRD 完成后进入 `to-issues` 阶段——拆 3 issue：

### Commit 1：sensory-writer Step 2 内心通道协议多模式化

**范围**：升级 A——Step 2 第 4 步 + 4b 协议扩展（5 种内心通道模式 + 按 variant 加载）。

**修改文件**：
- `.claude/skills/sensory-writer/SKILL.md` Step 2 第 4 步 + 4b

**修改要点**：
- 第 4 步从单一"自由间接引语为默认"扩展为"5 种模式（自由间接引语基线 / 第一人称吐槽 / 叙述者抒情 / 括号补充 / 系统/视角化内心）"
- 模式选择由 style_profile.variant 风格层 inner_channel_default 字段决定
- 4b opt-in 强调独白协议按模式分支（mode 3/5 禁用 / mode 1/2/4 启用）

### Commit 2：sensory-writer Step 3 per-scene 桥段协议化

**范围**：升级 B——Step 3 第 0 步（场景锚定补读 variant bridge_library）+ 第 3 步（末节拍护栏升级）。

**修改文件**：
- `.claude/skills/sensory-writer/SKILL.md` Step 3
- `.claude/skills/sensory-writer/_reference/scene-summary-protocol.md`（追加 bridge_anchor 字段 schema）

**修改要点**：
- Step 3 第 0 步（场景锚定）补读 style_profile.variant 风格层 bridge_library 字段 → 提取本作品候选桥段清单
- Step 3 第 3 步（末节拍护栏）从"ending_state 与下场景 first action 衔接"升级为"末节拍必须是下场景桥段的承接点"
- summary_200 schema 追加 bridge_anchor 字段（per-scene JSON 摘要）

### Commit 3：6 部 variant 风格层文件补 bridge_library + self_check_protocols 字段

**范围**：6 部 `_styles/{variant}.md` 补 2 个扩展字段——bridge_library / self_check_protocols。

**修改文件**：
- `framework/templates/_styles/kuiguannan-style.md` 补字段
- `framework/templates/_styles/amamorin-style.md` 补字段
- `framework/templates/_styles/shiniki-style.md` 补字段
- `framework/templates/_styles/yuantong-style.md` 补字段
- `framework/templates/_styles/fengyue-style.md` 补字段
- `framework/templates/_styles/buluofeng-style.md` 补字段

**字段内容**：见本文档"字段定义"段

### Commit 4：sensory-writer Step 4 作品特定自检协议

**范围**：升级 C——Step 4 自查分层（层 1 通用 + 层 2 作品特定）。

**修改文件**：
- `.claude/skills/sensory-writer/SKILL.md` Step 4

**修改要点**：
- 保持 7 项通用自检（POV/逻辑/尾部/禁词/指纹/自由间接引语/语法）不破坏
- 追加层 2"作品特定自检"——按 style_profile.variant 风格层 self_check_protocols 字段激活
- 命中 → ⚠️ 警告（不阻断）+ 修复建议

### Commit 5：端到端验证（6 部 works 风格 case 各 1 章）

**范围**：跑 sensory-writer 升级后 6 部 works 风格 case 端到端（每部 1 章 = 6 章），验证 3 块升级协同效果。

**修改文件**：无（仅端到端跑）

**验证步骤**：
- case 1：葵关南 + 碧阳子变体（回归测试——1816 字符产物可复现）
- case 2：风月 + 天启预报（验证升级 A 模式 3 + 升级 B 末日仪式 + 升级 C 末日意象）
- case 3：不落风 + 魔女小姐（验证升级 A 模式 5 + 升级 B 系统结算 + 升级 C 系统面板）
- case 4：远瞳 + 深海余烬（验证升级 A 模式 4/5 + 升级 B 视角感染 + 升级 C 视角感染）
- case 5：雨森焚火 + 败犬女主（验证升级 A 模式 1+2 + 升级 B 命运式不可达 + 升级 C 命运推进）
- case 6：杉井光 + 神的记事本（验证升级 A 模式 1+2 + 升级 B 侦探框架 + 升级 C 侦探框架）

## 实施计划

按 ask-matt 路径：grill ✅ → to-prd ✅（本文件）→ to-issues → implement。

| 阶段 | 状态 |
|------|------|
| grill | ✅ 完成（5 维 refactor 流程中已隐式完成——Q4+Q5 决策）|
| **to-prd** | **✅ 完成（本文档）** |
| to-issues | ⏳ 下一步——拆 5 commit（sensory-writer Step 2/3/4 + 6 部 variant 风格层 + 端到端验证）|
| implement | ⏳ 逐 commit 实施 |

## Further Notes

### 与 5 维 refactor 的关系

- 5 维 refactor 决策（PRD Q4+Q5）：**sensory-writer 是通用工具**——5 维消费决策在 plan-chapter
- 本 PRD 进一步推论：**sensory-writer 是"协议级通用工具"**——3 块升级（A/B/C）不内置 6 部 works 特定逻辑，而是从 variant 风格层文件动态加载
- 5 维 dict 签名不变（v2.0.0 已 commit）——升级只增加隐式 field

### 6 部 works 风格档案现状

- `profiles/authors/葵关南-默认.md` v2.1（750 行）—— 含 inner_channel_density 表 + 桥段库
- `profiles/authors/雨森焚火-败犬女主.md` v2.0（750 行）—— 含内心通道与桥段
- `profiles/authors/杉井光-神的记事本.md` v2.0（650 行）—— 含侦探叙事框架
- `profiles/authors/远瞳-默认.md` v2.0（770 行）—— 含双层信息差 + 视角感染 + 标签→谜题
- `profiles/authors/风月-天启预报.md` v2.0（730 行）—— 含末日意象网络 + 末日仪式
- `profiles/authors/不落风-魔女小姐.md` v2.0（750 行）—— 含系统结算面板

**6 部 works 档案已含升级 A/B/C 所需信息**——本 PRD 的工作是把"6 部档案中已分析出的模式"工程化为 variant 风格层文件的扩展字段。

### 5 维 vs 6 部 works

- 5 维 = 消费层最小集 = 架构约束（基底 + 主题叠加 + 风格 + 子变体 + 题材特化）
- 6 部 works 风格档案 = variant 风格层文件的数据源 = 6 部具体作品的工程化
- **5 维 不变**（保持消费层最小集）
- **6 部 works 档案可扩展**（v2.0 → v3.0 时补 inner_channel_default / bridge_library / self_check_protocols 字段）

### Architectural Principles（重申）

1. **5 维正交性约束**——不破坏
2. **工具与决策分离**——sensory-writer 是通用工具，5 维消费决策在 plan-chapter
3. **协议 vs 数据分离**——sensory-writer 协议 = Step 2/3/4 流程；6 部数据 = variant 风格层文件扩展字段
4. **协议更新不影响数据**——sensory-writer 升级 A/B/C 不要求 6 部档案同步更新（但实施时建议同步）
