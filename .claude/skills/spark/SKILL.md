---
name: spark
description: 碎片想法捕获——capture(单条当场)/import(批量离线) 两 mode，一句话落盘 novel/inspiration-log.md，零交互
---

# 火花 — 碎片想法捕获

> **范式**：append-only 单行 bullet 流——作者想到什么记什么，零结构负担。
> **横切工具**：不进任何编排层（不属于 plan/generate/review/publish 任何一环，也不进 adaptation-workflow），作者任何时候直接 `/spark` 调用。
> **座右铭**：宝库不是欠债——积累的资产，不是待办清单压力源。

## Identity

「火花」(Spark) 碎片想法捕获入口。职责是把作者冒出来的碎片想法低门槛落盘到 `novel/inspiration-log.md`，让它不被遗忘、能在 ask-yiyi 启动时浮回来。产出是"已记录"这件事本身，不是想法的质量评估、不是章节落地。

## Contract

| Aspect | Detail |
|--------|--------|
| **Input `mode`** | `capture`（单条当场，零交互）\| `import`（批量离线，交互收集）。`/spark <一句话>` → capture；`/spark import` 或 `/spark` 无参数 → import |
| **Called by** | 用户直接调用（qing-novelist / plan-chapter / idea-explorer 在交谈中提示作者触发，但**不直接 Skill 调用 spark**——由作者自己执行 `/spark`） |
| **Calls** | `file-manager` Skill（`ensure-file` operation——首次写入前检查 `novel/inspiration-log.md` 缺失时补齐） |
| **Produces** | `novel/inspiration-log.md` 追加 N 条 bullet；返回 `{appended: bool, count: N, path: "novel/inspiration-log.md", preview: "最近 3 条"}` |
| **Consumes** | 无（append-only，不读已有内容） |

## Triggers

- `/spark <一句话>` —— capture 单条当场
- `/spark import` —— 批量录入（粘贴多行）
- `/spark` —— 无参数，默认进 import 模式
- "记一下……" / "我有个想法……" / "把这个灵感记下来" —— 作者口头触发，spark 进 capture 模式

## Execution

### 前置：ensure 文件存在

1. 检查 `novel/inspiration-log.md` 存在性
2. 不存在 → 调 `Skill("file-manager", operation="ensure-file", file="inspiration-log.md", target="novel/")` 补齐
3. file-manager 不可用 → 🚫 硬阻断——"file-manager 不可用，无法 ensure inspiration-log.md，请检查 Skill 安装"
4. 文件存在或已补齐 → 进入 mode 分支

### capture mode

**触发**：`/spark <一句话>`（参数非空且非 `import`）

**执行**（零交互——不追问、不确认、不评估）：

1. 取当前时间戳 `YYYY-MM-DD HH:MM`
2. 构造 bullet：`- [{时间戳}] {内容}`（保留作者文本里的 `#标签`，不打标签就裸记）
3. append 到 `novel/inspiration-log.md` 末尾（`## 灵感流` 段之后）
4. 返回 `{appended: true, count: 1, path: "novel/inspiration-log.md", preview: "最近 3 条"}`

**格式约定**：单行 bullet，时间戳精确到分钟，内容原样保留（不纠错、不加工）。

### import mode

**触发**：`/spark import` 或 `/spark` 无参数

**执行**（交互收集——批量录入）：

1. 提示作者："把要记的想法贴出来，一行一条或多行都行。说『没了』结束。"
2. 作者粘贴文本 → 切分规则：
   - 按分隔符切分：`-` / `*` / `1.` 开头的行各为一条；无分隔符的连续行由 LLM 判断"独立想法 vs 跨行想法"
   - 空行忽略
3. 每条加时间戳 `YYYY-MM-DD HH:MM`，构造 bullet `- [{时间戳}] {内容}`（保留作者文本里的 `#标签`）
4. 追问："还有吗？"
5. 作者说"没了" / "结束" / "就这些" → flush 所有 bullet 一次性 append 到 `novel/inspiration-log.md`
6. 返回 `{appended: true, count: N, path: "novel/inspiration-log.md", preview: "最近 3 条"}`

**时间戳**：用 import 时刻（不是想法原始产生时刻——那个作者也记不清），每条独立加。

## Out of Scope

1. **不做结构化发散**——作者没想法时要"帮我想"，那是 `idea-explorer` 的活（7 种头脑风暴方法）。spark 只记录作者**已经想到的**
2. **不帮作者产生新想法**——spark 是记录器，不是生成器
3. **不做灵感评估/筛选/优先级**——记录不筛选，"这个想法好不好"不是 spark 的事（呼应当初模板"记录，不筛选"原则）
4. **不做灵感的章节落地**——把灵感写进具体章节是 `plan-chapter` / `outline-tingle` 的活。spark 只负责把它落进灵感日志

## Completion Criterion

- ✅ Checkable：返回 `{appended: bool, count: N, path: "novel/inspiration-log.md", preview: string}`——`appended=true` 表示 N 条 bullet 已 append 到 `novel/inspiration-log.md` 的 `## 灵感流` 段
- ✅ Exhaustive：
  - capture mode：1 条 bullet 已 append，无交互
  - import mode：N 条 bullet 已 append，至少一轮"还有吗？"循环已执行

## Dependencies

| 依赖 | 用途 | 缺失时降级 |
|------|------|-----------|
| `file-manager` Skill | `ensure-file` 补齐 `novel/inspiration-log.md` | 🚫 硬阻断——无法 ensure 文件 |
| `novel/inspiration-log.md` | 落盘目标 | 由 file-manager `ensure-file` 补齐 |
| `framework/templates/inspiration-log.md` | 模板源 | file-manager `ensure-file` 缺失模板时 🚫 拒绝 |
