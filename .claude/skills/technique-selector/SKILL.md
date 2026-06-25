---
name: technique-selector
description: 技法智能匹配——根据章节上下文（场景类型/角色状态/情绪张力）推荐技法和声音类型；索引自动解析，零维护
---

# 技法智能匹配

> **范式**：edit-article 范式——单次推荐 ≤ 240 字（Top-N 条目紧凑结构化）。
> **核心原则**：文件是源，本 Skill 是索引——不复制技法内容；每次调用从 framework 模板实时解析；返回匹配条目的完整内容（~500 字）而非全文库（12KB+）。
> **progressive disclosure**：技法条目本身存储在 `framework/templates/technique-library.md` 和 `framework/guides/reference-material.md`；本 Skill 只存结构化索引 + 匹配算法。

## Identity

技法智能匹配器。两种 Operation：`match`（技法推荐）和 `get-voice-types`（声音类型推荐）。被 `qing-novelist`（维度 4/5）、`mo-writer`（写作前仪式）、`plan-chapter`（pre-flight-check 阶段 0）调用。

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | `qing-novelist`（D4/D4b/D5）, `mo-writer`（写作前仪式）, `plan-chapter`（pre-flight-check C0） |
| **Input** | `operation` (`match`/`get-voice-types`), `chapter_context`（match 用）, `{emotional_goal, genre, chapter_type}`（get-voice-types 用） |
| **Output** | match: Top-N 技法 + 完整条目内容 + 子库覆盖报告；get-voice-types: Top-3 声音类型 + 核心参数 |

## Triggers

- 调用方 Skill 通过 `Skill` tool 传入参数

---

## Operations

| Operation | Trigger | Responsibility |
|-----------|---------|---------------|
| **match** | `operation="match"` | 解析技法索引 → 提取查询标签 → 匹配计算 → 返回 Top-N 推荐 + 子库覆盖 |
| **get-voice-types** | `operation="get-voice-types"` | 解析声音类型索引 → 匹配 → 返回 Top-3 + 匹配理由 + 参数摘要 |

---

## Operation: match

### 输入

```
{
  chapter_type: "战斗" | "日常" | "情感" | "揭示" | "过渡" | "高潮" | "悬疑" | "多势力",
  emotional_goal: "燃" | "温馨" | "紧张" | "悲伤" | "幽默" | "史诗" | "讽刺" | "华丽",
  scene_types: ["对话", "动作", "独白", "群像", ...],
  genre: "奇幻" | "修仙" | "都市" | "校园" | "末世" | ...,
  word_count: 3000,
  pov: "第一人称" | "第三人称" | "多POV"
}
```

### 流程

```
1. 解析索引：读 technique-library.md → 按 H2 标题定位各子库 + 识别 ### 条目 → 提取 name/category/tags/source_location/source_type（🏠/📖）/reference_author
2. 提取查询标签：chapter_type → 场景类型 / emotional_goal → 情感基调 / scene_types → 功能 / genre → 类型（调整权重）
3. 匹配计算：tags ∩ 查询标签 交集 + 🏠 内置权重 +1 → 按匹配数 + 权重降序 → 同分优先"开头方式"
4. 分类覆盖：Top-5 来自同一子库 → 各补 1 条；优先覆盖 开头/桥段/断章/衔接（≥2 场景时）
5. 读取完整内容：从源文件读完整条目（模式/要点/适用场景/避免事项） + **实例** 字段
6. 返回 Top-N（默认 5，最多 7）
```

### 输出格式

```
## 技法推荐：本章 Top-5

### 推荐 1：[技法名]（🏠/📖 | 匹配标签：[标签列表]）
**模式**：[摘要]
**写作要点**：[要点]
**避免**：[避免项]
**实例**：[如有]

[... 共 5 条]

### 子库覆盖
- 开头方式：✅ 已覆盖（推荐 N）
- 场景桥段：✅ 已覆盖（推荐 N）
- 断章技法：✅ 已覆盖（推荐 N）
- 场景衔接：✅ 已覆盖（推荐 N）| ⚠️ 未覆盖（无场景切换需求）
- 事件展开：✅ 已覆盖（推荐 N, M）
- 人物关系：⚠️ 未覆盖（本章无关系型场景，跳过）

→ 接受全部 / 替换 / 追加 / 跳过
```

### 内置技法标签映射（硬编码）

> 🏠 条目不标注适用场景时使用此默认映射：

| 技法 | 默认标签 |
|------|---------|
| 动作入场式 | 开头, 快节奏, 战斗, 悬念回收 |
| 对话钩子式 | 开头, 日常, 幽默, 关系推进 |
| 氛围铺垫式 | 开头, 慢热, 悬疑, 世界观输出 |
| 事件中段切入式 | 开头, 快节奏, 战斗, 高潮 |
| 伏笔式开场 | 开头, 悬念构建, 揭示 |
| 直接切换 | 桥段, 快节奏, 多势力 |
| 情绪呼应 | 桥段, 情感, 关系推进 |
| 因果链 | 桥段, 信息释放, 多势力 |
| 平行剪辑 | 桥段, 高潮, 多势力 |
| 时间省略 | 桥段, 过渡 |
| 渐进揭示 | 展开, 悬疑, 信息释放, 世界观输出 |
| 反转 | 展开, 高潮, 悬念构建 |
| 滚雪球升级 | 展开, 战斗, 紧张 |
| 多线汇聚 | 展开, 高潮, 多势力 |
| 考试驱动叙事 | 展开, 战斗, 快节奏 |
| 答案前一刻 | 断章, 悬念构建 |
| 关系临界点 | 断章, 情感, 关系推进 |
| 能力升级宣告 | 断章, 战斗, 角色塑造 |
| 敌人出现 | 断章, 战斗, 悬念构建 |
| 情绪反转 | 断章, 反差, 情感 |
| 平静中的不祥 | 断章, 悬疑, 压抑 |

**衔接技法**（§七，ID 前缀 S/C/V = 场景间/章间/卷间）：

| ID 范围 | 名称 | 默认标签 |
|--------|------|---------|
| S1-S14 | 时间锚定 / 地点锚定 / 同时反打 / 门之通道 / 对比转场 / 主题呼应 / 荒诞破局 / 日常沉降 / 梦醒锚点 / 无声收尾 / 软性开场 / 外部闯入 / 宏微反差 / 媒介物转场 | 衔接, 场景间衔接 + 类型标签 |
| C1-C8 | 浸入式跨章 / 钩子回收式 / 锚点重启式 / 情感延续式 / 视角接力式 / 话说体 / 对话钩子开章 / 章末金句法 | 衔接, 章间衔接 + 类型标签 |
| V1-V6 | 闭合+新钩 / 地位重置+升级 / 时间跳跃 / 舞台转移 / 序章重启 / 预案→意外→再预案 | 衔接, 卷间衔接 + 类型标签 |

> 完整 28 个衔接技法的标签细节 + 详细匹配表见 framework/templates/technique-library.md §七（每次调用实时解析，无需维护）

---

## Operation: get-voice-types

### 流程

```
1. 解析索引：读 framework/guides/reference-material.md §五「附录 A：参考叙事声音谱系」 → 识别 ### A 开头的子标题 → 提取 id/name/summary/tags/source_location

2. 匹配：每种声音类型 → 声音.tags ∩ 查询标签 的交集大小

3. 返回 Top-3：ID + 名称 + 一句话概括 + 匹配理由 + 核心参数摘要

4. 同时返回"不使用参考声音"选项（始终可用）
```

### 声音类型索引（7 种，硬编码标签）

| ID | 名称 | 标签 |
|----|------|------|
| A1 | 宏微反差声 | 史诗, 幽默, 反差, 奇幻, 穿越 |
| A2 | 理性推演声 | 策略, 悬疑, 多势力, 理性, 修仙 |
| A3 | 冷静荒诞声 | 讽刺, 荒诞, 黑色幽默, 压抑 |
| A4 | 优雅狼狈声 | 华丽, 反差, 多重身份, 幽默 |
| A5 | 旁观者声 | 日常, 温馨, 幽默, 校园, 慢热 |
| A6 | 末日抒情声 | 史诗, 压抑, 悲剧, 末世, 信息释放 |
| A7 | 桌游宅吐槽声 | 日常, 幽默, 主题型, 角色塑造 |

### 输出格式

```
## 声音类型推荐：本章 Top-3

### 推荐 1：A1 宏微反差声（匹配：史诗, 反差）
**一句话**：[一句话概括]
**匹配理由**：[为什么适合本章]
**参数摘要**：[句长/词汇/幽默机制/情感距离]

[... 共 3 条]

### 推荐 N：不使用参考声音
完全使用本项目 author-voice.md 定义的声音，不借助参考声音类型。

→ 选择对标策略：[A1 / A4 / 混合 / 不使用]
```

---

## 降级策略

| 缺失 | 降级 |
|------|------|
| `framework/templates/technique-library.md` 缺失 | 仅使用内置技法（🏠）—— 标签映射已硬编码 → 标注"⚠️ 技法库文件缺失，仅推荐内置技法" |
| `framework/guides/reference-material.md` §五 缺失 | 跳过声音推荐 → 标注"⚠️ 叙事声音谱系文件缺失，仅使用项目 author-voice.md" |

## Output

- **match**: Top-N 技法推荐 + 子库覆盖报告
- **get-voice-types**: Top-3 声音类型 + 匹配理由 + 参数摘要 + "不使用"选项

## Completion Criterion

- ✅ Checkable：match 返回 `{techniques: [{name, category, source_type, tags, full_content}], coverage_report, top_n}` —— top_n 默认 5，最多 7；get-voice-types 返回 `{voice_types: [{id, name, summary, match_reason, params}], no_reference_option: true}`
- ✅ Exhaustive：解析索引 + 标签提取 + 匹配计算 + 完整内容读取 + 分类覆盖检查全部执行
- 🚫 Stop：返回结构化结果到调用方，不继续执行后续流程

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `framework/templates/technique-library.md` | match Step 1 索引解析 | ⚠️ 仅使用内置技法（🏠）—— 标签硬编码 |
| `framework/guides/reference-material.md` | get-voice-types Step 1 索引解析 | ⚠️ 跳过声音推荐 |
