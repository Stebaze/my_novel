---
profile_id: "kuiguannan-style-v2"
version: "v2.0 (5 维正交化——移除所有主题相关项)"
status: 风格层（与基底/主题正交）
design_date: "2026-06-30"
supersedes: "kuiguannan-style-v1.md"
author: "葵关南"
analyzed_works:
  - "碧阳学园学生会默示录 (2008-2012, 9卷)"
  - "桌游咖（玩乐关系）(2018-2020, 3卷)"
  - "电玩咖 (2014-, 2卷+)"
orthogonal_with:
  - "framework/templates/_style-bases/* (2 基底)"
  - "framework/templates/_themes/* (8 主题族)"
design_principle: "本风格层只装葵关南特定的'叙述态度+域词+桥段选择'——不装主题/题材/基底"
---

# 葵关南风格层 v2.0（5 维正交化）

> **核心设计原则**：v2.0 移除所有主题/题材相关项——它们已移到 `_themes/` 主题层。
>
> **v2.0 只装**：葵关南特定的**叙述态度**（自嘲+吐槽+元叙事）+ **域词**（IP 戏仿+桌游域偏好）+ **桥段选择**（葵关南特定桥段）
>
> **5 维正交**：基底 × 主题 × 风格 × 子变体 × 题材特化

---

## 零、风格层定位

**葵关南特定风格**（与日轻共性基底的差异）：
- 葵关南特定的"叙述态度"= 自嘲式吐槽 + 元叙事自觉 + 跨作品 IP 戏仿
- 葵关南特定的"域词偏好"= 桌游域/学园议题/电玩游戏的"葵关南式用法"（不是单纯领域沉浸）
- 葵关南特定的"桥段选择"= 会议式吐槽（碧阳独有）+ 桌游-关系同构（桌游咖）+ TVGT 大赛（电玩咖）

**v1.0 vs v2.0**：v1.0 含"领域装置驱动/3 领域子变体/物理小物/必死的日常"等主题相关项——v2.0 已全部移除到 `_themes/`（具体为 `daily-life/romance/ensemble/scifi-fantasy` 等主题族）。

---

## 一、葵关南特定叙述态度（5 项）

### 态度 1：自嘲式吐槽（葵关南签名）

| 维度 | 葵关南默认 | 备注 |
|------|----------|------|
| 叙述者自贬 | 主角"自知路人/宅/小人物" | 番长/杉崎键/雨野 |
| 吐槽密度 | 22-35% 对话占比 | 高密度 |
| 与"日轻自嘲"基底区别 | 葵关南特有"番长式吐槽" | "按轻小说规律……" "我就烂但我有桌游" |
| 与基底层关系 | 沿用日轻基底"自嘲式亲密" | 葵关南特定实现 |

### 态度 2：元叙事自觉（葵关南式）

| 维度 | 葵关南默认 | 备注 |
|------|----------|------|
| 形式 | "按轻小说规律……" | 碧阳 9 卷稳定 |
| 频率 | 每卷 3-5 次 | 葵关南元叙事较密集 |
| 与基底层关系 | 沿用日轻基底"自嘲式亲密" | 葵关南特定为"轻小说元叙事" |

### 态度 3：跨作品 IP 戏仿（葵关南签名）

| 维度 | 葵关南默认 | 备注 |
|------|----------|------|
| 形式 | 角色名字戏仿（"真仪瑠鸟游" / "宇佐君" / "番长"）| 葵关南签名 |
| 跨读者群体 | 宅圈/桌游圈/电玩圈 | 葵关南跨圈覆盖 |
| 效果 | 跨作品 IP 借用 | 跨 3 作共有 |
| 与基底层关系 | 风格特定——不属于基底 |

### 态度 4：会议式吐槽（碧阳独有，跨作品罕见）

| 维度 | 葵关南默认 | 备注 |
|------|----------|------|
| 场景 | 5 角色固定会议 | 碧阳 9 卷模板 |
| 对话密度 | **55-65%**（会议密集型）| 远高于基底默认 20-40% |
| 说话模式 | 「议题抛出 → 全员吐槽 → 会长"嗯哼"转话题 → 戳破关键信息 → "四面楚歌"密室感余韵」| 5 步结构 |
| 与主题关系 | **关联 daily-life + school 主题**——已移到主题层 |

### 态度 5：双线自嘲+封手决胜（葵关南特定）

| 维度 | 葵关南默认 | 备注 |
|------|----------|------|
| 形式 | "我没事"="太喜欢了" | 出口 vs 内心 1-2 步鸿沟 |
| 高潮 | 节拍级失败承认 | 葵关南特定（不是雨森焚火"败级核心"）|
| 与基底层关系 | 沿用日轻基底"角色选择型" | 葵关南特定实现 |

---

## 二、葵关南特定域词（白名单）

### 葵关南 IP 戏仿域词

| 类型 | 词 | 备注 |
|------|---|------|
| 跨作品名 | "碧阳"/"桌游咖"/"电玩咖" | 葵关南签名 |
| 角色名 | "番长"/"宇佐君"/"米芙露"/"知弦 S"/"小鸟游" | 葵关南角色库 |
| 设定 | "DRAMAGA"/"Sword World"/"INDEX"/"生徒会"/"笑神"/"秀逗魔导士" | 碧阳 9 卷用语 |

### 葵关南桌游偏好域词（与桌游主题叠加时启用）

| 类型 | 词 | 备注 |
|------|---|------|
| 桌游术语 | "区域占优"/"拖延策略"/"快速止损"/"Kingmaker"/"downtime"/"长考"/"判定"/"手牌"/"回合"/"GM"/"卡坦岛"/"小麦" | 葵关南桌游咖用语 |
| 卡牌游戏 | "TCG"/"卡牌轮抽" | 葵关南电玩咖用语 |
| 桌游-关系同构 | 葵关南特定——用桌游术语表达情感博弈 | 风格特定 |

---

## 三、葵关南特定桥段选择（4 个）

### 桥段 1：Kingmaker 决胜（桌游咖）

| 维度 | 葵关南默认 | 备注 |
|------|----------|------|
| 机制 | 桌游胜负=情感真相揭露 | "对方把'小麦'给情敌" |
| 收束 | 自爆型选择+情感爆发 | 葵关南特定 |
| 与主题关系 | 关联 `tablegame` 主题——已移到主题层 |

### 桥段 2：会议决胜（碧阳独有）

| 维度 | 葵关南默认 | 备注 |
|------|----------|------|
| 机制 | 议题抛出+全员吐槽+会长"嗯哼"+戳破关键信息+密室感 | 5 步结构 |
| 收束 | 承认问题存在+不解决问题 | 葵关南特定 |
| 与主题关系 | 关联 `school` 主题——已移到主题层 |

### 桥段 3：大赛决胜（电玩咖）

| 维度 | 葵关南默认 | 备注 |
|------|----------|------|
| 机制 | 多游戏随机抽选+角色被迫展示不擅长 | TVGT 大赛 |
| 收束 | 学对方定型句+拿下 1 局 | 葵关南特定 |
| 与主题关系 | 关联 `dianwan` 主题——已移到主题层 |

### 桥段 4：辣妹反逻辑解构

| 维度 | 葵关南默认 | 备注 |
|------|----------|------|
| 机制 | 主角用"领域内逻辑"解释+解构者用"低俗/边缘"案例戳破 | 葵关南签名 |
| 收束 | 主角"被戳破"后的自嘲 | 葵关南特定 |

---

## 四、子变体（4 个，与主题层叠加使用）

### 子变体 1：biyang-conference（碧阳会议子变体）

```yaml
sub_variant: "biyang-conference"
activation: "与主题 school + daily-life 叠加时启用"
character_set: "5 固定角色"  # 杉崎键/樱野玖璃梦/知弦/深夏/真冬
overrides:
  attitude_4_meeting: "always-on"  # 会议式吐槽强制
  dialogue_density: "55-65%"  # 会议式对话密度
  climax_resolution: "conference-decision"  # 会议决断
```

### 子变体 2：tablegame-domain-embedding（桌游咖子变体）

```yaml
sub_variant: "tablegame-domain-embedding"
activation: "与主题 tablegame + romance 叠加时启用"
character_set: "番长+小鸟游+米芙露+月乃+宇佐君"
overrides:
  attitude_5_failure_acknowledgment: "beat-level"  # 节拍级失败承认
  climax_resolution: "tablegame-kingmaker"  # 桌游决胜
  physical_object_required: true  # 卡牌/桌游道具
```

### 子变体 3：dianwan-multi-pov（电玩咖多 POV 子变体）

```yaml
sub_variant: "dianwan-multi-pov"
activation: "与主题 dianwan 叠加时启用"
character_set: "雨野+三角+天道+上原+星之守+亚玖璃"
overrides:
  pov: "multi-pov-rotation"  # 多 POV 轮转
  ensemble_size: 6
  climax_resolution: "tournament-decision"  # 大赛决胜
```

### 子变体 4：kuiguannan-translation-ja（翻译腔子变体）

```yaml
sub_variant: "kuiguannan-translation-ja"
activation: "与 theme-daily-life 叠加且希望带翻译腔轻盈感时启用"
overrides:
  translation_register: "active"  # 翻译腔密度激活
  long_noun_phrase_pct: "15%+"
  passive_voice_residual_pct: "5%+"
  sentence_end_markers: ["~的说", "~嘛", "~呢"]
```

---

## 五、工程可加载参数（风格层默认配置）

### sensory-writer style_profile（葵关南风格层默认）

```yaml
style_profile:
  profile_id: "kuiguannan-style-v2"
  type: "light-novel-author-specific"
  # 葵关南特定叙述态度
  narrative_attitude: "self-deprecation-roast"  # 自嘲+吐槽
  meta_narrative: "frequent"  # 元叙事频繁
  ip_parody: "required"  # 跨作品 IP 戏仿必填
  meeting_roast: "optional"  # 会议式吐槽（碧阳独有）
  failure_acknowledgment: "beat-level"  # 节拍级失败承认
  # 葵关南特定域词（白名单）
  no_ban_words:  # 葵关南签名词
    - "健全"
    - "有病"
    - "碧阳"
    - "桌游咖"
    - "电玩咖"
    - "番长"
    - "宇佐君"
    - "米芙露"
    - "知弦 S"
    - "小鸟游"
  ip_parody_words: ["DRAMAGA", "Sword World", "INDEX", "生徒会", "笑神", "秀逗魔导士"]
  tablegame_words: ["区域占优", "拖延策略", "快速止损", "Kingmaker", "downtime", "长考", "判定", "手牌", "回合", "GM", "卡坦岛", "小麦"]
  translation_register: "default-off"
  # 不装任何主题/题材相关项
```

### handoff 字段（风格层默认）

```yaml
style_profile_type: "japanese-light-novel-base-v1.2"  # 基底（必填）
style_profile_themes: []  # 主题层（必填，如 ["school", "romance"]）
style_profile_variant: "kuiguannan-style-v2"  # 风格层
style_profile_subvariant: ""  # 子变体（按需：biyang-conference / tablegame-domain-embedding / dianwan-multi-pov / kuiguannan-translation-ja）
```

---

## 六、与 6 作家风格层的正交关系

| 风格层 | 与 kuiguannan-style 的关系 | 组合建议 |
|------|------------|---------|
| amamorin-style | 同源（同一作者不同笔名）| **可叠加**（雨森焚火 + 葵关南 = 葵关南全风格）|
| shiniki-style | 互补（推理 vs 校园）| 可叠加（实验性）|
| yuantong-style | 根本对照 | **不建议叠加** |
| fengyue-style | 根本对照 | **不建议叠加** |
| buluofeng-style | 根本对照 | **不建议叠加** |

---

## 七、5 维正交组合示例

### 示例 1：日轻基底 + 主题 school + 主题 romance + 主题 tablegame + 风格 kuiguannan + 子变体 biyang-conference

```yaml
主风格档案: "japanese-light-novel-base-v1.2"
主题: ["school", "romance", "tablegame"]  # 主题叠加
风格变体: ["kuiguannan-style-v2"]
子变体: ["biyang-conference"]
```

**实际效果**：
- 基底：7 坐标轴（第一人称/关系驱动/短句+极短段/...）
- 主题 school：学园场景/学生角色
- 主题 romance：8+ 女主/物理小物/失败承认
- 主题 tablegame：桌游域/桌游-关系同构/桌游咖啡馆
- 葵关南风格：自嘲+吐槽+元叙事+IP 戏仿（番长/碧阳/宇佐君）
- 子变体 biyang-conference：5 固定角色+会议式吐槽+55-65% 对话密度

### 示例 2：中国网文基底 + 主题 school + 主题 romance + 风格 kuiguannan（实验性）

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["school", "romance"]
风格变体: ["kuiguannan-style-v2"]
```

**实际效果**：
- 基底：7 坐标轴（多POV/事件驱动/长句+中段/...）——**与葵关南风格部分冲突**（POV/推进）
- 葵关南风格：自嘲+吐槽+IP 戏仿

**工程警告**：此组合违反基底层坐标轴 1/2——应警告。

---

## 八、变更记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-30 | 初版（从葵关南-默认.md v2.1 拆出风格层，但混入主题相关项）|
| v2.0 | 2026-06-30 | **5 维正交化**——移除所有主题/题材相关项；只装葵关南特定叙述态度+域词+桥段选择 |

---

> **本风格层的工程定位**：
> - 路径：`framework/templates/_styles/kuiguannan-style.md`
> - 工程价值：可与 `japanese-light-novel-base-v1.2` 基底 + `_themes/` 主题层独立正交叠加
