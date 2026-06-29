# 新增 xuanji（璇玑）碎片收敛层：在发散前理清残留碎片堆

outline-tingle Session 1 在 premise 之后直接进 idea-explorer 的发散，缺一层把作者持有的残留碎片堆理清的收敛。根因是缺收敛工具（3 字段 Premise 压缩过狠 + 一次性 prompt 入口是症状）。决定新增独立 skill `xuanji`（璇玑），身份=碎片收敛 grilling，产 `_briefs/premise-seed.md`（单本单文件 evolving，含 7 类型打标碎片 + 聚类 + 核心种子 + 缺口 + 冲突 + 未决停车场 + 三字段蒸馏）。xuanji 解耦——任意时点 `/xuanji` 可调，不绑 outline-tingle session 脊柱，可复用于书程中途新碎片簇。outline-tingle Session 1 入口检查 seed 存在 + `convergence_status: done`（**🟡 软阻断**，类 C9 outline 实质填充检查的"尊重网文边写边定"哲学——seed 是上游素材理清而非门禁，作者可确认放行走降级路径：口述 premise 直写 Premise 段 3 字段无 seed 指针，下游读 3 字段 Premise 无富材料；**降级路径下三字段 Premise 临时回任工作输入**，与默认"三字段降为宪法蒸馏"形成有条件例外）；idea-explorer mode=book 改接 `seed_path` 从富材料发散；qing-novelist mode=book 读 outline.md + `seed_path` 参考 seed 的核心/缺口/冲突；三字段 Premise 默认降为宪法蒸馏。adaptation 流对称 wiring——adaptation-workflow 阶段 0.5 检查 seed，改编 seed = 作者改编意图碎片（留什么/砍什么/注入什么），与原作画像分离共喂内联 divergent。收敛机制=grilling 式 + 开放碎片集（grilling 中作者持续抛新碎片，由作者 `/spark` 落盘，xuanji 不自动写 inspiration-log，与 idea-explorer 既有规则一致）。完成判定=混合（agent 提议结构化完成→作者确认翻 done）。taxonomy=轻量固定 7 类型（角色/场景/主题/世界观/意象/感受/母题 + other）。

## Considered Options

- **折叠进 qing-novelist 作 mode=seed**（否决）：身份契合（grilling），但 qing-novelist 表面区已三 mode（chapter / book / 作者分析），第四 mode 进一步膨胀；且碎片收敛与 L1-L3 grilling 是不同抽象层（前者理清素材、后者定宪法），混进同一 skill 模糊职责。独立 skill 身份最干净。
- **inline 进 outline-tingle Session 1 作 1.x 阶段**（否决）：零 skill 增量，但与"解耦、任意时点可调、可复用于书程中途新碎片簇"目标冲突——inline 把收敛钉死在 outline-tingle session 脊柱上，且项目正在做减层重构（草稿层镜像、原稿层删除），inline 加重 Session 1 与减层方向相悖。
- **3 session 形态（收敛独立成 S1）**（否决）：每个 session 干净上下文窗口，但把璇玑钉进 outline-tingle session 序列，破坏解耦目标。改为 outline-tingle Session 1 入口"检查 seed 缺失则导 `/xuanji`"——xuanji 是 peer 级前置而非脊柱节点。
- **outline.md Premise 段扩为多字段结构化 / seed 取代三字段**（否决）：outline.md 是宪法层、人读 + state machine 引用，结构化碎片堆属于工作产物层（`_briefs/`）。改用 seed 文件 + Premise 段保三字段加指针，宪法层与工作产物层分离，与 book-exploration.md 同层。
- **加 outline.md frontmatter `seed_converged` 字段 / `workflow_position: outline-tingle-seed-done` 中间态**（否决）：与 seed 文件内部 `convergence_status` 重复，双真相源风险。xuanji 解耦于 outline-tingle，其进度不该污染 outline 状态机。改用文件存在性 + 内部字段作单一信号。
- **taxonomy 开放聚类不预设类型 / 只聚类不标签**（否决）：跨调用不一致，下游 idea-explorer / qing-novelist 难定向读（如 qing-novelist 只想读角色+主题类碎片填 L1）。轻量固定 7 类型 + other 平衡结构化与灵活性。
- **seed gate 🚫 硬阻断（类 handoff 检查）/ 无降级路径**（否决）：handoff 检查是 🚫 硬阻断（CLAUDE.md 规则 2），但 handoff 是 plan→generate 的契约边界（无 handoff 则 generate 无输入可读），seed 是上游素材理清（非契约边界）。改 🟡 软阻断 + 降级路径，与 C9 outline 实质填充检查同哲学——尊重网文边写边定，作者可确认放行（口述 premise 直写 Premise 段，下游读三字段无富材料）。降级路径下三字段 Premise 临时回任工作输入，与默认"三字段降为宪法蒸馏"形成有条件例外（在 Consequences 注明）。
- **完成判定纯作者判 / agent 自动判**（否决）：纯作者判可能结构化未完就收；agent 自动判剥夺作者控制。混合（agent 提议 + 作者确认）合项目既有 gate+confirm 模式。

## Consequences

- 改动面约 7 文件：新建 `xuanji/SKILL.md`（SKILL.md 自洽——taxonomy 表内嵌，无超长方法论需外推，不另建 `_reference/`）；改 `outline-tingle`、`idea-explorer`、`qing-novelist`、`adaptation-workflow` 四处 SKILL.md；改 `framework/templates/outline.md` Premise 段加指针；改 `CLAUDE.md`（规则 9 / 用户入口表 / 工作流图 / 产出物即状态表）；注册 `framework/_specs/interaction-spec.md` §2.2 产出物表。pre-flight-check 不动（seed 检查由 outline-tingle 自管，不进 C0-C11）。
- skill 数量 21 → 22。项目减层重构针对的是稿件体系（草稿层/原稿层）与设定读写，不针对 skill 数量；新增 peer 级通用工具与减层方向不冲突。
- CONTEXT.md 为本 ADR 首次建立——此前 repo 无 CONTEXT.md，本设计的领域语言（残留碎片 / seed / 收敛 / 核心种子 / 缺口 / 冲突 / 未决停车场 / 三字段蒸馏）是首批入档术语。
- adaptation-workflow 阶段 0.5 门禁逻辑变更：原"调 outline-tingle mode=adaptation"前需加 seed 检查。改编流原作画像已是结构化来源，但作者改编意图碎片（留/砍/注入）不在画像里，仍需 xuanji 收敛——两流对称 wiring 是设计意图。
- 三字段 Premise 语义降级：默认从"工作输入"降为"宪法蒸馏（人读 + state machine）"。**有条件例外**：seed gate 🟡 软阻断的降级路径下（作者确认放行、未跑 xuanji），三字段 Premise 临时回任工作输入——下游 idea-explorer / qing-novelist 读三字段而非 seed（无富材料）。默认路径下任何读三字段作工作输入的代码需改读 seed_path（审计时重点排查 idea-explorer / qing-novelist）。
- 验收用契约审计 + dry-run（构造 inspiration-log 样本手动跑 xuanji 产 seed，再跑下游读 seed），不跑端到端 grilling（依赖 LLM 产出、不可重复）。
