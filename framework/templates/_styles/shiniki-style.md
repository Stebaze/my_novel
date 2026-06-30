---
profile_id: "shiniki-style-v2"
version: "v2.0 (5 维正交化——移除所有主题相关项)"
status: 风格层（与基底/主题正交）
design_date: "2026-06-30"
supersedes: "shiniki-style-v1.md"
author: "杉井光"
analyzed_works:
  - "神的记事本 (2007-2014) 9卷"
orthogonal_with:
  - "framework/templates/_style-bases/* (2 基底)"
  - "framework/templates/_themes/* (8 主题族)"
design_principle: "本风格层只装杉井光特定的'叙述态度+桥段选择'——不装主题/题材/基底"
---

# 杉井光风格层 v2.0（5 维正交化）

> **核心设计原则**：v2.0 移除所有主题/题材相关项——已移到 `_themes/` 主题层（具体为 `mystery/detective/supernatural/neet` 主题族）。
>
> **v2.0 只装**：杉井光特定的**叙述态度**（双轨制内心通道）+ **桥段选择**（委托-死者代言人推理+反转式高潮）
>
> **5 维正交**：基底 × 主题 × 风格 × 子变体 × 题材特化

---

## 零、风格层定位

**杉井光特定风格**（与日轻共性基底的差异）：
- 杉井光特定的"叙述态度"= 双轨制内心通道（自指"我"+爱丽丝演讲体）
- 杉井光特定的"桥段选择"= 委托-死者代言人推理+反转式高潮（"为什么发生"而非"谁干的"）
- 杉井光特定的"叙述节奏"= X 季的尾声文学化时间标记

**v1.0 vs v2.0**：v1.0 含"必死的日常/多边缘人共同战线/NEET 边缘人题材"——v2.0 已移除主题相关项。

---

## 一、杉井光特定叙述态度（3 项）

### 态度 1：双轨制内心通道（杉井光签名）

| 维度 | 杉井光默认 | 备注 |
|------|----------|------|
| 轨 1 | 自由间接引语（鸣海自指"我"）| 沿用日轻基底 |
| 轨 2 | **爱丽丝演讲体独白**（"侦探的本质是死者的代言人……"）| 杉井光特定 |
| 比例 | 60-80% 爱丽丝发言 | 绝对权威核心 |
| 与基底层关系 | 沿用日轻基底"自由间接引语" | 杉井光特定为"双轨制" |

### 态度 2：自传体背景建立（杉井光签名）

| 维度 | 杉井光默认 | 备注 |
|------|----------|------|
| 形式 | 每章开头"作者声线切入"（30-50 字）| "侦探是这样告诉我的""十六岁那年冬天" |
| 频率 | 每章 1 次 | 杉井光签名 |
| 与基底层关系 | 沿用日轻基底"自嘲式亲密" | 杉井光特定为"自传体" |

### 态度 3：自嘲+NEET 文化（vs 葵关南式自嘲）

| 维度 | 杉井光默认 | 备注 |
|------|----------|------|
| 吐槽方式 | 鸣海/宏哥/少校的三人转吐槽接龙 | 杉井光签名 |
| NEET 文化 | 尼特族/茧居族/家里蹲/Hikikomori 词汇密集 | 杉井光特定 |
| 与基底层关系 | 沿用日轻基底"吐槽" | 杉井光特定为"NEET 自嘲" |

---

## 二、杉井光特定桥段选择（3 个）

### 桥段 1：委托-死者代言人推理（杉井光签名）

| 维度 | 杉井光默认 | 备注 |
|------|----------|------|
| 4 阶段 | 委托登门→调查→多角色会议→爱丽丝独白 | 每次委托 = 1 卷 |
| 反转型 | 委托人 A → 爱丽丝挖出 B → B 不是"谁干的"而是"为什么发生" | 杉井光签名 |
| 否定式推理 | 排除法而非归纳法 | "不对，这不太对劲" |
| 与主题关系 | 关联 `mystery/detective` 主题——已移到主题层 |

### 桥段 2：反转式高潮（杉井光签名）

| 维度 | 杉井光默认 | 备注 |
|------|----------|------|
| 形式 | "死者想说的是 X" | 爱丽丝茧居床=祭坛 |
| 实例 | 彩夏跳楼真相="选择死亡地点" / 银二先生之死="为保护某人而被牺牲" | 杉井光签名 |
| 与主题关系 | 关联 `mystery/supernatural` 主题——已移到主题层 |

### 桥段 3：X 季的尾声文学化时间标记（杉井光签名）

| 维度 | 杉井光默认 | 备注 |
|------|----------|------|
| 形式 | "十一月的尾声" / "宛如漫长梦境的十六岁冬天" | 文学化时间 |
| 效果 | 把时间压缩为情绪刻度 | 杉井光特定 |
| 与基底层关系 | 风格特定——不属于基底 |

---

## 三、子变体（1 个）

### 子变体 1：neet-detective-death-cycle（NEET 侦探子变体）

```yaml
sub_variant: "neet-detective-death-cycle"
activation: "与主题 detective + supernatural + neet 叠加时启用"
character_set: "爱丽丝（NEET 侦探）+ 鸣海（助手）+ 第四代+少校+宏哥+阿哲学长+彩夏（锚点）"
overrides:
  inner_channel: "dual-track"  # 双轨制内心通道
  alice_speech_density: "60-80%"  # 爱丽丝发言密度
  death_pattern: "physical-per-volume"  # 每卷≥1 物理死亡
  climax_resolution: "reversal-truth"  # 反转型
```

---

## 四、工程可加载参数（风格层默认配置）

### sensory-writer style_profile（杉井光风格层默认）

```yaml
style_profile:
  profile_id: "shiniki-style-v2"
  type: "light-novel-author-specific"
  # 杉井光特定叙述态度
  inner_channel: "dual-track"  # 双轨制
  alice_speech_density: 60-80
  autobiographical_opening: "required"  # 自传体背景
  neet_culture: "required"  # NEET 文化域词必填
  # 杉井光特定桥段
  detective_framework: "always-on"  # 委托-死者代言人强制
  reversal_resolution: "always-on"  # 反转型高潮
  seasonal_euphemism: "required"  # X 季的尾声文学化时间
  # 杉井光签名词（白名单）
  no_ban_words:  # 杉井光签名词
    - "死者的代言人"
    - "NEET"
    - "茧居族"
    - "家里蹲"
    - "Hikikomori"
    - "Dr.Pepper"
  neet_culture_words: ["NEET", "茧居族", "家里蹲", "Hikikomori", "尼特族", "漫无目的地生活", "Dr.Pepper", "2ch", "IRC", "QQ表情", "BBA"]
  detective_words: ["福尔摩斯", "名侦探", "死者代言人", "委托人", "谜题", "排除法"]
  ramen_words: ["拉面", "汤头", "明老板", "花丸"]
  baseball_words: ["PowerPlayBall", "PWLB", "棒球", "球棒", "投手", "打击"]
  translation_register: "default-off"
  # 不装任何主题/题材相关项
```

### handoff 字段（风格层默认）

```yaml
style_profile_type: "japanese-light-novel-base-v1.2"
style_profile_themes: []  # 主题层（必填，如 ["detective", "supernatural", "neet"]）
style_profile_variant: "shiniki-style-v2"
style_profile_subvariant: ""  # 子变体（按需：neet-detective-death-cycle）
```

---

## 五、与 6 作家风格层的正交关系

| 风格层 | 与 shiniki-style 的关系 | 组合建议 |
|------|------------|---------|
| kuiguannan-style | 互补（推理 vs 校园）| 可叠加（实验性）|
| amamorin-style | 互补（推理 vs 败犬）| 可叠加（实验性）|
| yuantong-style | 根本对照 | **不建议叠加** |
| fengyue-style | 根本对照 | **不建议叠加** |
| buluofeng-style | 根本对照 | **不建议叠加** |

---

## 六、5 维正交组合示例

### 示例 1：日轻基底 + 主题 detective + 主题 supernatural + 主题 neet + 风格 shiniki + 子变体 neet-detective-death-cycle

```yaml
主风格档案: "japanese-light-novel-base-v1.2"
主题: ["detective", "supernatural", "neet"]  # 3 主题叠加
风格变体: ["shiniki-style-v2"]
子变体: ["neet-detective-death-cycle"]
```

**实际效果**：
- 基底：7 坐标轴（第一人称/关系驱动/短句+极短段/...）
- 主题叠加：侦探+超自然+NEET
- 杉井光风格：双轨制内心通道+委托-死者代言人+反转式高潮
- 子变体：爱丽丝+鸣海+NEET 团队+每卷≥1 物理死亡

### 示例 2：日轻基底 + 主题 mystery + 风格 shiniki（无 supernatural 主题）

```yaml
主风格档案: "japanese-light-novel-base-v1.2"
主题: ["mystery"]
风格变体: ["shiniki-style-v2"]
```

**效果**：日轻 7 坐标轴 + 推理主题（不含超自然） + 杉井光反转式高潮。

---

## 七、变更记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-30 | 初版（含主题相关项）|
| v2.0 | 2026-06-30 | **5 维正交化**——移除所有主题/题材相关项；只装杉井光特定叙述态度+桥段选择 |

---

> **本风格层的工程定位**：
> - 路径：`framework/templates/_styles/shiniki-style.md`
> - 工程价值：可与日轻基底 + `_themes/` 主题层独立正交叠加
