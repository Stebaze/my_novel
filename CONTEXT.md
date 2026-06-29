# 小说写作工程

AI 辅助长篇小说写作工程的领域语言。21 个 Skill 按 plan → handoff → generate → review → publish 主线协作；书级前置由 outline-tingle 完成大纲形成。

## 碎片与种子

**残留碎片 (residual fragment)**:
作者在开始写作（或写作中途）持有的一系列尚未结构化、需要工具辅助理清的想法与要素——角色、场景、主题、世界观、意象、感受、母题等。开放集合：grilling 过程中作者会持续抛入新碎片。
_Avoid_: 灵感（太宽，与灵感来源混）、想法（无结构意）、点子（已被 premise 占用）

**Premise（原始点子）**:
书级 handoff 起点。`outline.md` Premise 段三字段蒸馏——原始一句话 / 灵感来源 / 期望读者感受。是 seed 的宪法级摘要，不再是下游 skill 的工作输入。
_Avoid_: 主题（被 L1 核心主题占用）、核心点子

**seed（premise-seed）**:
`_briefs/premise-seed.md`，单本单文件、evolving。结构化沉淀全部残留碎片：7 类型打标 + 聚类 + 核心种子 + 缺口 + 冲突 + 未决停车场 + 三字段蒸馏。是下游 idea-explorer / qing-novelist 的工作输入。
_Avoid_: 种子文件、premise 文件

**收敛 (convergence)**:
璇玑执行的 grilling 纪律——把残留碎片堆理清：打标、聚类、识别核心种子、表面缺口与冲突。分析性扫描退为 incidental，不独立成阶段。
_Avoid_: 整理（无 grilling 意）、归纳（太弱）

**发散 (divergence)**:
思源（idea-explorer）执行的纪律——围绕焦点生成"如果…会怎样"的多种可能性。收敛的对冲：收敛把堆理清，发散把焦点打开。
_Avoid_: 头脑风暴（口语化）

**核心种子 (core seed)**:
seed 中被识别为高价值的少数碎片——将驱动主题选定与 L1 宪法。其余碎片为装饰性或待激活。
_Avoid_: 主线碎片、关键想法

**缺口 (gap)**:
收敛表面化的结构缺失——如"有角色无世界"、"有感受无场景"。是 idea-explorer 发散与 qing-novelist L1 grilling 的待补指向。
_Avoid_: 待办（与 todo 混）

**冲突 (conflict)**:
收敛表面化的碎片间矛盾——两个碎片无法在同一个宪法下共存。需作者在进 L1 前裁决。
_Avoid_: 矛盾（太泛）

**未决停车场 (parking lot)**:
seed 中暂不裁决、留待后续 session 处理的碎片。避免过早收敛压制开放性。
_Avoid_: 待办池、暂存区

## 工具身份

**火花 (spark)**:
碎片捕获工具——append-only 单行 bullet 流落盘 `novel/inspiration-log.md`，零交互。横切工件，不属任何编排层。是璇玑的上游：散记。
_Avoid_: 记录本、灵感本

**璇玑 (xuanji)**:
碎片收敛 grilling 工具——读 inspiration-log + 当场口述 + live 注入，产 seed。解耦，任意时点 `/xuanji` 可调，不绑 outline-tingle session 脊柱。与火花形成捕获→聚炼上下游；与思源形成收敛→发散对冲。
_Avoid_: 碎片整理器

**三字段蒸馏 (three-field distillation)**:
seed 产出的宪法级摘要——原始一句话 / 灵感来源 / 期望读者感受。由 outline-tingle 从 seed 写入 `outline.md` Premise 段，供人读与 state machine 引用，非工作输入。
_Avoid_: premise 三件套

## 状态

**convergence_status**:
seed 文件内部字段，`in-progress → done`。混合判定：agent 提议结构化完成（全打标/聚类/核心已识/缺口冲突已表面）→ 作者确认翻 done。outline-tingle Session 1 入口以"seed 文件存在 + convergence_status: done"为前置信号（类 generate-chapter 的 handoff 检查），不加 outline.md frontmatter 状态。
_Avoid_: seed_ready、收敛完成标志
