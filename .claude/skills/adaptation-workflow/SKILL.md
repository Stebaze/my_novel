---
name: adaptation-workflow
description: 文学作品的体系化改编——原作画像提取+逐章改编循环（复用写作工作流）
---

# Adaptation Workflow Skill — 体系化改编

## Identity

改编工作流是标准写作流的**薄封装层**——不重复实现写作/评审逻辑，仅在原作画像约束下串联 `plan-chapter` / `chapter-review`。当 `novel/project-config.md` 中「创作模式 = 改编」时自动接管所有写作请求。

**核心差异**（vs 标准写作流）：
- **阶段 0 强制前置**：六维原作画像提取——改编流独有阶段（描述性，原作是什么）
- **阶段 0.5 强制前置**：改编大纲形成（调 `outline-tingle mode="adaptation"`）——改编流独有阶段（规范性，改成什么）；原作画像与改编大纲分两层
- **plan-chapter 模式**：`mode="adaptation"` 增加 §0A 源文对照层 + L1-L6 改写深度选择
- **chapter-review 模式**：`mode="adaptation"` 增加原作对齐维度（严格/平衡/宽松）

## Contract

| Aspect | Detail |
|--------|--------|
| **Calls** | `qing-novelist`（六维原作画像 — 分析模式）, `ping-critic`（defect-marking 缺陷标记）, `outline-tingle`（mode="adaptation"，阶段 0.5 产改编大纲）, `plan-chapter`（mode="adaptation"）, `chapter-review`（mode="adaptation"） |
| **Produces** | `reference/manuscripts/_analysis/{作品名}.md`, `outline.md`（mode=adaptation，阶段 0.5 产）, `{draft}/_adaptation-tracker.md` |
| **Called by** | 用户入口（"改编这个作品" / "逐章改编"） |

## Triggers

- "改编这个作品" / "改写/润色这个" / "基于这个作品写一版新的"
- "逐章改编" / "一章一章来" / "按章节改编" / "边改边看"
- "帮我润色这个原稿"

## Flow

### 阶段 0：原作画像提取（🚫 硬阻断前置）

> 唯一独有阶段。未完成时禁止进入逐章循环。

**0.1 路径感知**：
1. 读 `novel/project-config.md` 确认「创作模式 = 改编」+「原作来源」路径
2. 检查 `reference/manuscripts/_analysis/` 是否已存在 `{作品名}.md`
3. 不存在 → 调 `qing-novelist`（分析模式 → Step 4 七维作者分析协议），对原作执行六维提取
4. 提取方法：逐章扫描，每条信息标注出处章节/段落，推测性信息标注"推测"

**0.2 缺陷标记**：调 `ping-critic`（operation="defect-marking"），与 0.1 串行或并行；输出追加到画像文档 §七「琉璃标注」

**0.3 门禁**：画像文件落盘 → 阶段 0 完成 → 进入逐章循环

**🚫 硬阻断**：画像文件不存在 → 禁止进入改编规划

### 阶段 0.5：改编大纲形成（🚫 硬阻断前置）

> 原作画像（描述性，原作是什么）后、逐章循环前，产出改编大纲（规范性，改成什么）。调 `outline-tingle mode="adaptation"` 完成 premise→L1→L2→L3。原作画像与改编大纲分两层——前者是原作的客观画像，后者是改编后的目标结构。

**0.5.1 调 outline-tingle mode="adaptation"**：

1. 读 `reference/manuscripts/_analysis/{作品名}.md` 已落盘（阶段 0 产物）→ 作为 outline-tingle Session 1 divergent 的素材源
2. 调 `Skill("outline-tingle", mode="adaptation")` → 触发 outline-tingle 2 session 流程：
   - **Session 1**：内联读原作画像 → 列 3-5 个候选改编主题方向（保留主线/删减支线/改结局/换视角/主题转译）→ 作者选定 → 写 `outline.md` Premise + L1 草稿
   - **Session 2**：调 `qing-novelist mode=book`（含第九维「原作对齐度」B9）→ 补 L1/L2/L3 + 写 `project-config.md`（创作模式=改编）+ `init-draft`
3. outline-tingle 完成后 `outline.md` frontmatter `mode: adaptation` + `workflow_position: outline-tingle-step2-done`

**0.5.2 门禁**：`outline.md` L1-L3 实质填充（无 `（待定）`）+ frontmatter `mode: adaptation` + `workflow_position: outline-tingle-step2-done` → 阶段 0.5 完成 → 进入逐章循环

**🚫 硬阻断**：`outline.md` 未达门禁（任一字段含 `（待定）` / frontmatter 标记缺失 / `workflow_position` 未推进到 `step2-done`）→ 禁止进入逐章循环，提示用户继续 `/outline-tingle continue` 完成 Session 2

### 逐章循环

```
Step 1: plan-chapter(mode="adaptation")
  传 target_chapter=N, source_portrait=画像路径, source_files=源文范围
  → 产出改编简报（标准 7 层 + §0A 源文对照层 + 改写深度选择 L1-L6）

[用户自己执笔改编正文]

Step 2: chapter-review(mode="adaptation")
  传 target_chapter=N, alignment_level=严格/平衡/宽松（默认平衡）
  → 产出综合评审报告（标准三维 + 原作结构对齐/设定一致性/风格 fidelity）

Step 3: 更新 {draft}/_adaptation-tracker.md
Step 4: 询问下一章源文位置 + 内容方向 → 回到 Step 1
```

**对齐级别**（chapter-review 评审前由用户选择）：

| 级别 | 结构对齐 | 设定对齐 | 风格对齐 |
|------|---------|---------|---------|
| 严格 | 事件序列一一对应 | 设定不得偏离 | 风格偏离需标注 |
| 平衡（默认） | 主要事件保留 | 核心设定保留 | 风格可优化 |
| 宽松 | 仅核心情节保留 | 仅世界观基础保留 | 风格自由 |

### 退出与切换

| 用户指令 | 行为 |
|---------|------|
| "下一章原创" | 本章切标准写作流（plan-chapter mode="writing"）|
| "之后都原创" | 退出改编流，后续全走标准流 |
| "结束改编" / "改编完成" | 输出改编摘要（原创 N 章 / 改编 N 章）|
| "跳过这章" | 追踪表标记跳过 |

## Completion Criterion

- ✅ Checkable：返回 `{current_chapter, mode: "改编", alignment_level, 原作画像存在性, 改编大纲就绪性}` 给用户
- ✅ Exhaustive：阶段 0 画像已落盘 + 阶段 0.5 改编大纲已落盘（`outline.md` frontmatter `workflow_position: outline-tingle-step2-done` + `mode: adaptation`）+ 逐章循环当前章 plan/评审产物在磁盘
- 🚫 Stop：不进入下一 Skill 调用——让用户选择下一章

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `qing-novelist`（分析模式） | 阶段 0.1 | 🚫 硬阻断——原作画像不可降级 |
| `ping-critic`（defect-marking） | 阶段 0.2 | 🚫 硬阻断——缺陷标记不可跳过 |
| `outline-tingle`（mode="adaptation"） | 阶段 0.5 | 🚫 硬阻断——改编大纲不可降级 |
| `plan-chapter` | Step 1 | 🚫 硬阻断——改编规划不可跳过 |
| `chapter-review` | Step 2 | 🚫 硬阻断——改编评审不可跳过 |
| `reference/manuscripts/{原作}.md` | 阶段 0 | 🚫 硬阻断——源文不可读则无法开始 |
| `reference/manuscripts/_analysis/{作品名}.md` | 阶段 0 产物 → 阶段 0.5 输入 | 🚫 硬阻断——画像不存在禁止改编 |
| `outline.md`（mode=adaptation） | 阶段 0.5 产物 → 逐章循环输入 | 🚫 硬阻断——改编大纲未达门禁（`workflow_position` 非 `outline-tingle-step2-done`）禁止进逐章循环 |
