---
name: outline-tingle
description: 大纲形成编排——从零 premise→主题→L1→L2→L3，2 session 薄封装层（original + adaptation 双 mode）
---

# Outline-Tingle Skill — 大纲形成编排

## Identity

大纲形成编排器——薄封装层，对标 `adaptation-workflow` 范式。不重复实现发散/grilling 方法论，仅串联 `idea-explorer`(mode=book) + `qing-novelist`(mode=book) 完成 premise→L3 全程。2 session 形态：Session 1 divergent（premise→主题），Session 2 grilling（主题→L1→L2→L3）。`outline.md` 本身作为书级 handoff 载体（frontmatter `workflow_position` 状态机管进度，不另建 handoff 文件——interaction-spec §2.4 书级例外）。

**核心差异**（vs `plan-chapter`）：plan-chapter 假定 outline.md L1-L3 已填实；outline-tingle 负责把它们从 `（待定）` 填到实质。plan-chapter 产章节级 handoff（8 字段）；outline-tingle 推进 outline.md frontmatter 状态机。

## Contract

| Aspect | Detail |
|--------|--------|
| **Input `mode`** | `original` \| `adaptation`（默认 `original`；`adaptation` 由 `adaptation-workflow` 阶段 0.5 调用，详见下方 adaptation mode 分支） |
| **Calls** | `pre-flight-check`（启动门禁，含 C9 outline 实质填充检查）, `xuanji`（Session 1 前置——seed 缺失时引导作者调，**不直接 Skill 调用**，由作者执行 `/xuanji`）, `idea-explorer`(mode=book, Session 1, **original mode only**, 接 `seed_path` 从 seed 富材料发散), `qing-novelist`(mode=book, Session 2；adaptation mode 额外激活 B9 原作对齐度；读 outline.md + `seed_path`), `file-manager`(ensure-novel/ensure-draft，经 init-draft 间接调), `settings-manager`(init-draft, Session 2 末) |
| **Produces** | `outline.md`（Premise 段含 seed 指针 prose + 三字段蒸馏 + L1-L3 填实 + frontmatter `workflow_position` 推进；adaptation mode 额外含 B9 三态标注 + 改编深度声明）/ `project-config.md`（最小集）/ `_briefs/book-exploration.md`（idea-explorer 产，**original mode only**）/ 草稿目录。**seed 文件由 `xuanji` 产出，本 Skill 只读不写** |
| **Called by** | 用户入口（`/outline-tingle` Session 1 / `/outline-tingle continue` Session 2）；adaptation mode 由 `adaptation-workflow` 阶段 0.5 内部调 |

## Triggers

- "从零写新书" / "我有 premise 想形成大纲" / "帮我定全书结构"
- `/outline-tingle`（Session 1 divergent）/ `/outline-tingle continue`（Session 2 grilling）
- "想写一个 XX 的故事但不知道怎么展开" / "premise 到大纲怎么落"

## Flow

### 启动判定（两 session 共用入口）

```
1. mode 判定：original（默认）/ adaptation（→ adaptation mode 分支）
2. 模式分支判定：
   ├── mode=original → 读 novel/project-config.md（若存在）——「创作模式 = 改编」→ 🚫 硬阻断：
   │     "改编流大纲形成由 adaptation-workflow 阶段 0.5 调本 Skill mode='adaptation' 触发，请改用 /adaptation-workflow"
   └── mode=adaptation → 跳过上述硬阻断（本 Skill 即由 adaptation-workflow 阶段 0.5 调用，
         本来就在改编流内），改读原作画像存在性：
         ├── reference/manuscripts/_analysis/{作品名}.md 存在 → 继续（原作画像作为 Session 1 divergent 素材源）
         └── 不存在 → 🚫 硬阻断："原作画像未提取，请先跑 /adaptation-workflow 阶段 0（原作画像提取），
             再回到阶段 0.5 调本 Skill"
         project-config.md「创作模式」校验：存在则确认 = 改编（否则 🚫 硬阻断提示配置不一致）；
         **缺失则按"创作模式=改编"隐式继续**——project-config.md 由本 Skill Session 2 步骤 2.7A 正式落盘，
         首次改编流在 Session 1 阶段不要求该文件存在（避免与阶段 0.5 落盘动作循环依赖）
3. 扫描 novel/chapters/ 有内容 → 🟡 软阻断警告：
   "检测到已有成稿，建议改用 /bootstrap-project 逆向产大纲；如需重提主题可放行进修订模式
    （修订模式完整流程 Out of Scope，本 commit 仅留此警告）" → 用户确认放行
4. 调 Skill("pre-flight-check", scope="writing") 做启动门禁（C0-C9 跑过）
5. 读 outline.md frontmatter workflow_position 判定 session：
   ├── 空/缺失/非 outline-tingle-* → Session 1
   ├── outline-tingle-step1-done → Session 2（grilling 入口）
   ├── outline-tingle-l1-confirmed → Session 2 续（L2/L3 未完，断点续传）
   └── outline-tingle-step2-done → "大纲已形成，请用 /plan-chapter 1 开始章节规划"
```

### adaptation mode 分支

改编流的 Session 1/2 与原创流共用骨架——前置输入、divergent 引擎、第九维 grilling 增量不同。本节声明与原创流的**差异点**，未声明的步骤（门禁 1/2/3、frontmatter 状态机推进、project-config.md 与草稿初始化）与原创流一致。

#### 启动判定差异

mode=adaptation 时启动判定步骤 2 已分流（见上方"启动判定"）：跳过原创流的"创作模式=改编 → 🚫 硬阻断"，改为读原作画像 `reference/manuscripts/_analysis/{作品名}.md` 存在性。原作画像由 `adaptation-workflow` 阶段 0 提取，缺失时硬阻断提示先跑 `/adaptation-workflow`。

#### Session 1：原作画像 → 候选改编主题（adaptation mode, divergent 替换）

```
1.0A seed 前置检查（同原创流 1.0，🟡 软阻断 + 降级路径）：
    改编 seed = 作者改编意图碎片（留什么/砍什么/注入什么），由 xuanji 产出（adaptation-workflow 阶段 0.5 引导）。
    seed 存在 + convergence_status: done → 进 1.1A；缺失 → 软阻断提示先 /xuanji（降级路径无 seed 富材料）。
1.1A 读原作画像 reference/manuscripts/_analysis/{作品名}.md：
    六维画像（主题/角色/情节/世界观/风格/缺陷标记）作为改编主题发散的外部素材源
    + 读 _briefs/premise-seed.md「核心种子 + 碎片表」——作者改编意图碎片（留/砍/注入）作为内部素材源
1.2A 内联 divergent（不调 idea-explorer mode=book）：
    以原作画像 + seed 改编意图为素材，列 3-5 个候选改编主题方向，每个 50-100 字陈述句，覆盖典型改编策略：
    - 保留主线：复刻原作主线骨架，仅置换世界观外壳
    - 删减支线：剥离 1-2 条次要支线，主线节奏收紧
    - 改结局：保留前段铺垫，重写结局走向（悲/喜反转、开放式）
    - 换视角：从原作配角/反派视角重述主线
    - 主题转译：原作主题在当代/异文化语境的变体
    每条陈述含"保留什么/改什么/为何这样改"三要素（保留/改/注入对照 seed 意图碎片）
1.3A 作者选定改编主题方向（同原创流 1.3，本 Skill 引导作者从一览表选）
1.4A 写入 outline.md Premise 段（原始一句话=原作一句话概括 + 改编方向标签；
    灵感来源=原作画像路径；期望读者感受=改编主题陈述）+ 加 seed 指针 prose 行
    + L1 核心主题/一句话/终点画面草稿
1.5A 推进 frontmatter：workflow_position: outline-tingle-step1-done /
    produced_by: outline-tingle / produced_at: <ts> / mode: adaptation / resume_command: /outline-tingle continue
1.6A 【门禁 1·可暂缓】同原创流 1.6
```

#### Session 2：改编主题 → L1 → L2 → L3（adaptation mode, grilling + 第九维）

```
2.1A 读 outline.md 现状（Premise 段 + L1 已填部分字段 + frontmatter）
    → 确认 workflow_position = outline-tingle-step1-done（否则提示先跑 Session 1）
2.2A 调 Skill("qing-novelist", mode="book", outline_path=<outline.md>, seed_path=<_briefs/premise-seed.md>, adaptation=true)
    → 补 L1：与原创流 2.2 相同的 B1/B2/B6/B7/B8 + 新增 B9 原作对齐度
    （qing-novelist 读 outline.md + seed 核心种子/缺口/冲突；adaptation mode seed 含改编意图碎片）
    （详见 qing-novelist/_reference/book-conversation-guide.md §B9；adaptation=true 参数激活 B9）
    B9 在 L1 末激活：每条 L1 字段标注"保留 / 改 / 新增"三态之一，汇总为改编深度声明
2.3A-2.6A 同原创流 2.3-2.6（门禁 2/3 + L2/L3 grilling，B9 在 L2/L3 阶段对每卷/每篇
    亦标注"保留 / 改 / 新增"三态）
2.7A 写 project-config.md（最小集）：创作模式=改编 / 原作来源=画像路径 / 写作类型 / 节拍窗口 /
    叙事人称 / 叙事基调 / 类型标签，其余字段填（待定）
2.8A-2.10A 同原创流 2.8-2.10（init-draft + 2.8.5 书级设定派发 [B9 三态不派发，留 outline 宪法层] +
    推进 frontmatter workflow_position:
    outline-tingle-step2-done + 完成提示）
```

#### adaptation mode 产出契约

- `outline.md` frontmatter `mode: adaptation` + `workflow_position: outline-tingle-step2-done`
- `outline.md` L1-L3 实质填充（无 `（待定）`），每条字段含 B9 三态标注（保留/改/新增）+ L1 含改编深度声明
- `project-config.md`「创作模式 = 改编」+「原作来源」字段已填
- 草稿目录已初始化（init-draft）

### Session 1：Premise → 主题（original mode, divergent）

> **seed 前置**：`_briefs/premise-seed.md`（由 `xuanji` 产出，frontmatter `convergence_status: done`）是 Session 1 的工作输入。三字段 Premise 不再由作者当场口述——作者持有的残留碎片由 `xuanji` 先收敛成 seed，本 Skill 从 seed 三字段蒸馏写 Premise 段。

```
1.0 seed 前置检查：
    ├── seed 存在 + convergence_status: done → 读 seed 三字段蒸馏段，进 1.1（seed 路径）
    └── seed 缺失 / status: in-progress → 🟡 软阻断：
        "seed 未收敛——建议先 /xuanji 理清残留碎片（下游 idea-explorer/qing-novelist 读 seed 富材料发散/grilling）。
         确认放行则走降级路径：口述 premise 直写 Premise 段 3 字段（无 seed 指针），下游读 3 字段 Premise（无富材料）。"
        作者确认放行 → 降级路径（1.1' 口述 premise → 写 Premise 段 3 字段无指针；1.2 idea-explorer 不传 seed_path）
1.1 [seed 路径] 读 _briefs/premise-seed.md「三字段蒸馏」段 → 写入 outline.md Premise 段 3 子项
    + 加指针 prose 行：> **seed**：`_briefs/premise-seed.md`（璇玑产出，下游 idea-explorer/qing-novelist 读作工作输入）
1.2 调 Skill("idea-explorer", mode="book", seed_path=<_briefs/premise-seed.md>)
    → 思源从 seed 富材料（核心种子 + 碎片表 + 缺口）发散，产 _briefs/book-exploration.md
    （7 法应用到 seed→候选主题方向，≥3 个方向，50-100 字主题陈述句）
    [降级路径] 不传 seed_path → 思源读 outline.md Premise 段 3 字段发散（旧行为）
1.3 作者选定主题（idea-explorer 不做选择，本 Skill 引导作者从一览表选）
1.4 写入 outline.md L1 部分字段（草稿）：
    核心主题（选定主题）/ 一句话概括（草稿，B1 细化）/ 终点画面（草稿，B8 细化）
1.5 推进 frontmatter：workflow_position: outline-tingle-step1-done /
    produced_by: outline-tingle / produced_at: <ts> / mode: original / resume_command: /outline-tingle continue
1.6 【门禁 1·可暂缓】展示已填字段 + 待填字段清单（L1 主角起终/规则/隐喻、L2、L3 均待 Session 2）
    → 不阻断，提示："主题已选定。开新对话输入 /outline-tingle continue 进入 Session 2 收敛 L1→L2→L3。"
```

### Session 2：主题 → L1 → L2 → L3（original mode, grilling）

```
2.1 读 outline.md 现状（Premise 段 + L1 已填部分字段 + frontmatter）
    → 确认 workflow_position = outline-tingle-step1-done（否则提示先跑 Session 1）
2.2 调 Skill("qing-novelist", mode="book", outline_path=<outline.md>, seed_path=<_briefs/premise-seed.md>) → 补 L1：
    （qing-novelist 读 outline.md 现状 + seed 核心种子/缺口/冲突作 grilling 参考；seed 缺失降级读 outline.md only）
    B1 主题深度（细化核心主题+一句话）/ B2 主角弧光起终 / B8 终点画面（细化）/
    B6 不可违背规则（3-5 条带编号）/ B7 核心隐喻
    每维 50-100 字结构陈述句，作者确认 → 本 Skill 写入 outline.md L1 对应字段
2.3 【门禁 2·不可暂缓】读 qing-novelist 返回 l1_ready：
    ├── true → 推进 frontmatter workflow_position: outline-tingle-l1-confirmed → 进 L2
    └── false → 🚫 拦截："L1 未全部填实（待填：<字段>），L1 不可暂缓。
        建议回 /outline-tingle Session 1 重新发散主题，或继续 grilling 补齐。"
2.4 L2 分卷：qing-novelist mode=book 继续激活 B3（分卷核心问题）+ B5（关系里程碑，卷级）
    → 每卷 卷主题/情感目标/剧情目标/大高潮/卷末状态/本卷新角色 → 写入 outline.md L2
2.5 L3 篇章：qing-novelist mode=book 继续激活 B4（篇章高潮分布）+ B5（关系里程碑，篇级）
    → 每篇 篇章功能/核心问题/关键事件链/角色聚焦/关系里程碑/情感曲线/结尾钩子 + 章位表 → 写入 outline.md L3
2.6 【门禁 3·可暂缓但状态机不推进】读 qing-novelist 返回 handoff_ready：
    ├── true → 进 2.7
    └── false → ⚠️ 提示待填字段，用户可选补齐或暂缓（暂缓则 workflow_position 停在 l1-confirmed）
2.7 写 project-config.md（最小集，其余字段填（待定））：
    创作模式=原创 / 写作类型 / 节拍窗口大小（长篇55·中篇30·短篇10-15）/ 叙事人称 / 叙事基调 / 类型标签
    frontmatter：format_version: 1 / produced_by: outline-tingle / produced_at: <ts> / chapter: book + sections（保留模板）
2.8 调 Skill("settings-manager", operation="init-draft") → 创建草稿目录（内部调 file-manager ensure-novel + ensure-draft）
2.8.5 书级设定派发：把 `outline.md` L1-L3 已定型字段派发到草稿目录设定文件的对应段（骨架占位），让下游 plan-chapter 阶段 1 设定快照能读到非空骨架。
    **派发前清空目标段**（Read 定位段 → Edit 替换整段），保证崩溃重跑幂等。**缺失文件补齐**：从 `framework/templates/` 拷对应模板到草稿目录再派发。**骨架占位原则**：只填书级 grilling 已定型字段，未定型段留 `（待定）`。
    **🟡 软阻断降级**：模板缺失/段 heading 不存在 → 记录软阻断清单，不阻塞大纲完成（`outline.md` 仍是真相源）。**adaptation mode B9 三态不派发**：original/adaptation 派发逻辑统一，三态标注留 outline 宪法层。

    Q3 映射表（outline.md 字段 → 设定文件段）：

    | outline.md 来源字段 | 派发目标 1 | 派发目标 2 |
    |---------------------|-----------|-----------|
    | B2 主角弧光起终（L1「主角起点状态 → 终点状态」） | `characters/{主角}.md`「角色弧线」段（起点状态/终点状态两项） | `character-arcs.md`「一、弧光总览」表（主角行）+「二、各角色弧光详情」段（弧光主题/起点状态/终点状态三项） |
    | B5 关系里程碑（L2 卷级） | `character-arcs.md`「三、关系里程碑进度」段（每条里程碑一行） | `characters/{主角}.md`「人际关系」段（关系类型/当前阶段） |
    | B6 不可违背规则（L1「不可违背的规则」3-5 条带编号） | `world/rules.md`「核心规则」段（每条规则一行） | — |
    | L2 每卷「本卷新角色」 | `characters/{新角色}.md` 全文骨架（从 `framework/templates/characters/_template.md` 拷贝；基本信息段填姓名，其余段留模板默认占位） | — |
    | L2 卷主题 / L3 篇章功能 | `thread-map.md`「一、主线推进状态」段（每卷一行：卷/阶段/阶段描述=卷主题/下一里程碑=该卷首篇篇章功能） | — |

    派发执行顺序：
    1. 读 `outline.md` L1-L3，提取 B2/B5/B6/L2 新角色/L2 卷主题/L3 篇章功能字段
    2. 对每个目标文件：缺失则从 `framework/templates/` 拷模板到草稿目录对应路径
    3. 对每个目标段：Read 定位段 heading → 用派发内容替换整段（保留段 heading 与后续分隔）
    4. 派发完成（含软阻断降级清单）→ 置 frontmatter `book_settings_dispatched: true`

    派发产出（草稿目录下）：
    - `characters/{主角}.md`（弧线段含 B2 起终，人际关系段含 B5；其余段保留模板默认/`（待定）`）
    - `characters/{新角色}.md`（每卷新角色各一份，全文骨架）
    - `character-arcs.md`（一/二/三段含 B2/B5 派发内容）
    - `world/rules.md`（核心规则段含 B6 规则）
    - `thread-map.md`（一、主线推进状态段含卷主题/篇章功能）
2.9 推进 frontmatter：workflow_position: outline-tingle-step2-done / produced_at: <ts> / resume_command: /plan-chapter 1
2.10 完成提示："大纲已形成 + 草稿已初始化。说「写第 1 章」即可开始 /plan-chapter 1。"
```

> **outline.md frontmatter 状态机**（8 字段）：`format_version` / `produced_by` / `produced_at` / `mode` / `workflow_position` / `resume_command` / `pending_confirm` / `book_settings_dispatched`。Session 1 末推进 `workflow_position: outline-tingle-step1-done`；Session 2 门禁 2 通过后推进 `outline-tingle-l1-confirmed`；2.8.5 派发完成置 `book_settings_dispatched: true`；2.9 推进 `workflow_position: outline-tingle-step2-done`。`book_settings_dispatched` 是派发状态的单一真相源——下游 pre-flight-check C10 检测该字段判提醒。

## Completion Criterion

- ✅ Checkable：
  - Session 1（original）：返回 `{mode: "original", session: 1, exploration_path, theme_selected, outline_l1_partial_filled, workflow_position: "outline-tingle-step1-done"}` —— exploration_path 指向 `_briefs/book-exploration.md`；outline.md Premise 段 + L1 核心主题/一句话/终点画面已填（草稿）
  - Session 2（original）：返回 `{mode: "original", session: 2, outline_fields_filled: [...], l1_ready, handoff_ready, project_config_path, draft_dir, workflow_position: "outline-tingle-step2-done"}` —— outline.md L1-L3 实质填充（无 `（待定）`），project-config.md 已落盘，草稿目录已创建
  - Session 1（adaptation）：返回 `{mode: "adaptation", session: 1, portrait_path, theme_direction_selected, outline_l1_partial_filled, workflow_position: "outline-tingle-step1-done"}` —— portrait_path 指向 `reference/manuscripts/_analysis/{作品名}.md`；outline.md Premise 段 + L1 部分字段已填（草稿）；无 `book-exploration.md`（adaptation 不调 idea-explorer）
  - Session 2（adaptation）：返回 `{mode: "adaptation", session: 2, outline_fields_filled: [...], l1_ready, handoff_ready, project_config_path, draft_dir, workflow_position: "outline-tingle-step2-done", adaptation_depth: "保留 X% / 改 Y% / 新增 Z%"}` —— outline.md L1-L3 实质填充 + B9 三态标注 + 改编深度声明；project-config.md「创作模式=改编」已落盘；草稿目录已创建
- ✅ Exhaustive：
  - Session 1（original）：步骤 1.1-1.6 全部执行；idea-explorer mode=book 已调用；outline.md Premise 段 + L1 部分字段已写入；frontmatter 已推进到 step1-done
  - Session 2（original）：步骤 2.1-2.10 全部执行；qing-novelist mode=book 已调用；L1 全部填实（门禁 2 通过）；L2/L3 填实（门禁 3 通过）；project-config.md + 草稿已落盘；2.8.5 派发已执行 + `book_settings_dispatched: true`；frontmatter 已推进到 step2-done
  - Session 1（adaptation）：步骤 1.1A-1.6A 全部执行；原作画像已读取；3-5 个候选改编主题方向已列；作者选定已记录；outline.md Premise + L1 部分字段已写入；frontmatter `mode: adaptation` + step1-done
  - Session 2（adaptation）：步骤 2.1A-2.10A 全部执行；qing-novelist mode=book(adaptation=true) 已调用；L1 全部填实 + B9 改编深度声明 + 三态标注（门禁 2 通过）；L2/L3 填实 + 每卷/每篇 B9 三态标注（门禁 3 通过）；project-config.md「创作模式=改编」+ 草稿已落盘；2.8.5 派发已执行 + `book_settings_dispatched: true`（B9 三态不派发）；frontmatter `mode: adaptation` + step2-done
- 🚫 Stop：不调 plan-chapter——让用户自己触发下一章

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `idea-explorer` Skill（mode=book，接 `seed_path`） | Session 1 步骤 1.2（**original mode only**；adaptation mode 内联 divergent 不调） | 🚫 硬阻断——主题发散不可降级（adaptation mode 不适用） |
| `qing-novelist` Skill（mode=book，接 `outline_path` + `seed_path`，adaptation mode 激活 B9） | Session 2 步骤 2.2/2.4/2.5 | 🚫 硬阻断——书级 grilling 不可降级 |
| `_briefs/premise-seed.md`（xuanji 产出，`convergence_status: done`） | Session 1 步骤 1.0 前置检查（original + adaptation） | 🟡 软阻断——缺失提示先 `/xuanji`；作者确认放行走降级路径（口述 premise，下游无富材料） |
| `reference/manuscripts/_analysis/{作品名}.md` 原作画像 | adaptation mode 启动判定步骤 2（**adaptation mode only**） | 🚫 硬阻断——画像缺失提示先跑 `/adaptation-workflow` 阶段 0 |
| `settings-manager` Skill（init-draft） | Session 2 步骤 2.8 | 🚫 硬阻断——草稿初始化不可跳过 |
| `file-manager` Skill | Session 2 步骤 2.8（init-draft 间接调） | 🚫 硬阻断——草稿目录无法建立 |
| `pre-flight-check` Skill | 启动判定步骤 4 | 🚫 硬阻断——启动门禁不可跳过 |
| `novel/outline.md` | 两 session 核心 IO | 🚫 硬阻断——缺失时调 file-manager(ensure-novel) 补齐 v2 模板；frontmatter 8 字段状态机（含 `book_settings_dispatched`） |
| `novel/project-config.md` | 启动判定 + Session 2 产出 | ⚠️ 启动判定时缺失按原创模式继续 |

## 与其他组件的关系

| 组件 | 关系 |
|------|------|
| `idea-explorer` Skill | Session 1 调用（mode=book，**original mode only**，接 `seed_path`）——seed→候选主题方向，产 `book-exploration.md`；adaptation mode 不调用，改内联读原作画像 + seed 发散 |
| `qing-novelist` Skill | Session 2 调用（mode=book，接 `outline_path` + `seed_path`）——主题→L1→L2→L3 书级 grilling，读 seed 核心种子/缺口/冲突作参考；adaptation mode 额外激活 B9 原作对齐度（保留/改/新增三态 + 改编深度声明，详见 `_reference/book-conversation-guide.md` §B9） |
| `xuanji` Skill | 上游——产出 `_briefs/premise-seed.md`（`convergence_status: done`）作 Session 1/2 工作输入；本 Skill 只读 seed 不写，seed 缺失时软阻断引导作者 `/xuanji` |
| `plan-chapter` Skill | 下游——本 Skill 产出 outline.md L1-L3 填实后，plan-chapter 读大纲跑章节规划 |
| `adaptation-workflow` Skill | 改编流——阶段 0.5 调本 Skill mode="adaptation"（本 commit 实现）；original mode 启动判定检测到改编模式时硬阻断导向 adaptation-workflow |
| `bootstrap-project` Skill | 互补可串——本 Skill 正向产大纲后，bootstrap 可逆向补 voice/character/world（Commit 7 加跳过 1a 逻辑）；启动判定检测到已有成稿时建议 bootstrap |
| `pre-flight-check` Skill | 启动门禁（C9 outline 实质填充检查；adaptation mode 下 `workflow_position: outline-tingle-step2-done` 时 C9 直接放行） |
| `framework/templates/outline.md` | v2 模板（Commit 1 升级）——本 Skill 产出的落点，frontmatter 8 字段状态机 |
| `framework/templates/project-config.md` | 最小集配置模板——本 Skill Session 2 末填充 |
