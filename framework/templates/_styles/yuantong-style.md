---
profile_id: "yuantong-style-v2"
version: "v2.0 (5 维正交化——移除所有主题相关项)"
status: 风格层（与基底/主题正交）
design_date: "2026-06-30"
supersedes: "yuantong-style-v1.md"
author: "远瞳"
analyzed_works:
  - "异常生物见闻录 (2017-2018, 1773章)"
  - "黎明之剑 (2018-2020, 1593章)"
  - "深海余烬 (2022-2024, 851章)"
orthogonal_with:
  - "framework/templates/_style-bases/* (2 基底)"
  - "framework/templates/_themes/* (8 主题族)"
design_principle: "本风格层只装远瞳特定的'叙述态度+域词+桥段选择'——不装主题/题材/基底"
---

# 远瞳风格层 v2.0（5 维正交化）

> **核心设计原则**：v2.0 移除所有主题/题材相关项——已移到 `_themes/` 主题层（具体为 `scifi-fantasy/ensemble` 主题族）。
>
> **v2.0 只装**：远瞳特定的**叙述态度**（双层信息差+三层叙述距离+碎嘴+市井幽默）+ **域词**（远瞳式自反词）+ **桥段选择**（三阶释放高潮+宏微反差）
>
> **5 维正交**：基底 × 主题 × 风格 × 子变体 × 题材特化

---

## 零、风格层定位

**远瞳特定风格**（与中国网文共性基底的差异）：
- 远瞳特定的"叙述态度"= 双层信息差叙述+三层叙述距离切换+碎嘴+市井幽默
- 远瞳特定的"域词"= 远瞳式自反词（"卧槽""妈个鸡""这剧本不对"）+ 远瞳式白名单
- 远瞳特定的"桥段选择"= 三阶释放高潮（认知+权力+视觉）+ 群像 4 梯队频次分布+宏微反差

**v1.0 vs v2.0**：v1.0 含"双层信息差叙述/三阶释放高潮/群像 4 梯队/克苏鲁+科学+地球梗"等主题相关项——v2.0 已移除主题相关项。

---

## 一、远瞳特定叙述态度（4 项）

### 态度 1：双层信息差叙述（远瞳签名）

| 维度 | 远瞳默认 | 备注 |
|------|---------|------|
| 双层 | 读者 > 主角心理 > 外人感知 | 远瞳深海独有 |
| 效果 | 持续性幽默张力 | "风太大我听不见" vs "绚烂扭曲的星光扑面而来" |
| 与基底层关系 | 沿用中国网文基底"信息差机制" | 远瞳特定为"双层"实现 |

### 态度 2：三层叙述距离切换（远瞳发明）

| 维度 | 远瞳默认 | 备注 |
|------|---------|------|
| 距离 1（近）| 30% 贴身 | 角色内心 |
| 距离 2（中）| 55% 标准 | 第三人称叙述 |
| 距离 3（远）| 15% 卫星视角 | 黎明高文式哲思段落 |
| 来源 | 黎明之剑发明 | 远瞳特定 |
| 与基底层关系 | 沿用中国网文基底"信息差机制" | 远瞳特定为"三层距离"实现 |

### 态度 3：碎嘴+市井幽默（远瞳签名）

| 维度 | 远瞳默认 | 备注 |
|------|---------|------|
| 形式 | 碎嘴吐槽+冷幽默+地球梗 | 远瞳签名 |
| 温度 | 冷（vs 风月暖/不落风温）| 远瞳特定 |
| 与基底层关系 | 沿用中国网文基底"信息差机制" | 远瞳特定为"碎嘴冷幽默" |

### 态度 4：远瞳式自反词（地球梗/网络文化自指）

| 维度 | 远瞳默认 | 备注 |
|------|----------|------|
| 形式 | "卧槽"/"妈个鸡"/"这剧本不对" | 远瞳签名 |
| 频率 | 仅在角色对话中出现（叙述者不使用）| 远瞳特定 |
| 与基底层关系 | 沿用中国网文基底 | 远瞳特定为"自反词"实现 |

---

## 二、远瞳特定域词（白名单）

### 远瞳式自反词

| 类型 | 词 | 备注 |
|------|---|------|
| 远瞳口头禅 | "卧槽" / "妈个鸡" / "妈耶" / "艹" / "邪门" / "这TM" | 远瞳汉化版特征 |
| 远瞳元评论 | "这剧本不对" / "这不符合XX的设定" / "就很离谱" | 远瞳签名 |
| 远瞳吐槽 | "过过过" | 远瞳签名 |
| 远瞳身份标签 | "建筑耗材" / "一带一路" | 远瞳地球梗 |

### 远瞳特定禁用/保留词

| 类别 | 词 | 备注 |
|------|---|------|
| 必保留 | "卧槽" / "妈个鸡" / "这剧本不对" | 远瞳签名 |
| 必保留 | "古神" / "深渊" / "灵界" / "大湮灭" / "幽邃恶魔" | 远瞳世界标识 |
| 必保留 | "双缝干涉" / "心智统一场" / "量子" / "弦理论" | 远瞳科学思维 |

---

## 三、远瞳特定桥段选择（3 个）

### 桥段 1：三阶释放高潮（远瞳签名）

| 阶段 | 描述 | 备注 |
|------|------|------|
| 阶 1 | 认知释放 | 终于明白真相/终于理解对方 |
| 阶 2 | 权力释放 | 主角隐藏身份/能力确认（如巨人形态）|
| 阶 3 | 视觉释放 | 华丽的、有视觉冲击力的收尾场景 |
| 跨作通用 | 异常/黎明/深海 3 作都有 | 远瞳特定 |
| 与主题关系 | 关联 `ensemble/scifi-fantasy` 主题——已移到主题层 |

### 桥段 2：宏微反差（远瞳+风月共有）

| 维度 | 远瞳默认 | 备注 |
|------|---------|------|
| 形式 | 史诗收尾 → 立刻日常吐槽 | 远瞳+风月共有 |
| 跨章节 | 浸入式+话说体 | 远瞳特定 |
| 与基底层关系 | 沿用中国网文基底 | 远瞳特定实现 |

### 桥段 3：群像 4 梯队频次分布（远瞳签名）

| 维度 | 远瞳默认 | 备注 |
|------|---------|------|
| 梯队 1（主角）| 频次 10000+ | 深海邓肯 10094 / 黎明高文 20995 |
| 梯队 2（核心吐槽）| 频次 2000-3000 | 深海凡娜/雪莉/爱丽丝 |
| 梯队 3（功能型）| 频次 1500-3000 | 深海阿加莎/妮娜/露克蕾西娅 |
| 梯队 4（重要配角）| 频次 1000-1500 | 深海山羊头/阿狗 |
| 群英会型 | 每角色都有自己的故事线+独立叙事价值 | 远瞳特定 |
| 与主题关系 | 关联 `ensemble` 主题——已移到主题层 |

---

## 四、子变体（3 个，与主题层叠加使用）

### 子变体 1：multi-pov-abyss（深海多 POV 深渊子变体）

```yaml
sub_variant: "multi-pov-abyss"
activation: "与主题 cosmic-horror + ensemble + scifi 叠加时启用"
character_set: "邓肯+凡娜+雪莉+爱丽丝+山羊头+阿狗"
overrides:
  inner_channel: "double-layer-info-gap"  # 双层信息差叙述
  climax_resolution: "three-stage-release"  # 三阶释放
```

### 子变体 2：multi-pov-civilization（黎明多 POV 文明子变体）

```yaml
sub_variant: "multi-pov-civilization"
activation: "与主题 multi-civilization + ensemble + political-intrigue 叠加时启用"
character_set: "高文+琥珀+瑞贝卡+卡迈尔+赫蒂+拜伦"
overrides:
  narrative_distance: "three-tier"  # 三层叙述距离切换
  climax_resolution: "three-stage-release"  # 三阶释放
```

### 子变体 3：multi-pov-cosmic（异常多 POV 宇宙子变体）

```yaml
sub_variant: "multi-pov-cosmic"
activation: "与主题 scifi + ensemble + cosmic-horror + isekai 叠加时启用"
character_set: "郝仁+数据终端+莉莉+薇薇安+渡鸦 12345"
overrides:
  inner_channel: "single-layer-rant"  # 异常单层叙述
  climax_resolution: "unit-arc-decision"  # 单元剧决断
```

---

## 五、工程可加载参数（风格层默认配置）

### sensory-writer style_profile（远瞳风格层默认）

```yaml
style_profile:
  profile_id: "yuantong-style-v2"
  type: "chinese-webnovel-author-specific"
  # 远瞳特定叙述态度
  information_gap_subtype: "double-layer"  # 双层信息差
  narrative_distance: "three-tier"  # 三层叙述距离
  voice_type: "roast-cold"  # 碎嘴+市井幽默（冷）
  self_referential_words: "required"  # 远瞳式自反词必填
  # 远瞳特定桥段
  climax_release: "three-stage"  # 三阶释放
  ensemble_structure: "4-tier-stepped"  # 4 梯队阶梯式
  macro_micro_contrast: "required"  # 宏微反差
  # 远瞳签名词（白名单）
  no_ban_words:  # 远瞳签名词（不视为违禁）
    - "卧槽"
    - "妈个鸡"
    - "妈耶"
    - "邪门"
    - "这TM"
    - "这剧本不对"
    - "这不符合XX的设定"
    - "就很离谱"
    - "过过过"
  translation_register: null  # 0 翻译腔（与基底层一致）
  # 不装任何主题/题材相关项
```

### handoff 字段（风格层默认）

```yaml
style_profile_type: "chinese-webnovel-base-v1.2"
style_profile_themes: []  # 主题层（必填，如 ["scifi", "ensemble", "cosmic-horror"]）
style_profile_variant: "yuantong-style-v2"
style_profile_subvariant: ""  # 子变体（按需：multi-pov-abyss / -civilization / -cosmic）
```

---

## 六、与 6 作家风格层的正交关系

| 风格层 | 与 yuantong-style 的关系 | 组合建议 |
|------|------------|---------|
| kuiguannan-style | 根本对照 | **不建议叠加** |
| amamorin-style | 根本对照 | **不建议叠加** |
| shiniki-style | 根本对照 | **不建议叠加** |
| fengyue-style | 部分同源（中国网文+末日意象）| **可叠加**（远瞳+风月 = 中国网文+科幻+末日）|
| buluofeng-style | 部分同源（中国网文+系统）| **可叠加**（远瞳+不落风 = 中国网文+科幻+系统）|

---

## 七、5 维正交组合示例

### 示例 1：中国网文基底 + 主题 scifi + 主题 cosmic-horror + 主题 ensemble + 主题 multi-civilization + 风格 yuantong + 子变体 multi-pov-abyss

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["scifi", "cosmic-horror", "ensemble", "multi-civilization"]  # 4 主题叠加
风格变体: ["yuantong-style-v2"]
子变体: ["multi-pov-abyss"]
```

**实际效果**：
- 基底：7 坐标轴（多POV/事件驱动/长句+中段/...）
- 主题叠加：科幻+克苏鲁+群像+多文明
- 远瞳风格：双层信息差+三层叙述距离+三阶释放
- 子变体：深海 4 角色（邓肯+凡娜+雪莉+爱丽丝）+ 双层信息差+三阶释放

### 示例 2：中国网文基底 + 主题 fantasy + 主题 multi-civilization + 主题 ensemble + 主题 political-intrigue + 风格 yuantong + 子变体 multi-pov-civilization

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["fantasy", "multi-civilization", "ensemble", "political-intrigue"]  # 4 主题叠加
风格变体: ["yuantong-style-v2"]
子变体: ["multi-pov-civilization"]
```

**效果**：中国网文 7 坐标轴 + 奇幻+多文明+群像+政治权谋主题 + 远瞳+黎明之剑 7 角色。

### 示例 3：中国网文基底 + 主题 scifi + 主题 ensemble + 主题 cosmic-horror + 主题 isekai + 风格 yuantong + 子变体 multi-pov-cosmic

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["scifi", "ensemble", "cosmic-horror", "isekai"]  # 4 主题叠加
风格变体: ["yuantong-style-v2"]
子变体: ["multi-pov-cosmic"]
```

**效果**：中国网文 7 坐标轴 + 科幻+群像+克苏鲁+异世界主题 + 远瞳+异常生物见闻录 5 角色。

### 示例 4：中国网文基底 + 主题 scifi + 主题 ensemble + 主题 cosmic-horror + 风格 yuantong + 风格 fengyue（双风格叠加）

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["scifi", "ensemble", "cosmic-horror"]
风格变体: ["yuantong-style-v2", "fengyue-style-v2"]  # 双风格叠加
```

**效果**：中国网文 7 坐标轴 + 科幻+群像+克苏鲁主题 + 远瞳+风月双风格（实验性"科幻+末日"）。

---

## 八、变更记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-30 | 初版（含主题相关项）|
| v2.0 | 2026-06-30 | **5 维正交化**——移除所有主题/题材相关项；只装远瞳特定叙述态度+域词+桥段选择 |

---

> **本风格层的工程定位**：
> - 路径：`framework/templates/_styles/yuantong-style.md`
> - 工程价值：可与中国网文基底 + `_themes/` 主题层独立正交叠加
