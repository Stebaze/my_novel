---
name: sensory-writer
description: 感官锚定写作工具——执行方法一（入身→外观→环境→内心独白）+方法二（入声→听到→写下→校准→不说）+方法三（脚本模式）的逐句写作步骤，单次一过式生成无AI指纹叙事文本；支持 single（整章单次）/ per-scene（逐场景 + 200字结构化摘要）双模式
---

# 感官锚定写作工具

> **edit-article 范式**：单场景散文 800-2000 字（per-scene 模式），每句走"核心方法"逐句协议。单次一过式——不检查、不修改、不重写。
> **双模式**：single（整章单次）/ per-scene（逐场景 + 200 字 JSON 摘要 → `_exchanges/scene-summaries.json`）。
> **方法三（AVG 脚本）** 详细协议外移到 `_reference/script-mode-protocol.md`，本 Skill 仅留执行入口与护栏。

## 强约束摘要（加载时从 ai-risk-mitigation.md 动态构建）

> **SSOT 契约**（2026-06-25 重构）：本节不再硬编码指纹枚举。`framework/guides/ai-risk-mitigation.md`「叙述者解码参考（诊断附录）」是**唯一真相源**——所有已注册指纹（含正字法级检测规则 + 修复策略）按 `{#fingerprint-N}` 锚点动态构建为本摘要。新指纹由 `fingerprint-discovery` 阶段 4 入库，**SKILL.md 无需修改**，下次加载自动反映。

### 加载协议

```
1. Read framework/guides/ai-risk-mitigation.md「叙述者解码参考（诊断附录）」段
2. 按 ### {编号}. {模式名} {#fingerprint-N} 锚点 parse 每条已注册指纹
3. 提取：模式名 / 表现 / 修复策略 → 构建首屏速查列表
4. 提取：「检测规则」段的正字法级规则 → 注入 Step 5 自查的禁式扫描
5. 加载失败 → 降级为下方「降级摘要」（不含已注册指纹枚举——形式 SSOT 受损但功能仍可用）
```

### 强约束规则（固定——不随指纹库变化）

1. **任何"展示角色没做什么"的句式都是违禁的**——默认状态不需要叙述；若确实要写"不思考"，用身体动作替代（"他的手指停在杯壁上，没动"）。
2. **本 Skill 所有护栏规则的唯一真相源是 `framework/guides/ai-risk-mitigation.md`**——执行期间如与该文档冲突，以该文档为准。
3. **抽象情感标签速查**——禁词：斟酌/意味深长/难以言喻/不容置疑/难以察觉/似乎/仿佛。完整清单见 `framework/templates/style-guide.md` 的"禁用词汇清单"情感标签分类。

### 降级摘要（加载 ai-risk-mitigation.md 失败时使用）

仅固定规则 1/2/3 + 速查 #1-5（`ai-risk-mitigation.md`「生成前速查」段的 5 条动笔前禁令）。**不覆盖已注册指纹的硬约束**——出现违禁模式需手动校验源文档。

## Identity

写作执行工具。应用 `framework/guides/ai-risk-mitigation.md` 方法一（感官锚定）+ 方法二（角色声音自然化）+ `framework/guides/audiobook-script-guide.md` 方法三（脚本模式），单次一过式生成叙事文本或广播剧脚本。**不做创意判断**——调用方提供"写什么"和"用什么声音写"，工具只负责"怎么写"。

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | `mo-writer`（参考示例 mode="single"）, `voice-sculptor`（声音实验）, `qing-novelist`（交谈长片段）, `generate-chapter`（Step 2 + Step 4 per-scene + Fix 循环单场景重写） |
| **Input** | `mode`（`"single"` / `"per-scene"`）, `scene_spec`, `character_voices`, `style_profile`, `output_format`（`"prose"` / `"script"`）, `prev_scene_summary`（per-scene 可选）, `opus_dna_contract: bool = false`（true 时加载 Step 2.5 5 层写作契约） |
| **Output** | single: 单一文本串；per-scene: `{prose, summary_200}`（散文 + 200 字 JSON 摘要） |
| **不变量** | 不检查、不修改、不重写——一过式生成 |

## Triggers

- 调用方 Skill 通过 `Skill` tool 传入参数

## Flow

### Step 1: Mode Selection

```
mode = "single"（默认）：
  → 一次生成整段文本（参考示例 / 整章 / 长示例片段）
  → 输出：单一文本串

mode = "per-scene"（generate-chapter 调用）：
  → 一次生成一个场景，附 200 字结构化摘要
  → scene_spec 字段：index/name/pov/location/time/events/dialogue_points/emotion_arc/next_scene_setup
  → 输出：{prose, summary_200}
  → 优势：单次 LLM 质量曲线约束更小 / per-scene 感官锚定更聚焦 / 200 字摘要供 Fix 循环精准定位
```

### Step 2: Core Method（方法一+二 + 内置护栏）

> 来自 `ai-risk-mitigation.md`（方法一+二），经硬化内置。

**逐句协议——叙事句**：

```
1. [入身] 站进 POV 角色的身体。此刻 ta 哪个部位有感觉？（指尖/喉咙/胸口/脊椎/肩膀/胃/眼皮/脚底）
   → 感觉具体是什么？（紧/松/热/冷/麻/空/重/轻/刺/颤/酸/涨）
   → 没有身体感觉就不下笔
2. [外观] 角色因身体感觉做了什么外部动作？
   → 写动作本身。不写"他生气了"——写"他把杯子搁回桌上，没松手"
3. [环境] 动作引发了什么环境反馈或他人反应？
   → 把内部状态钉在外部世界的因果链上
4. [需要时] 【】内心反应——不完整、不解释、像脱口而出
   → 正确：【三个不够。】 错误：【看来她的灵力量级比我高出一个阶位】
   → 不需要就跳过——沉默也是表达
```

**逐句协议——对话句**：

```
1. [入声] 脑中已有角色声音样本——句长/口癖/绝不会说的话/情绪温度
2. [听到] 脑中"听到"角色说下一句话——不是设计，是听到
3. [写下] 原样写下。不修整、不补全。句子可断裂
4. [校准] 遮掉角色名——可能是别人说的吗？是→回到步骤 2
   → 这是"最合理的回答"吗？是→更极端（更损/更嘴硬/更笨拙/更幼稚）
5. [不说] 不开口的时刻也是声音——沉默是表达
```

**步骤内置护栏**——执行期间从 `framework/guides/ai-risk-mitigation.md` 附录加载的强约束摘要（详见顶部「强约束摘要」段加载协议）：5 条带例句+替代策略的"生成前速查" + 7 模式带例句+违和+检测规则+修复策略。SSOT 契约——SKILL.md 不再硬编码指纹枚举，新指纹入库后自动反映。

### Step 2.5: opus-dna 5 层写作契约（仅 `opus_dna_contract=true` 激活）

> 5 层框架来自外部 opus-writing-dna（完整原文 `framework/guides/opus-writing-dna.md`）。此处为执行速查版——总长约 400 tokens。Standalone 调用（voice-sculptor / qing-novelist）默认不加载，避免 prompt 膨胀。

**感知层**（pre-writing，每场景动笔前必读）：
- **任务类型** = `scene_spec.task_type`（来自简报 §-1：convince/explain/resonate/decide-help/record）
- **读者具象** = `scene_spec.reader_persona`（来自简报 §-1）—— 心里必须有一个具体的人：他知道什么、情绪是什么、读完之后要做什么
- **声音人设** = `voice_persona_source`（来自简报 §-1 → `voice-bible.md`）

**结构层**（planning，铺场景骨架时用）：
- **开头类型** = `scene_spec.opening_type`（认知缺口 / 共鸣 / 结果 / 冲突）—— 开头唯一任务：让读者继续往下读
- **末拍** = `scene_spec.ending_type`（闭环 / 开放问题 / 静默 / 停在最有力）
- **段落间"所以呢"自检**——两段之间插入"所以/但是/这就引出一个问题"通顺吗？插不进去 = 转换失败
- **不对称分配**——关键场景占 50%+ 篇幅；其他场景支撑；缓冲场景少量。避免每个部分分配差不多字数

**语言层**（writing，每句执行）：
- **一句一事**——避免带 3 个从句的长句。复杂的事拆成 2-3 句短句
- **具体 > 抽象**——"显著提升效率" → "原来三小时，现在十五分钟"。每写一个抽象表述就问"能不能换成读者脑子里能出现画面的说法"
- **节奏**——长句后必有短句做"吐气"；重要的话单独成段
- **类比**——只在你熟且抓核心相似性时用。所有类比都有边界，不要过度延伸
- **不美化**——7 分的事说 7 分的话。产品不要都"强大"，方法不要都"高效"

**元认知层**（写完后，下一节拍前自检 5 项）：
- **删减测试**——这段删掉，文章是否受损？不受损 → 删
- **替换测试**——这段能用更短的方式说吗？能用 → 换
- **出声测试**——读出来像人在说话吗？像念稿子 → 改
- **So-what 测试**——读者看完会想"所以呢"吗？会 → 给信息或行动指引
- **AI 味检测**——委托给 chapter-review + ping-critic（fingerprint 区已覆盖）

**高级能力**（rule-breaking，**显式**而非意外）：
- `scene_spec.voice_flags.rule_break_choice` 不为空时主动打破对应规则：
  - `长句沉浸` → 故事高潮/情绪蔓延/连锁反应时使用，一口气读完的势不可挡
  - `抽象收束` → 读者已充分理解具体内容，需要上位概念"收住"细节时
  - `对称仪式` → 制造仪式感或对比力量时
  - `不克制情感` → 情感是核心任务时（书信/回忆录/告别）——"多余的话"本身就是载体
- `safety_valve` 必须填写——打破后用什么手段"吐气"（例：长句结尾一个极短句；抽象收束前先给 3 个具体细节）

> 打破规则的前提是你知道自己在打破什么、为什么要打破、打破之后的效果是什么。不知道为什么打破的，就别打破。

### Step 3: per-scene 协议（仅 mode="per-scene" 激活）

> **不破坏 single 模式**：以下协议仅在 per-scene 时叠加。

**逐场景协议**：

```
0. [场景锚定] 地点+时间+POV → 场景名 → 节拍数（800-2000 字散文 / 1-3 段对话脚本）
   → prev_scene_summary 提供 → 读 ending_state + next_link → 在脑中承接

1. [拆节拍] events 拆成 3-6 个节拍
   → 节拍 1：开场感官/身体定位（POV 入身）
   → 节拍 2-N：events 逐项落地
   → 末节拍：未结束的场景——停在互动中途或情绪高点，不收束

2. [逐节拍写作] 每节拍执行 Step 2 逐句协议

3. [末节拍护栏]
   → 不写场景总结/升华句
   → 不在末尾加悬念钩子（除非 next_scene_setup 明确要求）
   → 不收束到 POV「内心结论」——停在动作或环境反馈上
   → 末尾句应是下场景可无缝承接的状态

4. [产出 prose] 完整场景散文（无场景头/场景标记——generate-chapter Step 2c 拼装时统一加）
```

**200 字结构化摘要**（per-scene 必出）：

> 完整 schema + 字段填写规则 + 下游消费方式见 `_reference/scene-summary-protocol.md`（200 字序列化约束 / 字段语义 / chapter-review ai-content 5 项校验数据映射）

必出字段：`scene_index / scene_name / pov / core_event / key_actions / key_dialogue / pov_state_change / ending_state / next_link / foreshadow_touched`。

**per-scene 自查**（叠加在 Step 5 之上）：

```
5. [断裂] 末节拍是否停在 next_scene_setup 期望的状态？→ 否 → 微调末句
6. [摘要] summary_200 字段齐全？ending_state 与下场景 first action 衔接？→ 断裂 → 修正
```

**Fix 循环单场景重写**（generate-chapter Step 4 调用）：

```
追加输入：prev_prose + fix_issues（评审问题列表，精确到句子）
→ 在脑中先扫一遍 prev_prose 的"为什么不行"——OOC / 节拍错位 / AI 指纹 / 对白不像
→ 按 fix_issues 逐项修，不动未指出的部分
→ 产出新 prose + 新 summary_200
→ 不重写整章——只重写单场景
```

### Step 4: 方法三 AVG 脚本模式（仅 output_format="script" 激活）

> 详细协议在 `_reference/script-mode-protocol.md`——本 Step 仅作执行入口和护栏速查。
> 格式规范：`framework/guides/avg-script-format.md` + `framework/guides/audiobook-script-guide.md`。

**执行步骤**（详见 `_reference/script-mode-protocol.md` 一、逐场景协议）：

```
0. [场景锚定] 写【场景：{地点}·{时间}】
1. [视听环境] BGM 情绪 + 背景 + 旁白建场
2. [角色登场] 首次出场 → 【立绘：角色 表情 位置 滑入】；已在场景中 → 跳过
3. 逐句生成——a. 台词 [表情] + ⏱ N.Ns / b. 演出注 / c. 表情变 / d. 音效 / e. 旁白 / f. CG / g. 停顿 / h. 检定
4. [角色退场] → 【立绘：角色 淡出】
5. [章末汇总] 配音时长汇总表 + 背景生图提示词索引 + CG 生图提示词索引
```

**AVG 脚本护栏**（详见 `_reference/script-mode-protocol.md` 二）：

- 角色名 [表情] 直接前缀——不用散文对话标签；每句对白必带 `[表情]` + `⏱ N.Ns`
- 情绪变化 = 【立绘：新表情】+ 下句对白 [新表情] 同步
- 演出注写"看得见的"——肢体动作/微表情/环境互动；不解释动机
- 旁白内心独白可保留（AVG 旁白承担内心叙事）
- CG 提示词仅写角色姓名——样貌从立绘规格卡获取
- 背景提示词含：场景描述+光影+关键视觉元素+构图视角
- 项目类型决定块类型：跑团 Replay VN 不用选择块/跳转/flag；标准 AVG 不用检定块

### Step 5: 生成后轻量自查（一过式）

返回前静默执行 4 项检查。发现问题静默修正后返回，不报告修正过程：

```
1. [POV] 有无泄露 POV 不可能知道的信息？→ 替换为 POV 可感知的外部观察
2. [逻辑] 本段内部有无前后矛盾？角色情感/认知有无突兀跳变？→ 加入过渡或修正
3. [尾部] 结尾是否擅自结束场景或引入未铺垫悬念？→ 停在互动中途，去掉总结/升华/悬念句
4. [禁词] 读 style-guide.md「禁用词汇清单」→ 扫一遍生成文本 → 命中按"替代策略"列替换
   → style-guide 不存在则跳过
5. [指纹] 按强约束摘要加载的「正字法级检测规则」扫一遍生成文本 → 命中按对应指纹的「修复策略」改写
   → 加载失败时跳过——已在顶部「降级摘要」标注
```

### Step 6: 风格适配

生成时匹配 `style_profile`：句长分布 / 段落密度（每段 1-3 句，段落间空行）/ 感官分布（视觉~55% + 内心独白~25% + 听觉~10% + 触觉~5%）/ 情感表达层级（身体反应→内心独白→陈述→隐喻）/ 对话标签（动作~35% + 无~20% + 说道变体~25% + 【】~15% + 声音响起~5%）/ 【】内部对话使用。

---

## Output

- **single 模式**：返回单一文本串（prose / script）——一过式
- **per-scene 模式**：返回 `{prose, summary_200}` 两段。`summary_200` JSON 块置于 prose 之后单独代码块包裹
- **per-scene 路径**：调用方负责将 summary_200 写入 `_exchanges/scene-summaries.json`，prose 拼装到 `chapters/chapter-{N}.md`

## Completion Criterion

- ✅ Checkable：返回 `{output_text, mode, scenes_count（per-scene）, scene_summaries_path（per-scene 写盘后）, chapter_assembled_path}`
- ✅ Exhaustive：Step 1-6 全部执行；per-scene 模式 summary_200 字段齐全（缺字段视为不完整）
- 🚫 Stop：一过式生成后不修改不重写——返回结果到调用方

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `_reference/script-mode-protocol.md` | Step 4（方法三 AVG 脚本） | 🚫 硬阻断——方法三协议外移后必须能读取 |
| `_reference/scene-summary-protocol.md` | Step 3（per-scene 200 字摘要） | 🚫 硬阻断——per-scene 必出 schema 外移后必须能读取 |
| `framework/guides/ai-risk-mitigation.md` | 方法一+二参考 | ⚠️ 使用内嵌步骤（标注"方法指南缺失"） |
| `framework/guides/avg-script-format.md` | 方法三 AVG 规范 | ⚠️ 使用内嵌块类型定义 |
| `framework/guides/audiobook-script-guide.md` | 方法三写作流程 | ⚠️ 使用内嵌协议 |
| `framework/templates/_script-format-spec.md` | 方法三格式速查 | ⚠️ 仅使用内嵌块类型定义 |
| `framework/templates/style-guide.md` | Step 5 自查——禁词表 | ⚠️ 跳过第 4 项禁词检查 |
| `framework/templates/characters/_sprite-spec.md` | 方法三立绘规格 | ⚠️ 立绘表情仅使用通用表情集 |
| `prev_scene_summary` | per-scene 模式（非首场景） | ⚠️ 跨场景连续性降级为"凭印象衔接"——可能产生轻微 drift |
| 调用方传入的 `events` / `dialogue_points` / `emotion_arc` | per-scene 模式 | 🚫 硬阻断——简报 §3 拆解缺失则 per-scene 无内容可写 |
