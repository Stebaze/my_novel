# outline-tingle 书级设定派发到设定文件

outline-tingle Session 2 产出的角色弧光/关系/规则/卷篇章结构原本只落入 `outline.md`，下游 plan-chapter 阶段 1 设定快照读 `characters/`/`character-arcs.md`/`world/`/`thread-map.md` 时为空。决定在 Session 2 `init-draft` 后新增 2.8.5 步骤，把 `outline.md` L1-L3 已定型字段按映射表派发到草稿目录对应设定文件的对应段（骨架占位，未定型段留 `（待定）`），由 outline-tingle 自己执行——不调 file-manager / settings-manager，不进 `_changes.md` 时间线。派发前清空目标段保证幂等，缺失文件从模板补齐 + 🟡 软阻断降级（不阻塞大纲完成）。`outline.md` frontmatter 加 `book_settings_dispatched` 字段 + pre-flight-check 新增 C10 ⚠️ 提醒。adaptation mode 的 B9 三态标注不派发（留 outline 宪法层），original/adaptation 派发逻辑统一。

## Considered Options

- **settings-manager 注册引入章节=0**（否决）：read-settings 合并逻辑是"读文件 + `_changes.md` 增量层"，文件存在即被读到，`_changes.md` 是变更增量而非设定来源。书级设定是宪法、不属"引入章节 ≤ N"过滤语义，进时间线是概念错配。
- **委托 file-manager 新增 dispatch operation**（否决）：file-manager 职责是补齐（模板拷贝/目录建立），内容填充会漂移其语义；Q3 映射表（哪个 B 维度去哪段）属 outline-tingle 的 Flow 知识，外推到 file-manager 只是换地方。
- **B9 三态派发到设定文件**（否决）：B9 是 outline 宪法层元信息，设定文件是执行层实体档案，层级不同；chapter-review 评审对齐度时本就读 outline.md，三态在那里是单一真相源。
- **靠文件内容非空判定派发状态**（否决）：状态判定逻辑分散到下游每个读者，且无法区分"该跑 Session 2"vs"派发失败软阻断"。改用 `book_settings_dispatched` frontmatter 字段作单一真相源。

## Consequences

- 下游 plan-chapter 阶段 1 设定快照能读到非空骨架，但仍需章节级 Skill（qing-novelist 章节模式 / voice-sculptor / sensory-writer）逐步填实"性格剖面/心理动力/语言风格/能力限制"等段——这是设计意图，书级只定宪法。
- `book_settings_dispatched` 是 outline.md frontmatter 第 8 个状态字段，pre-flight-check C10 是新增第 10 项检测（C0-C9 既有）。ask-yiyi 会话初始化的工件扫描需识别该字段（CLAUDE.md 规则 8 已同步）。
- 派发是 outline-tingle 内部步骤，不新增 Skill 间调用——interaction-spec（Skill 契约层）不动。
- 验收用契约审计 + dry-run（构造已填实 outline.md 样本手动执行派发），不跑端到端 grilling（依赖 LLM 产出、不可重复）。
