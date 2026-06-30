---
profile_id: "fengyue-style-v2"
version: "v2.0 (5 维正交化——移除所有主题相关项)"
status: 风格层（与基底/主题正交）
design_date: "2026-06-30"
supersedes: "fengyue-style-v1.md"
author: "风月"
analyzed_works:
  - "天启预报 (1646章)"
orthogonal_with:
  - "framework/templates/_style-bases/* (2 基底)"
  - "framework/templates/_themes/* (8 主题族)"
design_principle: "本风格层只装风月特定的'叙述态度+域词+桥段选择'——不装主题/题材/基底"
---

# 风月风格层 v2.0（5 维正交化）

> **核心设计原则**：v2.0 移除所有主题/题材相关项——已移到 `_themes/` 主题层（具体为 `doomsday/revelation/ritual/ensemble` 主题族）。
>
> **v2.0 只装**：风月特定的**叙述态度**（叙述者抒情 70-80%+碎嘴市井少）+ **域词**（末日意象网络 + 古风比喻连接词）+ **桥段选择**（启示式高潮+元叙事收束+棋局-传承意象闭环）
>
> **5 维正交**：基底 × 主题 × 风格 × 子变体 × 题材特化

---

## 零、风格层定位

**风月特定风格**（与中国网文共性基底的差异）：
- 风月特定的"叙述态度"= 叙述者抒情 70-80%（**不碎嘴+不市井幽默**——vs 远瞳冷幽默）
- 风月特定的"域词"= 末日意象网络（光暗/灰烬/棋局/深渊）+ 古风比喻连接词（宛如/仿佛/如同/宛若/恰如/恍若）
- 风月特定的"桥段选择"= 启示式高潮+元叙事收束+棋局-传承意象闭环

**v1.0 vs v2.0**：v1.0 含"末日意象网络/叙述者抒情 70-80%/启示见证型/棋局-传承意象闭环/多势力文明级博弈"——v2.0 已移除主题相关项。

---

## 一、风月特定叙述态度（3 项）

### 态度 1：叙述者抒情 70-80%（风月签名）

| 维度 | 风月默认 | 备注 |
|------|---------|------|
| 内心通道 | 叙述者抒情（第三人称）70-80% | 风月签名 |
| 形式 | "她就这样站在深渊的边缘……" | 抒情独白 |
| 与基底层关系 | 沿用中国网文基底"信息差机制" | 风月特定为"叙述者抒情"实现 |

### 态度 2：温暖+抒情（vs 远瞳冷幽默+不落风系统冷嘲）

| 维度 | 风月默认 | 备注 |
|------|---------|------|
| 温度 | 暖（vs 远瞳冷/不落风温）| 风月特定 |
| 形式 | 末日抒情+金句+感悟 | 风月签名 |
| 与基底层关系 | 沿用中国网文基底 | 风月特定为"暖"实现 |

### 态度 3：克制的吐槽（远瞳碎嘴 vs 风月克制）

| 维度 | 风月默认 | 备注 |
|------|---------|------|
| 吐槽密度 | 极低（vs 远瞳高）| 风月特定 |
| 形式 | 偶尔金句而非碎嘴 | 风月签名 |
| 与基底层关系 | 沿用中国网文基底 | 风月特定为"克制"实现 |

---

## 二、风月特定域词（白名单）

### 末日意象家族

| 类别 | 词 | 备注 |
|------|---|------|
| 光 | "黎明" / "光焰" / "光辉" / "光源" | 末日抒情第一语义场 |
| 暗 | "黑暗" / "暗影" / "暗灭" / "昏暗" | 末日抒情第二语义场 |
| 灰 | "灰烬" / "灰色" / "灰尘" | 末日意象 |
| 棋 | "棋局" / "棋子" / "黑白" / "人丁凋零" | 风月传承意象 |
| 渊 | "深渊" / "凋零" / "残骸" / "湮灭" / "终焉" | 末日核心 |
| 仪式 | "殉道" / "遗志" / "传承" / "托付" / "守望" / "诀别" / "永别" | 仪式相关 |

### 古风比喻连接词（高密度 9.86/万字）

| 词 | 频率 | 备注 |
|---|------|------|
| 宛如 | 高 | 风月签名 |
| 仿佛 | 高 | 风月签名 |
| 如同 | 高 | 风月签名 |
| 宛若 | 中 | 风月签名 |
| 恰如 | 中 | 风月签名 |
| 恍若 | 中 | 风月签名 |

### 风月签名词（白名单）

| 类别 | 词 | 备注 |
|------|---|------|
| 末日意象 | "宛如" / "仿佛" / "如同" / "宛若" / "恰如" / "恍若" | 古风比喻连接词 |
| 末日核心 | "光" / "暗" / "灰" / "烬" / "深渊" / "寂静" / "凋零" / "残骸" / "崩裂" / "湮灭" / "终焉" / "黎明" / "黄昏" / "夕阳" / "废墟" / "灰烬" / "棋局" / "传承" | 末日意象家族 |

---

## 三、风月特定桥段选择（3 个）

### 桥段 1：启示式高潮（风月签名）

| 维度 | 风月默认 | 备注 |
|------|---------|------|
| 形式 | 启示/认知翻转/信息揭示 | 5 阶段 |
| 实例 | 槐诗意识到"我是救世主还是罪魁祸首" | 风月签名 |
| 收束 | 末日意象回响+认知收束 | 风月特定 |
| 与主题关系 | 关联 `revelation/doomsday` 主题——已移到主题层 |

### 桥段 2：元叙事收束（风月罕见的中国网文结局技法）

| 维度 | 风月默认 | 备注 |
|------|---------|------|
| 形式 | 记录者采访+时间跳跃+7 个时间线分支 | 中国网文罕见 |
| 章节 | 尾声《新世》| 471 年后 |
| 角色 | 原诚采访圣者 | 双重身份标签 |
| 与主题关系 | 关联 `post-civilization` 主题——已移到主题层 |

### 桥段 3：棋局-传承意象闭环（风月签名）

| 维度 | 风月默认 | 备注 |
|------|---------|------|
| 开篇画面 | 序章棋局+铁板烧+最后的晚餐 | 风月签名 |
| 终章画面 | 终章大君之争 | 棋局呼应收束 |
| 元叙事收束 | 尾声"新世历 471 年记录者采访" | 风月罕见的中国网文结局技法 |
| 形式 | "一晃眼，这么多年就过去了吗？" | 意象回响 |
| 与主题关系 | 关联 `ritual/apocalypse` 主题——已移到主题层 |

### 桥段 4：宏微反差 + 末日意象回响（风月+远瞳共有）

| 维度 | 风月默认 | 备注 |
|------|---------|------|
| 宏微反差 | 史诗收尾 → 立刻日常收束 | 风月+远瞳共有 |
| 末日意象回响 | 结尾画面与开头画面=同样画面不同理解 | 风月特定 |
| 形式 | "槐诗"在大君之争中回响"棋局已散" | 意象闭环 |
| 与基底层关系 | 沿用中国网文基底 | 风月特定实现 |

---

## 四、子变体（1 个）

### 子变体 1：doomsday-imagery-narrator-lyrical（末日意象-叙述者抒情子变体）

```yaml
sub_variant: "doomsday-imagery-narrator-lyrical"
activation: "与主题 doomsday + revelation + ensemble + multi-faction 叠加时启用"
character_set: "槐诗+乌鸦+老杨+莫里斯+叶苏+林中小屋+原诚+姬宫华恋（部分重合）"
overrides:
  inner_channel: "narrator-lyrical-70-80"  # 叙述者抒情 70-80%
  climax_resolution: "revelation"  # 启示式
  chess_inheritance_loop: "required"  # 棋局-传承意象闭环
  meta_narrative_closure: "required"  # 元叙事收束
  long_sentence_bias: "high"  # 长句密集
  metaphor_density: "very-high"  # 9.86/万字
```

---

## 五、工程可加载参数（风格层默认配置）

### sensory-writer style_profile（风月风格层默认）

```yaml
style_profile:
  profile_id: "fengyue-style-v2"
  type: "chinese-webnovel-author-specific"
  # 风月特定叙述态度
  inner_channel: "narrator-lyrical"  # 叙述者抒情
  narrator_lyrical_pct: 70-80
  voice_type: "lyrical-warm"  # 抒情+暖（vs 远瞳冷/不落风温）
  roast_density: "low"  # 极低吐槽（vs 远瞳碎嘴）
  # 风月特定桥段
  climax_resolution: "revelation"  # 启示式
  meta_narrative_closure: "required"  # 元叙事收束
  chess_inheritance_loop: "required"  # 棋局-传承意象闭环
  long_sentence_bias: "high"
  metaphor_density: "very-high"  # 9.86/万字
  # 风月签名词（白名单）
  no_ban_words:  # 风月签名词（不视为违禁）
    - "宛如"
    - "仿佛"
    - "如同"
    - "宛若"
    - "恰如"
    - "恍若"
  doomsday_imagery: ["光", "暗", "灰", "烬", "深渊", "寂静", "凋零", "残骸", "崩裂", "湮灭", "终焉", "黎明", "黄昏", "夕阳", "废墟", "灰烬", "棋局", "传承"]
  translation_register: null  # 0 翻译腔
  # 不装任何主题/题材相关项
```

### handoff 字段（风格层默认）

```yaml
style_profile_type: "chinese-webnovel-base-v1.2"
style_profile_themes: []  # 主题层（必填，如 ["doomsday", "revelation", "ensemble", "multi-faction"]）
style_profile_variant: "fengyue-style-v2"
style_profile_subvariant: ""  # 子变体（按需：doomsday-imagery-narrator-lyrical）
```

---

## 六、与 6 作家风格层的正交关系

| 风格层 | 与 fengyue-style 的关系 | 组合建议 |
|------|------------|---------|
| kuiguannan-style | 根本对照 | **不建议叠加** |
| amamorin-style | 根本对照 | **不建议叠加** |
| shiniki-style | 根本对照 | **不建议叠加** |
| yuantong-style | 部分同源（中国网文+末日意象）| **可叠加**（风月+远瞳 = 中国网文+末日+科幻）|
| buluofeng-style | 部分同源（中国网文）| **可叠加**（风月+不落风 = 中国网文+末日+系统）|

---

## 七、5 维正交组合示例

### 示例 1：中国网文基底 + 主题 doomsday + 主题 revelation + 主题 ensemble + 主题 multi-faction + 风格 fengyue + 子变体 doomsday-imagery-narrator-lyrical

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["doomsday", "revelation", "ensemble", "multi-faction"]  # 4 主题叠加
风格变体: ["fengyue-style-v2"]
子变体: ["doomsday-imagery-narrator-lyrical"]
```

**实际效果**：
- 基底：7 坐标轴（多POV/事件驱动/长句+中段/...）
- 主题叠加：末日+启示+群像+多势力
- 风月风格：叙述者抒情 70-80%+末日意象网络+启示式高潮+棋局-传承闭环
- 子变体：末日意象+长句密集+元叙事收束

### 示例 2：中国网文基底 + 主题 doomsday + 主题 ensemble + 主题 cosmic-horror + 风格 fengyue + 风格 yuantong（双风格叠加）

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["doomsday", "ensemble", "cosmic-horror"]
风格变体: ["fengyue-style-v2", "yuantong-style-v2"]  # 双风格叠加
```

**效果**：中国网文 7 坐标轴 + 末日+群像+克苏鲁主题 + 风月+远瞳双风格（实验性"科幻+末日"）。

### 示例 3：中国网文基底 + 主题 doomsday + 主题 system + 风格 fengyue + 风格 buluofeng（双风格叠加）

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["doomsday", "system"]
风格变体: ["fengyue-style-v2", "buluofeng-style-v2"]  # 双风格叠加
```

**效果**：中国网文 7 坐标轴 + 末日+系统主题 + 风月+不落风双风格（实验性"末日+系统"）。

---

## 八、变更记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-30 | 初版（含主题相关项）|
| v2.0 | 2026-06-30 | **5 维正交化**——移除所有主题/题材相关项；只装风月特定叙述态度+域词+桥段选择 |

---

> **本风格层的工程定位**：
> - 路径：`framework/templates/_styles/fengyue-style.md`
> - 工程价值：可与中国网文基底 + `_themes/` 主题层独立正交叠加
