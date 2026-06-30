---
profile_id: "buluofeng-style-v2"
version: "v2.0 (5 维正交化——移除所有主题相关项)"
status: 风格层（与基底/主题正交）
design_date: "2026-06-30"
supersedes: "buluofeng-style-v1.md"
author: "不落风"
analyzed_works:
  - "魔女小姐的速通手册 (191章)"
orthogonal_with:
  - "framework/templates/_style-bases/* (2 基底)"
  - "framework/templates/_themes/* (8 主题族)"
design_principle: "本风格层只装不落风特定的'叙述态度+域词+桥段选择'——不装主题/题材/基底"
---

# 不落风风格层 v2.0（5 维正交化）

> **核心设计原则**：v2.0 移除所有主题/题材相关项——已移到 `_themes/` 主题层（具体为 `system/simulator/cross-time/urban-fantasy` 主题族）。
>
> **v2.0 只装**：不落风特定的**叙述态度**（系统作为第二叙事声音+反英雄吐槽+角色+系统双声）+ **域词**（系统冷嘲词+维多利亚工业词）+ **桥段选择**（系统结算型高潮+仪式中断+角色存档）
>
> **5 维正交**：基底 × 主题 × 风格 × 子变体 × 题材特化

---

## 零、风格层定位

**不落风特定风格**（与中国网文共性基底的差异）：
- 不落风特定的"叙述态度"= **系统作为第二叙事声音**（「」609 块）+ 反英雄吐槽+角色+系统双声
- 不落风特定的"域词"= 系统冷嘲词（评价/表情别这么严肃嘛/坏事没发生）+ 维多利亚工业词（蒸汽/煤烟/钟塔/酸雨）
- 不落风特定的"桥段选择"= 系统结算型高潮（评价+奖励+技能升级）+ 仪式中断+角色存档

**v1.0 vs v2.0**：v1.0 含"系统作为第二叙事声音/维多利亚工业革命语义场/单次模拟=推进单位/角色+系统双声吐槽/反英雄穿越"等主题相关项——v2.0 已移除主题相关项。

---

## 一、不落风特定叙述态度（3 项）

### 态度 1：系统作为第二叙事声音（不落风签名）

| 维度 | 不落风默认 | 备注 |
|------|----------|------|
| 「」密度 | 609 个「」块 = 5.7/万字 | 文本密度的"第二位主角" |
| 3 模式 | 机械报告体 60% / 毒舌评语 30% / 危机提示 10% | 系统多模式 |
| 范本 | 「评价：战斗！爽！」 | 系统结算 |
| 与基底层关系 | 沿用中国网文基底"信息差机制" | 不落风特定为"系统作为叙事声音"实现 |

### 态度 2：反英雄吐槽（不落风签名）

| 维度 | 不落风默认 | 备注 |
|------|----------|------|
| 主角定位 | 反英雄穿越者（无金手指预备知识）| 不落风签名 |
| 吐槽方式 | "我的价值观和我的价值观很不一样" | 反英雄 |
| 与基底层关系 | 沿用中国网文基底 | 不落风特定为"反英雄"实现 |

### 态度 3：角色+系统双声吐槽（vs 远瞳碎嘴+葵关南吐槽）

| 维度 | 不落风默认 | 备注 |
|------|----------|------|
| 模式 | 主角吐槽 + 系统冷嘲 + 角色互动 = 3 层 | 葵关南是 2 层 |
| 系统冷嘲 | 「表情别这么严肃嘛」「坏事这不还没发生吗？」| 系统吐槽 |
| 与基底层关系 | 沿用中国网文基底 | 不落风特定为"双声"实现 |

---

## 二、不落风特定域词（白名单）

### 系统冷嘲词

| 类别 | 词 | 备注 |
|------|---|------|
| 系统报告 | 「正在检测可带入物品」「命定点数：21」「评价：战斗!爽!」| 系统报告体 |
| 系统冷嘲 | 「表情别这么严肃嘛」「坏事这不还没发生吗？」「你的价值观和我的价值观很不一样」| 系统毒舌评语 |
| 系统危机 | 「但没泣想到你二是靠彡着^出卖本-系统才澪得到事的信任~...诌..⑺.衤只三能说四多注意灵吧梦」| 第四面墙警告 |
| 系统动作 | 「奖励」「存档」「评价」「模拟」| 系统动作词 |

### 维多利亚工业词

| 类别 | 词 | 备注 |
|------|---|------|
| 工业核心 | 蒸汽/煤烟/火炉/钟塔/酸雨 | 维多利亚工业革命 |
| 工业建筑 | 工厂/机车/齿轮/烟囱 | 工业城市景观 |
| 工业社会 | 钟塔巷区/贫民/烧伤姐姐 | 维多利亚阶级 |

### 不落风签名词（白名单）

| 类别 | 词 | 备注 |
|------|---|------|
| 系统签名 | "评价" / "奖励" / "命定点数" / "存档" / "技能" | 不落风系统签名 |
| 工业签名 | "蒸汽" / "煤烟" / "火炉" / "钟塔" / "酸雨" / "工厂" / "机车" / "齿轮" / "烟囱" | 维多利亚工业签名 |
| 反英雄签名 | "我的价值观和我的价值观很不一样" | 不落风反英雄吐槽 |

---

## 三、不落风特定桥段选择（4 个）

### 桥段 1：系统结算型高潮（不落风签名）

| 维度 | 不落风默认 | 备注 |
|------|----------|------|
| 形式 | 「评价：战斗！爽！」+ 奖励+技能升级 | 系统结算 |
| 实例 | Ch9 系统结算 | 不落风签名 |
| 收束 | 系统「评价」+ 奖励 + 命运点扣减 + 技能升级 | 不落风特定 |
| 与主题关系 | 关联 `system/simulator` 主题——已移到主题层 |

### 桥段 2：仪式中断（不落风签名）

| 维度 | 不落风默认 | 备注 |
|------|----------|------|
| 形式 | 仪式中断+入侵者 | Ch7 范本 |
| 收束 | 仪式未完成+系统介入 | 不落风特定 |
| 与主题关系 | 关联 `ritual/system` 主题——已移到主题层 |

### 桥段 3：角色存档诞生（不落风签名）

| 维度 | 不落风默认 | 备注 |
|------|----------|------|
| 形式 | 模拟收束 → 角色存档 | Ch17 范本 |
| 收束 | "力量突破"型高潮 | 不落风特定 |
| 与主题关系 | 关联 `system/level-up` 主题——已移到主题层 |

### 桥段 4：身份伪装戏（不落风签名）

| 维度 | 不落风默认 | 备注 |
|------|----------|------|
| 形式 | 戴面具+教会袍伪装 | Ch19-20 范本 |
| 收束 | 身份暴露/维持 | 不落风特定 |
| 与主题关系 | 关联 `urban-fantasy/system` 主题——已移到主题层 |

---

## 四、子变体（1 个）

### 子变体 1：victorian-system-anti-hero（维多利亚-系统-反英雄子变体）

```yaml
sub_variant: "victorian-system-anti-hero"
activation: "与主题 system + simulator + cross-time + anti-hero + urban-fantasy 叠加时启用"
character_set: "夏尔+莉奇+艾米+艾维娜+尤莉斯+梅尔牧师+钟塔巷区贫民"
overrides:
  system_narrative_voice: "always-on"  # 系统作为第二叙事声音
  system_dialogue_density: 5.7  # 「」每万字
  simulation_unit: "24h-countdown"  # 单次模拟
  inner_channel: "narrator-third-with-system-voice"  # 叙述者第三人称+系统
  climax_resolution: "system-settlement"  # 系统结算
  long_sentence_bias: "very-high"  # 29.3 字
```

---

## 五、工程可加载参数（风格层默认配置）

### sensory-writer style_profile（不落风风格层默认）

```yaml
style_profile:
  profile_id: "buluofeng-style-v2"
  type: "chinese-webnovel-author-specific"
  # 不落风特定叙述态度
  system_narrative_voice: "always-on"  # 系统作为第二叙事声音
  system_dialogue_count: 609
  system_dialogue_density: 5.7  # 「」每万字
  system_modes:
    mechanical_report: 60
    sarcastic_commentary: 30
    crisis_warning: 10
  protagonist_type: "anti-hero"  # 反英雄
  inner_channel: "third-person-with-system-voice"  # 叙述者第三人称+系统
  voice_type: "system-rant-self-deprecation"  # 系统+反英雄吐槽
  # 不落风特定桥段
  climax_resolution: "system-settlement"  # 系统结算
  ritual_interruption: "required"  # 仪式中断
  character_archiving: "required"  # 角色存档
  identity_disguise: "required"  # 身份伪装
  long_sentence_bias: "very-high"
  # 不落风签名词（白名单）
  no_ban_words:  # 不落风签名词
    - "评价"
    - "奖励"
    - "命定点数"
    - "存档"
    - "技能"
  system_words: ["存档", "模拟", "技能", "装备", "点数", "评价", "奖励", "升级", "任务", "命定"]
  victorian_words: ["蒸汽", "煤烟", "火炉", "钟塔", "酸雨", "工厂", "机车", "齿轮", "烟囱"]
  translation_register: null  # 0 翻译腔
  # 不装任何主题/题材相关项
```

### handoff 字段（风格层默认）

```yaml
style_profile_type: "chinese-webnovel-base-v1.2"
style_profile_themes: []  # 主题层（必填，如 ["system", "simulator", "urban-fantasy", "cross-time", "anti-hero"]）
style_profile_variant: "buluofeng-style-v2"
style_profile_subvariant: ""  # 子变体（按需：victorian-system-anti-hero）
```

---

## 六、与 6 作家风格层的正交关系

| 风格层 | 与 buluofeng-style 的关系 | 组合建议 |
|------|------------|---------|
| kuiguannan-style | 根本对照 | **不建议叠加** |
| amamorin-style | 根本对照 | **不建议叠加** |
| shiniki-style | 根本对照 | **不建议叠加** |
| yuantong-style | 部分同源（中国网文+系统）| **可叠加**（不落风+远瞳 = 中国网文+系统+科幻）|
| fengyue-style | 部分同源（中国网文）| **可叠加**（不落风+风月 = 中国网文+系统+末日）|

---

## 七、5 维正交组合示例

### 示例 1：中国网文基底 + 主题 system + 主题 simulator + 主题 urban-fantasy + 主题 cross-time + 主题 anti-hero + 风格 buluofeng + 子变体 victorian-system-anti-hero

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["system", "simulator", "urban-fantasy", "cross-time", "anti-hero"]  # 5 主题叠加
风格变体: ["buluofeng-style-v2"]
子变体: ["victorian-system-anti-hero"]
```

**实际效果**：
- 基底：7 坐标轴（多POV/事件驱动/长句+中段/...）
- 主题叠加：系统+模拟+都市奇幻+穿越+反英雄（不落风 5 主题全加载）
- 不落风风格：系统作为第二叙事声音+反英雄吐槽+角色+系统双声
- 子变体：维多利亚+系统+反英雄+24h 模拟+系统结算

### 示例 2：中国网文基底 + 主题 system + 主题 level-up + 主题 ensemble

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["system", "level-up", "ensemble"]
风格变体: ["buluofeng-style-v2"]
```

**效果**：中国网文 7 坐标轴 + 系统+升级+群像主题 + 不落风系统作为第二叙事声音。

### 示例 3：中国网文基底 + 主题 system + 主题 doomsday + 风格 fengyue + 风格 buluofeng（双风格叠加）

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["system", "doomsday"]
风格变体: ["fengyue-style-v2", "buluofeng-style-v2"]  # 双风格叠加
```

**效果**：中国网文 7 坐标轴 + 系统+末日主题 + 风月+不落风双风格（实验性"末日+系统"）。

---

## 八、变更记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-30 | 初版（含主题相关项）|
| v2.0 | 2026-06-30 | **5 维正交化**——移除所有主题/题材相关项；只装不落风特定叙述态度+域词+桥段选择 |

---

> **本风格层的工程定位**：
> - 路径：`framework/templates/_styles/buluofeng-style.md`
> - 工程价值：可与中国网文基底 + `_themes/` 主题层独立正交叠加
