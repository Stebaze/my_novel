---
profile_id: "theme-mystery-v1"
version: "v1.0"
status: 主题层（与基底/风格正交）
design_date: "2026-06-30"
orthogonal_to:
  - "framework/templates/_style-bases/* (2 基底)"
  - "framework/templates/_styles/* (6 作家风格层)"
themes_in_family: ["mystery", "detective", "supernatural", "neet", "mystery-romance"]
design_principle: "本主题族 = 推理/侦探/超自然/NEET 主题；不装基底坐标轴；不装作家风格"
---

# 主题族：推理/侦探/超自然/NEET（theme-mystery-v1）

> **核心定位**：本主题族装"推理/侦探/超自然/NEET"领域的题材内容——**不装基底坐标轴**，**不装作家风格**。
>
> **可叠加**：可与基底正交叠加，可与作家风格层独立叠加。

---

## 零、主题族包含

| 主题 | 描述 | 典型代表作品 |
|------|------|------------|
| **mystery（推理）** | 谜题/真相/委托人 | 杉井光神之记事本 |
| **detective（侦探）** | 侦探/助手/委托 | 杉井光神之记事本 |
| **supernatural（超自然）** | 幽灵/灵异/超能力/死者 | 杉井光神之记事本（卷 1 ANGEL·FIX/卷 9 爱丽丝之死）|
| **neet（NEET）** | NEET 边缘人/茧居/家里蹲/御宅族 | 杉井光神之记事本 |
| **mystery-romance（推理恋爱）** | 推理+恋爱 | （混合主题）|

---

## 一、领域装置（必需）

| 主题 | 领域装置 | 关键特征 |
|------|---------|--------|
| mystery | 谜题/真相/排除法 | "为什么发生"而非"谁干的" |
| detective | 委托-侦探-助手/调查 | 委托机制+爱丽丝型侦探 |
| supernatural | 幽灵/灵异/超能力/死者 | 现实主义中插入超自然 |
| neet | 拉面店/2ch/秋叶原/御宅族文化 | 2007-2014 东京秋叶原 |
| mystery-romance | 谜题+爱情线索 | 混合 |

---

## 二、关系障碍（主题相关）

| 障碍类型 | 占比 | 主题相关 |
|---------|-----|---------|
| NEET 边缘人 | ~30% | neet 强——被社会视为"无法使用的人" |
| 社会隔离 | ~25% | neet 强——不出门无法建立传统关系 |
| 侦探+普通人信任 | ~20% | detective 强 |
| 死亡（不可逆）| ~15% | mystery/supernatural 强 |
| 谜题解答/委托人隐瞒 | ~10% | mystery 强 |

---

## 三、关系网规模

| 主题 | 规模 | 互动模式 |
|------|------|---------|
| mystery | 5-10 角色 | 等权重共同战线 |
| detective | 5-10 角色 | 委托-雇主权力倒置 |
| supernatural | 5-8 角色 | 现实+超自然双层 |
| neet | 5-8 角色 | 边缘人互助网络 |
| mystery-romance | 5-10 角色 | 混合 |

---

## 四、推进单位

| 主题 | 推进单位 | 跨章衔接 |
|------|---------|--------|
| mystery | **一次委托+一次推理** | 委托登门+调查+排除+爱丽丝独白 |
| detective | 一次委托+一次推理 | 同上 |
| supernatural | 一次委托+一次超自然遭遇 | 现实锚点+超自然插入 |
| neet | 一次共同战线任务+一次吐槽 | 团队小剧场+日常锚点 |
| mystery-romance | 一次委托+一次恋爱互动 | 混合 |

---

## 五、高潮模式

| 主题 | 高潮类型 | 收束模式 |
|------|---------|--------|
| mystery | **反转式**（死者真正想说的话）| "死者想说的是 X" |
| detective | 反转式 | 同上 |
| supernatural | 反转式 | 超自然揭示 |
| neet | 反转式 | 必死的日常+反转 |
| mystery-romance | 反转式+角色选择 | 混合 |

---

## 六、死亡模式

| 主题 | 死亡 | 备注 |
|------|------|------|
| mystery | **物理死亡（每卷≥1 次）** | 杉井光式 |
| detective | 物理死亡 | 同上 |
| supernatural | 物理死亡 | 同上 |
| neet | 物理死亡 | 同上 |
| mystery-romance | 物理死亡 | 同上 |

---

## 七、物理道具

| 主题 | 物理道具 | 备注 |
|------|---------|------|
| mystery | 委托物/线索/档案 | 推理 |
| detective | Dr.Pepper/拉面/棒球/福尔摩斯引文 | 杉井光式 |
| supernatural | 超自然物品 | 推理+超自然 |
| neet | 御宅族周边/2ch 段子 | NEET 文化 |
| mystery-romance | 混合 | 混合 |

---

## 八、内容配比建议

| 内容类型 | mystery | detective | supernatural | neet |
|---------|---------|-----------|-------------|------|
| 推理/排除法 | 35% | 35% | 30% | 20% |
| 对话/吐槽 | 25% | 25% | 25% | **40%** |
| 日常锚点 | 15% | 15% | 15% | 20% |
| 内心独白 | 15% | 15% | 20% | 15% |
| 超自然 | 0% | 0% | **10%** | 0% |
| 元叙事/吐槽 | 10% | 10% | 0% | 5% |

---

## 九、5 维正交组合示例

### 示例 1：日轻基底 + 主题 detective + 主题 supernatural + 主题 neet + 风格 shiniki

```yaml
主风格档案: "japanese-light-novel-base-v1.2"
主题: ["detective", "supernatural", "neet"]
风格变体: ["shiniki-style-v1"]
```

**效果**：日轻 7 坐标轴 + 委托-侦探+超自然+NEET 边缘人 + 杉井光委托-死者代言人推理 + 双轨制内心通道。

### 示例 2：日轻基底 + 主题 mystery + 风格 custom-author-style

```yaml
主风格档案: "japanese-light-novel-base-v1.2"
主题: ["mystery"]
风格变体: ["custom-author-style"]
```

**效果**：日轻 7 坐标轴 + 推理主题（谜题/排除法/必死的日常）+ 作者自创风格。

### 示例 3：中国网文基底 + 主题 detective（实验性）

```yaml
主风格档案: "chinese-webnovel-base-v1.2"
主题: ["detective"]
风格变体: []
```

**效果**：中国网文 7 坐标轴（多POV/事件驱动/...）+ 推理主题——实验性"中国网文事件驱动 + 推理"。

---

## 十、与其他主题族的边界

| 主题族 | 与本主题族的差异 |
|------|----------|
| daily-life（日常/校园/职场）| 日常无死亡——本主题族有物理死亡 |
| romance（恋爱/后宫/败犬）| 恋爱无死亡——本主题族有 |
| scifi-fantasy（科幻/奇幻/玄幻）| 科幻有"硬规则"——本主题族现实+微超自然 |
| doomsday（末日/启示/仪式）| 末日有"末日背景"——本主题族是日常现实 |

---

## 十一、变更记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-30 | 初版（从杉井光神之记事本.md v2.0 抽象主题族）|

---

> **本主题族的工程定位**：
> - 路径：`framework/templates/_themes/theme-mystery.md`
> - 工程价值：让 mo-writer/sensory-writer/chapter-review 等 Skill 在加载 `style_profile_themes = ["mystery", "detective", "neet", ...]` 时自动获取推理主题相关项
