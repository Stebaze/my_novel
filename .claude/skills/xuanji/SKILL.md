---
name: xuanji
description: 碎片收敛 grilling——读 inspiration-log + 当场口述 + live 注入，产 _briefs/premise-seed.md（7 类型打标碎片 + 聚类 + 核心种子/缺口/冲突/未决停车场 + 三字段蒸馏）；解耦任意时点可调
---

# 璇玑 Skill — 碎片收敛 grilling

## Identity

「璇玑」(Xuan Ji) 碎片收敛 grilling 入口。职责是把作者持有的残留碎片堆理清——打标、聚类、识别核心种子、表面缺口与冲突、未决入停车场，产出结构化 `_briefs/premise-seed.md` 供下游 idea-explorer / qing-novelist 读作工作输入。**开放碎片集**：grilling 过程中作者会持续抛入新碎片。

**核心差异**（vs `idea-explorer`）：思源是*发散*（围绕焦点生成"如果…会怎样"的多种可能），璇玑是*收敛*（把碎片堆理清）。两者对冲——收敛在前把素材理清，发散在后把焦点打开。

**核心差异**（vs `spark`）：火花是*捕获*（append-only 单行 bullet 落盘 inspiration-log，零交互），璇玑是*聚炼*（把散记的 bullet 流 + 口述 + live 注入 grilling 成结构化 seed）。两者形成捕获→聚炼上下游。璇玑**不自动写 inspiration-log**——grilling 中作者抛的新碎片由作者 `/spark` 落盘（与 idea-explorer 既有规则一致，记录职责收敛在 spark）。

**解耦**：任意时点 `/xuanji` 可调，不绑 outline-tingle session 脊柱。首次在 outline-tingle Session 1 前调（产 seed 供发散/L1 grilling 用）；书程中途新碎片簇涌现时亦可复调（seed 是 evolving 单本单文件）。

## Contract

| Aspect | Detail |
|--------|--------|
| **Input** | 无 mode 参数——单形态。素材源：(a) `novel/inspiration-log.md` bullet 流（grep `^- \[`）+ (b) 当场口述碎片 + (c) grilling 中 live 注入（作者 `/spark` 落盘后拉入）+ (d) 既有 `_briefs/premise-seed.md`（续跑时读，evolving） |
| **Called by** | 用户直接 `/xuanji`；`outline-tingle` Session 1 入口检测 seed 缺失时引导作者调；`adaptation-workflow` 阶段 0.5 检测 seed 缺失时引导作者调（两流对称 wiring） |
| **Calls** | `file-manager` Skill（`ensure-novel` 间接保证 `novel/inspiration-log.md` 可达 + `ensure-draft` 保证 `_briefs/` 目录；首次写 seed 前 ensure-draft） |
| **Produces** | `_briefs/premise-seed.md`（首次创建 / 续跑原地更新，evolving）：7 类型打标碎片表（聚类 fold 进"簇"列）+ 核心种子 + 缺口 + 冲突 + 未决停车场 + 三字段蒸馏（6 H2 段）；frontmatter `format_version: 1` / `chapter: book` / `convergence_status: in-progress\|done` / `produced_by: xuanji` / `produced_at` / `produced_in_session`（首次/续跑标记）。返回 `{seed_path, convergence_status, core_seeds_count, gaps_count, conflicts_count, parking_lot_count}` |
| **Consumes** | `novel/inspiration-log.md`（横切工件，绕过草稿直接读）+ 既有 seed（续跑） |
| **Not calls** | `pre-flight-check`（璇玑在 outline-tingle 之前，C9 outline 实质填充对璇玑无意义；解耦任意时点可调，跑 pre-flight 过重）；`idea-explorer` / `qing-novelist`（璇玑是它们的上游，不反向调）；`spark`（记录职责收敛在 spark，璇玑只提示作者触发） |

## Triggers

- `/xuanji` —— 用户直接调
- "帮我把这些想法理清" / "我有一堆碎片想整理" / "这些点子怎么收"
- "我有 premise 想形成大纲"（outline-tingle Session 1 入口检测 seed 缺失时引导）
- "改编这个作品"（adaptation-workflow 阶段 0.5 检测 seed 缺失时引导）

## Flow

### Step 0: 前置 ensure

```
1. 调 Skill("file-manager", operation="ensure-draft") —— 保证 _briefs/ 目录存在
   （草稿优先：CLAUDE.md 规则 6，seed 落草稿 _briefs/；无活跃草稿时 file-manager 降级补齐 novel/_drafts/）
2. 检查 novel/inspiration-log.md 存在性：
   ├── 存在 → grep `^- \[` 提取 bullet 流作为素材源 (a)
   └── 缺失 → ⚠️ 提醒"inspiration-log 为空：作者若已有碎片建议先 /spark 捕获，或当场口述。空素材可继续（仅靠口述 + live 注入）"
3. 检查既有 _briefs/premise-seed.md：
   ├── 存在 → 读其结构化内容作为续跑基线 (d)，本次为 evolving 更新
   └── 缺失 → 首次创建，本次为初产
```

### Step 1: 素材汇总与初扫

```
1. 汇总素材源：
   - inspiration-log bullet 流（若非空）
   - 既有 seed 已结构化碎片（若续跑）
   - 询问作者："除了已记录的，还有哪些碎片没落盘？现在口述。"
     → 当场口述碎片 (b) 入池
2. 初扫（incidental，非独立阶段）：
   agent 浏览碎片池，按 7 类型 taxonomy 给每条碎片打标（可多标）：
   - 角色 / 场景 / 主题 / 世界观 / 意象 / 感受 / 母题 / other
   初步聚类相似项，**不在本步**判定核心/缺口/冲突——那些在 grilling 中浮现。
3. 展示初扫结果给作者确认："以下是你目前的碎片，按类型分组。有遗漏或归类错的请指出。"
```

### Step 2: 收敛 grilling（核心）

```
grilling 范式——单焦点逐条追问，每次只盯一个碎片。循环直至 agent 提议结构化完成。

对每条碎片（或每簇），追问四问（择相关）：
  Q1 归属：这条碎片属于 7 类型中的哪个（或哪几个）？初扫标签是否准确？
  Q2 内核：这条碎片背后想表达什么？它驱动什么（角色动机/世界规则/主题陈述/情感体验）？
  Q3 必要性：它与主角弧光/核心主题什么关系？是核心种子还是装饰性碎片？还是该入未决停车场？
  Q4 关系：它与池中其他碎片是聚合（同簇）/ 互补 / 冲突（无法在同一宪法下共存）？

 incidental 同步动作（边 grill 边做，不独立成阶段）：
  - 打标修正 / 聚类调整
  - 识别核心种子（高价值少数碎片，将驱动主题选定与 L1 宪法）
  - 表面缺口（结构缺失，如"有角色无世界"/"有感受无场景"）
  - 表面冲突（碎片间矛盾，需作者裁决）
  - 未决入停车场（暂不裁决，避免过早收敛压制开放性）

【开放碎片集处理】
grilling 中作者抛新碎片 →
  提示："这条请 /spark <一句话> 落盘，然后我拉入继续 grill。"
  （与 idea-explorer 既有规则一致——璇玑不自动写 inspiration-log，记录职责收敛在 spark）
  作者 /spark 后 → grep 重新拉取 bullet 流 → 新碎片入池 → 继续 grilling
  作者当场口述不愿落盘的碎片 → 直接入池（不强制 /spark），但提示"建议落盘以便后续 session 可达"

每轮 grilling 末展示当前 seed 草图（打标表 + 聚类 + 核心种子候选 + 缺口 + 冲突 + 停车场）让作者复核。
```

### Step 3: 完成判定（混合）

```
agent 判结构化完成条件（全部满足）：
  ✓ 全部碎片已打标（无 unlabeled）
  ✓ 聚类稳定（无悬空单条除非作者确认独立）
  ✓ 核心种子已识别（≥1 条，作者认可）
  ✓ 缺口已表面化（列清单，非必须补齐——缺口是下游 idea-explorer/qing-novelist 的待补指向）
  ✓ 冲突已表面化（列清单，非必须裁决——冲突可留停车场待 L1 前裁决）
  ✓ 三字段蒸馏草稿已写（原始一句话/灵感来源/期望读者感受）

→ agent 提议："结构化完成。核心种子 N 条 / 缺口 M 项 / 冲突 K 项 / 停车场 L 条。是否确认 done？
   （确认后 outline-tingle 可读 seed 进发散；冲突/缺口留待下游处理）"
→ 作者确认 → convergence_status: in-progress → done
→ 作者不确认（"还有碎片要加"/"核心种子没对"）→ 回 Step 2 继续 grilling
```

### Step 4: 产/更新 seed 文件

```
写 _briefs/premise-seed.md（首次创建 / 续跑原地更新，幂等——重写全文）：

---
format_version: 1
chapter: book
convergence_status: done
produced_by: xuanji
produced_at: <ts>
produced_in_session: initial | resume-<n>
core_seeds_count: N
gaps_count: M
conflicts_count: K
parking_lot_count: L
sections:
  - heading: "## 三字段蒸馏"
    skills: [outline-tingle]
  - heading: "## 核心种子"
    skills: [idea-explorer, qing-novelist]
  - heading: "## 碎片表（7 类型打标）"
    skills: [idea-explorer, qing-novelist]
  - heading: "## 缺口"
    skills: [idea-explorer, qing-novelist]
  - heading: "## 冲突"
    skills: [qing-novelist]
  - heading: "## 未决停车场"
    skills: [qing-novelist]
---

# Premise Seed

> 璇玑产出，单本单文件 evolving。下游 idea-explorer / qing-novelist 读作工作输入。

## 三字段蒸馏
- **原始一句话**：<从核心种子蒸馏的一句话>
- **灵感来源**：<作者口述 / inspiration-log 标签聚类>
- **期望读者感受**：<从感受类碎片蒸馏>

## 核心种子
（高价值少数碎片，将驱动主题选定与 L1 宪法）
1. <碎片> —— <为何是核心>
2. ...

## 碎片表（7 类型打标）
| 碎片 | 类型 | 簇 | 备注 |
|------|------|----|------|
| ... | 角色/场景/主题/世界观/意象/感受/母题/other | <簇名或独立> | |

## 缺口
（结构缺失，下游待补指向）
- <缺口描述> —— <下游谁补>

## 冲突
（碎片间矛盾，需 L1 前裁决）
- <冲突>：<碎片 A> vs <碎片 B>

## 未决停车场
（暂不裁决，留待后续 session）
- <碎片> —— <暂缓原因>

返回 {seed_path, convergence_status: "done", core_seeds_count, gaps_count, conflicts_count, parking_lot_count}
```

## Completion Criterion

- ✅ Checkable：返回 `{seed_path, convergence_status: "done", core_seeds_count: N, gaps_count: M, conflicts_count: K, parking_lot_count: L}` —— `_briefs/premise-seed.md` 已落盘，frontmatter `convergence_status: done`，六段（三字段蒸馏/核心种子/碎片表/缺口/冲突/未决停车场）均有内容或显式标注"无"
- ✅ Exhaustive：Step 0-4 全部执行；inspiration-log 已读（或空素材提醒已发）；初扫 + grilling 循环至作者确认 done；seed 文件六段已写；frontmatter `convergence_status: done` + `produced_by: xuanji`
- 🚫 Stop：不调 idea-explorer / qing-novelist——让 outline-tingle 编排者读 seed 进下一阶段；不调 outline-tingle——编排由用户触发

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `file-manager` Skill（ensure-draft） | Step 0 | 🚫 硬阻断——_briefs/ 目录无法建立则 seed 无落点 |
| `novel/inspiration-log.md` | Step 0/1 素材源 (a) | ⚠️ 提醒不阻断——空素材继续（仅靠口述 + live 注入） |
| 既有 `_briefs/premise-seed.md` | Step 0 续跑基线 (d) | 首次缺失正常——按初产处理 |
| 作者参与（grilling + 完成判定确认） | Step 2/3 | 🚫 硬阻断——grilling 不可无人值守自动跑 |

## 与其他组件的关系

| 组件 | 关系 |
|------|------|
| `spark` Skill | 上游——火花捕获碎片到 inspiration-log，璇玑读 bullet 流聚炼。璇玑 grilling 中作者抛新碎片时提示作者 `/spark` 落盘（不自动写） |
| `idea-explorer` Skill | 下游——思源 mode=book 改接 `seed_path`，从 seed 富材料（核心种子 + 碎片表 + 缺口）发散候选主题方向。璇玑是思源的上游收敛 |
| `qing-novelist` Skill | 下游——五更 mode=book 读 outline.md + `seed_path`，L1 grilling 参考 seed 的核心种子/缺口/冲突。冲突清单是 L1 前裁决指向 |
| `outline-tingle` Skill | 编排者——Session 1 入口检查 seed 存在 + `convergence_status: done`，缺失导 `/xuanji`；1.4 从 seed 三字段蒸馏写 outline.md Premise 段 + 指针 prose |
| `adaptation-workflow` Skill | 改编流——阶段 0.5 调 outline-tingle mode=adaptation 前加 seed 检查，缺失导 `/xuanji`。改编 seed = 作者改编意图碎片（留什么/砍什么/注入什么），与原作画像（外部素材）分离 |
| `pre-flight-check` Skill | 不调用——璇玑在 outline-tingle 之前，C9 outline 实质填充对璇玑无意义；解耦任意时点可调，跑 pre-flight 过重 |

## taxonomy（7 类型 + other）

| 类型 | 含义 | 下游消费 |
|------|------|---------|
| 角色 | 人物碎片——身份/动机/关系/弧光端点 | qing-novelist B2 主角弧光 |
| 场景 | 画面/事件碎片——发生了什么 | idea-explorer 发散素材 |
| 主题 | 这本书想表达什么 | idea-explorer 候选主题方向 / qing-novelist B1 主题深度 |
| 世界观 | 世界规则/设定碎片 | qing-novelist B6 不可违背规则 |
| 意象 | 反复出现的象征物/隐喻 | qing-novelist B7 核心隐喻 |
| 感受 | 期望读者感受/情感体验 | 三字段蒸馏「期望读者感受」 |
| 母题 | 贯穿全书的反复结构（复仇/成长/救赎等） | idea-explorer 候选主题方向 |
| other | 不属上述——grilling 中可能升华出新类型 | 停车场待定 |
