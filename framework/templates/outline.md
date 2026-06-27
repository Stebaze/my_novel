---
format_version: 2
produced_by: ""
produced_at: ""
mode: original
workflow_position: ""
resume_command: /outline-tingle
pending_confirm: []
sections:
  - heading: "## Premise（原始点子）"
    skills: [outline-tingle]
    desc: "书级 handoff 起点——原始一句话/灵感来源/期望读者感受；outline-tingle Session 1 由此发散主题"
  - heading: "## L1：全书级"
    skills: [plan-chapter, qing-novelist, mo-writer]
    desc: "宪法级别——书名/核心主题/终点画面/主角起终状态/不可违背规则/一句话概括/类型标签/核心隐喻"
  - heading: "## L2：分卷级"
    skills: [plan-chapter, qing-novelist]
    desc: "每卷的核心问题/关键事件/角色弧光阶段/关系里程碑"
  - heading: "## L3：篇章级"
    skills: [plan-chapter, mo-writer]
    desc: "卷内篇章划分——篇章主题/章数范围/高潮点分布"
  - heading: "## L4：章节级"
    skills: [mo-writer, plan-chapter]
    desc: "每章的核心事件和功能定位"
  - heading: "## L5：场景级"
    skills: [mo-writer]
    desc: "每场景的节拍设计——最细粒度的事件编排"
  - heading: "## 角色出场率追踪"
    skills: [plan-chapter, qing-novelist, ping-critic]
    desc: "各角色出场频率统计——检测某些角色是否被遗忘或过度使用"
  - heading: "## 关系里程碑进度"
    skills: [plan-chapter, qing-novelist]
    desc: "各关系线的阶段推进追踪"
  - heading: "## 爆点计划与交付"
    skills: [plan-chapter, mo-writer, ping-critic]
    desc: "已规划的爆点+已交付的爆点+差距分析"
  - heading: "## 伏笔追踪"
    skills: [plan-chapter, qing-novelist, ping-critic]
    desc: "全书画笔埋设/揭示/待回收的全量追踪"
  - heading: "## 多视角一致性检查"
    skills: [ping-critic]
    desc: "多POV作品中各视角信息一致性验证"
---

# 全书大纲

> **导航地图**：本文档按照五级大纲体系组织（详见 `framework/guides/narrative-engineering.md`）。
> Agent 在每次写作前读取对应级别，在每次写完后更新对应追踪表。

---

## Premise（原始点子）

> **书级 handoff 起点**——`outline-tingle` Session 1 从此段读 premise 发散到主题；frontmatter `workflow_position` 推进书级状态机。

- **原始一句话**：（待定）
- **灵感来源**（可空）：（待定）
- **期望读者感受**：（待定）

---

## L1：全书级

> **宪法级别**。以下内容一旦确定，修改必须记录到 `notes.md` 决策表并同步所有下级大纲。

- **书名**：（待定）
- **核心主题**：（待定）
- **终点画面**（最后一卷最后一章，读者合上书看到什么、感受到什么）：（待定）
- **主角起点状态 → 终点状态**：（待定）
- **不可违背的规则**（连载膨胀的刹车；3-5 条，每条带编号，便于门禁精确引用）：
  1. （待定）
  2. （待定）
  3. （待定）

### 一句话概括

> （待定）

### 类型标签与核心卖点

- **类型标签**：（待定）
- **核心卖点**（读者为什么选这本）：
  1. （待定）
  2. （待定）
  3. （待定）
- **目标平台**：（待定）
- **计划卷数/总字数**：待定

### 核心隐喻/意象

> （待定）

---

## L2：分卷级

> 每卷是一个独立的"情感产品"——新读者从此卷开始也能享受。
> 同时每卷在 L1 主线中承担不可替代的功能。

### 第一卷：（待定）

| 字段 | 内容 |
|------|------|
| **卷主题** | （待定） |
| **情感目标**（读者读完感受到什么） | （待定） |
| **剧情目标**（在主线中不可替代的推进） | （待定） |
| **大高潮** | （待定） |
| **卷末状态** | （待定） |
| **本卷新角色** | （待定） |

---

## L3：篇章级（第一卷）

> 每卷分为若干篇章，每篇 5-7 章，是一个完整的"迷你电影"。
> 每篇有独立的核心问题和情感曲线。

### 第一篇：（待定）

- **篇章功能**：（待定）
- **核心问题**：（待定）
- **关键事件链**：（待定）
- **角色聚焦**：（待定）
- **关系里程碑**：（待定）
- **情感曲线**：（待定）
- **结尾钩子**：（待定）

| 章位 | 章节 | 标题 | 功能 | 核心内容 | 字数 | 状态 |
|------|------|------|------|----------|------|------|
| 开端 | 1 | （待定） | （待定） | （待定） | 待定 | ⬜ |

---

> **状态标记说明**：⬜ 未写 / ✍️ 写作中 / ✅ 初稿完成 / 🔴 需重写 / ⭐ 定稿

---

## L4：章节级

> 每章使用 `framework/templates/chapters/_chapter-template.md`。在此只保留跨章追踪信息。

### 篇章衔接检查

| 篇章 | 结束时角色状态变化 |
|------|------------------|
| | |

---

## L5：场景级

> 每章内的场景规划使用"场景规划卡"（见 `framework/guides/narrative-engineering.md` 第五章）。

---

---

> **动态追踪数据已分离**：
> - 角色弧光 + 关系里程碑 + 出场率 → [`character-arcs.md`](character-arcs.md)
> - 主线/支线/伏笔/线索交织 → [`thread-map.md`](thread-map.md)
>
> 本文件仅保留大纲规划（L1-L5）。写作过程中的追踪数据更新到上述文件。

---

## 多视角一致性检查

> 每写完一卷，Agent 从四个视角执行交叉检查。

### 作者视角（可持续性）
- [ ] 下一卷 L3 篇章结构已规划
- [ ] 无角色超过 10 章无实质进展
- [ ] 无伏笔超过 2 卷未触碰
- [ ] 未偏离 L1 终点方向

### 编辑视角（经济性）
- [ ] 本卷每个场景都有不可删除的理由
- [ ] 事件链是因果链而非"and then"链
- [ ] 情感节拍按计划交付

### 老读者视角（深度一致性）
- [ ] 伏笔揭示有回响感
- [ ] 角色行为无前后矛盾
- [ ] 世界观规则无被违反

### 新读者视角（可进入性）
- [ ] 从本卷 Ch1 开始读能理解角色关系
- [ ] 前情通过场景自然带出
- [ ] 有至少 1-2 个场景"没读过前文也能享受"

---

## 附录 A：参考作品大纲结构模式

> 6 种大纲结构模式已迁移至 [`framework/guides/reference-material.md` §一](../guides/reference-material.md#一大纲结构模式6-种)。
> 选择最接近你作品类型的 1-2 种作为结构参考。
>
> 通过 `qing-novelist`（作者分析模式）分析参考作品后，可将新发现的结构模式添加到 `novel/outline.md` 本附录中。
