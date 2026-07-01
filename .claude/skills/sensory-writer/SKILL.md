---
name: sensory-writer
description: 写作执行工具——4 Step 轻量流程（场景锚定→逐节拍→末拍护栏→读出来），开放风格兼容，腔调交 author_profile（指定作家时）或 5 维 风格档案（不指定时）运行时决定；opus-dna 5 层默认加载并融合进 4 Step（不再单独 Step 2.5）；生成端自查只保留"读出来·全章"（其余交评审端）。双模式：single（整章单次）/ per-scene（逐场景 + 200 字 JSON 摘要）。
execution_model: "协议即 skill"  # 2026-07-01 修复——明确本 skill 是协议文档
---

# 写作执行工具 v3.0（轻量版）

> **execution_model = "协议即 skill"**（2026-07-01 修复）
>
> 本 skill 在 Claude Code 平台上的执行方式与其他 skill（pre-flight-check / settings-manager / chapter-review 等）不同：
>
> | 维度 | pre-flight-check / settings-manager / chapter-review | sensory-writer |
> |------|---------------------------------------------------|----------------|
> | 调用结果 | Skill tool 返回 SKILL.md 描述 | Skill tool 返回 SKILL.md 描述 |
> | 实际执行 | **agent 读取 SKILL.md 后手动执行协议** | **agent 读取 SKILL.md 后手动执行协议** |
> | 脚本化 | 部分有 scripts/（2026-07-01 修复中）| 仅有协议，无脚本（sensory-writer 是"创作"工具，难脚本化）|
> | agent 角色 | 门禁判断 / 设定管理 / 评审 | **创作——agent 真正生成 prose** |
>
> **结论**：sensory-writer 调用时，agent 必须自己按 4 Step 协议生成 prose——不是调 LLM 生成（虽然本 skill 的输出在概念上是 LLM 的工作）。
> 脚本化路径见 `scripts/sensory-writer-protocol.sh`（提供可执行参考实现，但 agent 仍可选择"协议推理"路径）。

> **4 Step 轻量流程**（2026-06-30 重构）：
> - Step 1：场景锚定（per-scene）— 读 POV + 设计流程阶段 1-2 → 决定叙述者+节拍
> - Step 2：逐节拍写作（轻量）— 读 设计流程阶段 3 → 改写场景内组织
> - Step 3：末拍护栏（per-scene）— 不写总结/升华；停在动作/环境反馈
> - Step 4：读出来·全章 — 唯一保留的生成端自查；其他交评审端
>
> **opus-dna 融合**：5 层（感知/结构/语言/元认知/高级）默认加载并融合进 4 Step——不再单独 Step 2.5。
> **author_profile 集成**：指定作家时加载 `profiles/authors/{name}.md` 改写下方所有 Step 协议；不指定时回退 3 维 风格档案（基底+主题+风格 fallback）。
> **5 步协议砍**：入身/外观/环境/内心/用词具体——已删（破坏流畅+前后关联）。
> **6 项自查砍**：POV/逻辑/尾部/禁词/指纹/语法——只留"读出来"；其他交 chapter-review。

## 强约束摘要（固定——不随指纹库变化）

1. **任何"展示角色没做什么"的句式都是违禁的**——默认状态不需要叙述；若确实要写"不思考"，用身体动作替代（"他的手指停在杯壁上，没动"）。
2. **本 Skill 所有护栏规则的唯一真相源是 `framework/guides/ai-writing-dna.md`**——执行期间如与该文档冲突，以该文档为准。**不要读 `ai-fingerprint-checklist.md`**——该文件是评审端核对清单，生成端写时按 `ai-writing-dna.md` 第 3.6 节的 ❌ 范例规避（2026-07-01 重构）。
3. **抽象情感标签速查**——禁词：斟酌/意味深长/难以言喻/不容置疑/难以察觉/似乎/仿佛。
4. **指纹意识分工（生成端最小集原则）**——下笔时识别并规避 3 类高频全场景问题（语法/分段/句式机关枪）。**词汇指纹**（慢慢/忽然/原来 等高频词累计）不在生成端判断——单句层无法知章级累计，交 generate-chapter 2b-gate 追踪器 + 章末 chapter-review 统一处理。**其余场景特异指纹**生成端不加载不判断，交评审端兜底。
5. **声纹承载原则**——角色声纹特征靠「句式/词汇/口头禅/语法结构」承载，**不靠「段数/独立段」承载**。当声纹要求 1 句 1 段 vs 读感要求合并时，**默认选合并 + 声纹靠句式保留**。1 句独立段的合法触发：新场景/新时间/新 POV/动作结果/重要情绪爆点。

## Identity

写作执行工具。单次一过式生成叙事文本。**不做创意判断**——调用方提供"写什么"和"用什么声音写"，工具只负责"怎么写"。**开放风格兼容**：协议只保质量底线（强约束 5 条），不绑定任何作者腔调——腔调交 author_profile 或 5 维 风格档案运行时决定。

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | `mo-writer`（参考示例 mode="single"）, `voice-sculptor`（声音实验）, `qing-novelist`（交谈长片段）, `generate-chapter`（Step 2 + Step 4 per-scene + Fix 循环单场景重写） |
| **Input** | `mode`（`"single"` / `"per-scene"`）, `scene_spec`, `character_voices`, `style_profile` (3 维 dict：`{type, themes[], variant}`), `author_profile`（可选，作家名如"葵关南"/"远瞳"）, `opus_dna_contract: bool = false`（true 时加载高级能力 rule-breaking），`prev_scene_summary`（per-scene 可选） |
| **Output** | single: 单一文本串；per-scene: `{prose, summary_200}`（散文 + 200 字 JSON 摘要） |
| **不变量** | 不检查、不修改、不重写——一过式生成（除 Step 4"读出来·全章"轻量自检） |

## Step 0: 加载协议（style_profile + author_profile + opus-dna）

### 0.1 加载优先级

```
1. author_profile（指定作家时）→ 优先加载 profiles/authors/{name}.md
   - 含 POV 4 维（叙述者/温度/对话密度/内心通道/段长句长）+ 设计流程 3 阶段（大纲→事件/事件→场景/场景内组织）
   - 改写下方 Step 1-4 所有协议（叙述者声音/节拍切分/对话写/动作写/内心写）
   - 注：profiles/authors/ 在 .gitignore 中（版权隔离），指定作家时需用户本地有该档案
   - 项目默认（作家=""）不加载此层

2. style_profile（3 维 fallback——不指定作者时）→ 加载 framework/templates/_style-bases/ + _themes/ + _styles/ fallback
   - 基底（japanese-light-novel-base / chinese-webnovel-base）→ 6 坐标轴
   - 主题叠加（theme-*）→ 5 字段
   - 风格 fallback（kuiguannan/amamorin/shiniki/yuantong/fengyue/buluofeng-style）→ 叙述态度+域词+桥段
   - **项目默认 = chinese-webnovel-base + romance + amamorin-style-fallback**
     —— 详细 spec：framework/templates/_defaults/default-style.md（git tracked，fresh clone 即用）

3. opus-dna 5 层（默认加载——不再 opt-in）→ 融合进 Step 1-4
   - 感知层 → Step 1 场景锚定
   - 结构层 → Step 1 场景锚定
   - 语言层 → Step 2 逐节拍写作
   - 元认知层 → Step 4 读出来·全章
   - 高级能力 rule-breaking → opt-in（opus_dna_contract=true 时启用）
```

**项目默认（作家=""）加载链**（fresh clone 即可用，不需要 profiles/authors/）：

```
novel/project-config.md
  ├ 作家 = ""                            → 不走 profiles/authors/
  ├ 主风格档案 = "chinese-webnovel-base"  → framework/templates/_style-bases/chinese-webnovel-base.md (6 坐标轴)
  ├ 主题 = ["romance"]                    → framework/templates/_themes/theme-romance.md (5 字段)
  └ 风格 = "amamorin-style-fallback"     → framework/templates/_styles/amamorin-style.md (3 块 fallback)
```

### 0.2 加载失败降级

```
- author_profile 不存在 → 降级到 style_profile 5 维 fallback（不阻断，标注降级）
  - 注：项目默认（作家=""）直接走此路径，不算"降级"
- style_profile 加载失败 → 仅保强约束 5 条（标注"风格档案缺失，已降级为通用质量底线"）
- opus-dna 加载失败 → 跳过元认知层 Step 4 自检（标注"opus-dna 未加载"）
```

## Step 1: 场景锚定（per-scene）

> **融合 opus-dna 感知层 + 结构层**——读 POV + 设计流程阶段 1-2 → 决定叙述者+节拍
> **v3.0 5 维扩展**：场景锚定除地点+时间+POV 外，还需读 author_profile（或 style_profile）加载主题领域装置（romance → 物理小物 / mystery → 委托人机制 / scifi → 硬规则设定 / system → 系统模拟等）——决定场景的"题材装置"。

**逐场景协议**：

```
0. [场景锚定] 地点+时间+POV → 场景名 → 节拍数（800-2000 字散文）
   → prev_scene_summary 提供 → 读 ending_state + next_link → 在脑中承接
   → 简报 §3「质感钩子」读 1 遍——本场景最该"读出来"读 1 遍的位置是哪一句？记下

0.5. [动笔前通顺预读] 30 秒扫读 5 维度（不写正文，只过脑）：
   1. [分段预判] 本场景打算分几段？每段结尾是完整语义单元吗？
      → 若有"半句话/未完成动作"打算独立成段 → 合并到下一段
      [1 句独立段·判断标准] 1 句独立段是工具不是默认,先问:
        - 新场景/新时间/新 POV 切换? → 1 段 OK
        - 上一段的动作结果/重要反转? → 1 段 OK（节奏停顿）
        - 上一段的展开/细化/承接/同主题重复? → ❌ 合并
        - 同一动作链的中间步骤? → ❌ 合并
      默认: 2-3 句段。1 句独立段需明确理由。
   2. [用词预判] 关键动作打算用什么动词？能不能更具体？
   3. [衔接预判] 上一场景最后一句是什么？本场景第一句承接什么？
      → 若是"另起炉灶"无任何呼应 → 加 1 句环境/动作/物件桥
   4. [语法预判] 是否有把握避开：成分残缺/搭配不当/语序错乱/虚词误用/标点错配
      → 任意项无把握 → 在该处动笔时多看 1 遍
   5. [段间合并预判] 预读每个节拍草拟的段切分,标出"该合并"的段对:
      → 同动作链（触发→动作→反应）→ 合并
      → 同思维链（想→再想→结论）→ 合并
      → 同主题重复（"X不...X不...X——"/"想...想...想..."）→ 合并
      → 把这些标出来,写作时主动连气,不独立成段

1. [拆节拍] events 拆成 3-6 个节拍
   → 节拍 1：开场感官/身体定位（POV 入身）
   → 节拍 2-N：events 逐项落地
   → 末节拍：未结束的场景——停在互动中途或情绪高点，不收束

2. [结构层] 读 opus-dna 结构层
   → 开头类型 = scene_spec.opening_type（认知缺口/共鸣/结果/冲突）—— 开头唯一任务：让读者继续往下读
   → 末拍 = scene_spec.ending_type（闭环/开放问题/静默/停在最有力）
   → 段落间"所以呢"自检——两段之间插入"所以/但是/这就引出一个问题"通顺吗？插不进去 = 转换失败
   → 不对称分配——关键场景给足篇幅，支撑/缓冲场景明显更短

3. [感知层] 读 opus-dna 感知层
   → 任务类型 = scene_spec.task_type（来自简报 §-1：convince/explain/resonate/decide-help/record）
   → 读者具象 = scene_spec.reader_persona（来自简报 §-1）—— 心里必须有一个具体的人：他知道什么、情绪是什么、读完之后要做什么
   → 声音人设 = voice_persona_source（来自简报 §-1 → voice-bible.md）

4. [产出 scene_spec] 完整场景规范（无场景头/场景标记——generate-chapter Step 2c 拼装时统一加）
```

## Step 2: 逐节拍写作（轻量）

> **融合 opus-dna 语言层**——读 设计流程阶段 3 → 改写场景内组织
> **v3.0 砍重**：5 步逐句协议（入身/外观/环境/内心/用词具体）已删——作者特定协议由 author_profile 设计流程阶段 3 提供；风格 fallback 由 style_profile 提供。

**每节拍执行**：

```
1. [入节拍] 读 author_profile（或 style_profile）提供的"对话写/动作写/内心写"协议
   → 不强制 5 步顺序——按作者风格/场景需要自由组合
   → 葵关南=5 步听到-写下-校准（对话）+ 拒绝"他生气了"（动作）+ 自由间接引语（内心）
   → 远瞳=多 POV 拼图（对话）+ 大场面奇观（动作）+ 多层信息差（内心）
   → 不落风=主角吐槽+系统冷嘲+角色互动 3 层（对话）+ 系统面板作动作锚点 + 长心理+超短段
   → fallback（无作者时）→ 通用质量底线（强约束 5 条）

2. [写] 落笔写一节拍
   → 自由间接引语为默认内心通道（无"他想/觉得"标签）
   → 第三人称带 POV 角色腔调（角色会脱口而出的判断/比喻/反讽）
   → 短促独立判断可用【】（如【三个不够。】【读得透。但——】）
   → 物理道具必填（每场景配一个物理小物作潜台词载体）
   → 段长以 2-3 句为主；1 句独立段需明确理由

3. [读语言层] 读 opus-dna 语言层
   → 一句一事——避免带 3 个从句的长句
   → 具体 > 抽象——"显著提升效率" → "原来三小时，现在十五分钟"
   → 节奏——长句后必有短句做"吐气"
   → 类比——只在你熟且抓核心相似性时用
   → 不美化——7 分的事说 7 分的话
```

## Step 3: 末拍护栏（per-scene）

```
1. [末拍检查] 末节拍是否停在 next_scene_setup 期望的状态？
   → 否 → 微调末句
2. [场景末节拍原则] 不写场景总结/升华句
   → 不在末尾加悬念钩子（除非 next_scene_setup 明确要求）
   → 不收束到 POV「内心结论」——停在动作或环境反馈
3. [产出 prose] 完整场景散文（无场景头/场景标记——generate-chapter Step 2c 拼装时统一加）
4. [摘要] summary_200 字段齐全（per-scene 必出）
   → 必出字段：scene_index / scene_name / pov / core_event / key_actions / key_dialogue / pov_state_change / ending_state / next_link / foreshadow_touched
```

**Fix 循环单场景重写**（generate-chapter Step 4 调用）：

```
追加输入：prev_prose + fix_issues（评审问题列表，精确到句子）
→ 在脑中先扫一遍 prev_prose 的"为什么不行"——OOC / 节拍错位 / AI 指纹 / 对白不像
→ 按 fix_issues 逐项修，不动未指出的部分
→ 产出新 prose + 新 summary_200
→ 不重写整章——只重写单场景
```

## Step 4: 读出来·全章（唯一保留的生成端自查）

> **融合 opus-dna 元认知层**——5 项出声测试（删减/替换/出声/So-what/AI 味）中只保留"出声"和"删减"两项；其他 3 项交评审端。
> **v3.0 砍重**：6 项自查（POV/逻辑/尾部/禁词/指纹/语法）已删——其他 5 项交评审端。

```
1. [读出来·全章] 在脑里（或出声）从头读一遍——模拟读者体验，而非列项检查：
   → 读到哪里"卡一下"？记下位置，回头改
   → "卡一下"包括：回看上句（衔接断裂）/ 跳过某词（用词不准）/
     觉得"为什么这么写"（叙述者闯入）/ 觉得"太长"（节奏过载）/
     觉得"太短"（信息过载）
2. [读出来·段间衔接] 重读每段最后一句 + 下段第一句：
   → 若读者要回看 → 两条路径二选一:
     · 该断: 加 1 句环境/动作桥（保留分段,仅补桥）
     · 该连: 把两段合并为一段（用逗号/破折号连气, 牺牲分段换紧凑）
   → 默认选"该连"——除非是真正新场景/新 POV 切换
3. [读出来·声音] 重读所有对话：
   → 若某句话遮掉角色名后可由别人说 → 重写
   → 若角色用了"不属于 ta 的梗/口头禅" → 删
4. [删减测试] 这段删掉，文章是否受损？不受损 → 删
5. [元认知层·读 opus-dna] 5 项出声测试中保留 2 项（出声+删减）；其他 3 项（替换/So-what/AI 味）交评审端
```

## opus-dna 高级能力（rule-breaking——**显式 opt-in**）

> 默认不启用。调用方设 `opus_dna_contract=true` 时加载。

```
- `scene_spec.voice_flags.rule_break_choice` 不为空时主动打破对应规则：
  - `长句沉浸` → 故事高潮/情绪蔓延/连锁反应时使用，一口气读完的势不可挡
  - `抽象收束` → 读者已充分理解具体内容，需要上位概念"收住"细节时
  - `对称仪式` → 制造仪式感或对比力量时
  - `不克制情感` → 情感是核心任务时（书信/回忆录/告别）——"多余的话"本身就是载体
- `safety_valve` 必须填写——打破后用什么手段"吐气"（例：长句结尾一个极短句；抽象收束前先给 3 个具体细节）
- 打破规则的前提是你知道自己在打破什么、为什么要打破、打破之后的效果是什么。不知道为什么打破的，就别打破。
```

## Output

- **single 模式**：返回单一文本串——一过式
- **per-scene 模式**：返回 `{prose, summary_200}` 两段。`summary_200` JSON 块置于 prose 之后单独代码块包裹
- **per-scene 路径**：调用方负责将 summary_200 写入 `_exchanges/scene-summaries.json`，prose 拼装到 `chapters/chapter-{N}.md`

## Completion Criterion

- ✅ Checkable：返回 `{output_text, mode, scenes_count（per-scene）, scene_summaries_path（per-scene 写盘后）, chapter_assembled_path}`
- ✅ Exhaustive：Step 0-4 全部执行；per-scene 模式 summary_200 字段齐全（缺字段视为不完整）
- 🚫 Stop：一过式生成后不修改不重写——返回结果到调用方（除 Step 4"读出来·全章"轻量自检后可能微调）

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `framework/guides/ai-writing-dna.md` | 强约束摘要 | ⚠️ 使用内嵌 5 层 opus-dna + 3.6 指纹反例（标注"方法指南缺失"） |
| `framework/templates/style-guide.md` | 禁词表参考 | ⚠️ 跳过禁词检查（强约束 5 条有"抽象情感标签速查"） |
| `profiles/authors/{name}.md`（指定作者时）| Step 0.1 author_profile 加载 | ⚠️ 不存在时降级到 style_profile（不阻断）；项目默认（作家=""）不加载此层 |
| `framework/templates/_style-bases/ + _themes/ + _styles/` | Step 0.1 style_profile 加载 | ⚠️ 加载失败时仅保强约束 5 条（标注降级） |
| `framework/guides/opus-writing-dna.md` | opus-dna 5 层加载 | ⚠️ 加载失败时跳过 Step 4 元认知层自检（标注"opus-dna 未加载"） |
| `_reference/scene-summary-protocol.md` | Step 3（per-scene 200 字摘要） | 🚫 硬阻断——per-scene 必出 schema 外移后必须能读取 |
| `prev_scene_summary` | per-scene 模式（非首场景） | ⚠️ 跨场景连续性降级为"凭印象衔接"——可能产生轻微 drift |
| 调用方传入的 `events` / `dialogue_points` / `emotion_arc` | per-scene 模式 | 🚫 硬阻断——简报 §3 拆解缺失则 per-scene 无内容可写 |

## 变更记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-06-30 | 初版（方法一+二 + 5 步逐句协议 + 6 项自查）|
| v2.0.0 | 2026-06-30 | 5 维扩展（style_profile type/themes/variant/subvariant/specialization 5 维正交）|
| v2.0.1 | 2026-06-30 | 声纹承载原则（句式层面而非分段层面）|
| v3.0 | 2026-06-30 | **轻量化重构**——砍 5 步协议 + 6 项自查（只留"读出来"）+ opus-dna 5 层融合进 4 Step（不再单独 Step 2.5）+ author_profile 集成（指定作家时改写协议）|
| v3.0.1 | 2026-07-01 | **项目默认风格固化**——`framework/templates/_defaults/default-style.md` 声明 chinese-webnovel-base + romance + amamorin-style-fallback = 项目默认；Step 0.1/0.2/Dependencies/关联文件 四处加 default 路径说明（fresh clone 即可用，profiles/authors/ 可空）|

## 关联文件

- 强约束真相源：`framework/guides/ai-writing-dna.md`
- opus-dna 速查：`framework/guides/opus-writing-dna.md`
- 200 字摘要协议：`_reference/scene-summary-protocol.md`
- 禁词表：`framework/templates/style-guide.md`
- 3 维 风格档案（基底+主题+风格 fallback）：`framework/templates/_style-bases/ + _themes/ + _styles/`
- **项目默认风格 spec**：`framework/templates/_defaults/default-style.md`（git tracked，fresh clone 即用——`chinese-webnovel-base + romance + amamorin-style-fallback`）
- 作者档案（profiles）：`profiles/authors/*.md`（`.gitignore` 中，git ignored；可选 enrich——`作家` 字段指定时加载）
- 下游消费：generate-chapter（Step 2 + Step 4 per-scene + Fix 循环）
