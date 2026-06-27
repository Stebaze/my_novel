---
name: outline-tingle
description: 大纲形成编排——从零 premise→主题→L1→L2→L3，2 session 薄封装层（original mode；adaptation 留 stub）
---

# Outline-Tingle Skill — 大纲形成编排

## Identity

大纲形成编排器——薄封装层，对标 `adaptation-workflow` 范式。不重复实现发散/grilling 方法论，仅串联 `idea-explorer`(mode=book) + `qing-novelist`(mode=book) 完成 premise→L3 全程。2 session 形态：Session 1 divergent（premise→主题），Session 2 grilling（主题→L1→L2→L3）。`outline.md` 本身作为书级 handoff 载体（frontmatter `workflow_position` 状态机管进度，不另建 handoff 文件——interaction-spec §2.4 书级例外）。

**核心差异**（vs `plan-chapter`）：plan-chapter 假定 outline.md L1-L3 已填实；outline-tingle 负责把它们从 `（待定）` 填到实质。plan-chapter 产章节级 handoff（8 字段）；outline-tingle 推进 outline.md frontmatter 状态机。

## Contract

| Aspect | Detail |
|--------|--------|
| **Input `mode`** | `original` \| `adaptation`（默认 `original`；`adaptation` 留 stub，Commit 8 实现） |
| **Calls** | `pre-flight-check`（启动门禁；C9 outline 实质填充检查待 Commit 6 加，本 commit 先声明调用关系）, `idea-explorer`(mode=book, Session 1), `qing-novelist`(mode=book, Session 2), `file-manager`(ensure-novel/ensure-draft，经 init-draft 间接调), `settings-manager`(init-draft, Session 2 末) |
| **Produces** | `outline.md`（Premise 段 + L1-L3 填实 + frontmatter `workflow_position` 推进）/ `project-config.md`（最小集）/ `_briefs/book-exploration.md`（idea-explorer 产）/ 草稿目录 |
| **Called by** | 用户入口（`/outline-tingle` Session 1 / `/outline-tingle continue` Session 2） |

## Triggers

- "从零写新书" / "我有 premise 想形成大纲" / "帮我定全书结构"
- `/outline-tingle`（Session 1 divergent）/ `/outline-tingle continue`（Session 2 grilling）
- "想写一个 XX 的故事但不知道怎么展开" / "premise 到大纲怎么落"

## Flow

### 启动判定（两 session 共用入口）

```
1. mode 判定：original（默认）/ adaptation（→ stub 分支）
2. 读 novel/project-config.md（若存在）——「创作模式 = 改编」→ 🚫 硬阻断：
   "改编流大纲形成由 adaptation-workflow 阶段 0.5 调本 Skill mode='adaptation' 触发，请改用 /adaptation-workflow"
3. 扫描 novel/chapters/ 有内容 → 🟡 软阻断警告：
   "检测到已有成稿，建议改用 /bootstrap-project 逆向产大纲；如需重提主题可放行进修订模式
    （修订模式完整流程 Out of Scope，本 commit 仅留此警告）" → 用户确认放行
4. 调 Skill("pre-flight-check", scope="writing") 做启动门禁（C9 待 Commit 6；本 commit C0-C8 跑过即可）
5. 读 outline.md frontmatter workflow_position 判定 session：
   ├── 空/缺失/非 outline-tingle-* → Session 1
   ├── outline-tingle-step1-done → Session 2（grilling 入口）
   ├── outline-tingle-l1-confirmed → Session 2 续（L2/L3 未完，断点续传）
   └── outline-tingle-step2-done → "大纲已形成，请用 /plan-chapter 1 开始章节规划"
```

### adaptation mode stub

`mode=adaptation` 分支存在但本 commit 不实现——返回提示「adaptation mode 待 Commit 8 实现。改编流大纲形成由 adaptation-workflow 阶段 0.5 调本 Skill mode="adaptation" 触发：Session 1 divergent 替换为读原作画像提取候选改编主题，Session 2 grilling 增加第九维原作对齐度。敬请期待。」不调任何子 Skill。

### Session 1：Premise → 主题（original mode, divergent）

```
1.1 读 premise：
    ├── 口述（用户当场给）→ 写入 outline.md Premise 段 3 子项（原始一句话/灵感来源/期望读者感受）
    └── inspiration-log.md 已有记录 → 提取并复述确认 → 写入 Premise 段
1.2 调 Skill("idea-explorer", mode="book", premise=<Premise 段>)
    → 产 _briefs/book-exploration.md（7 法应用到 premise→候选主题方向，≥3 个方向，50-100 字主题陈述句）
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
2.2 调 Skill("qing-novelist", mode="book", outline_path=<outline.md>) → 补 L1：
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
2.9 推进 frontmatter：workflow_position: outline-tingle-step2-done / produced_at: <ts> / resume_command: /plan-chapter 1
2.10 完成提示："大纲已形成 + 草稿已初始化。说「写第 1 章」即可开始 /plan-chapter 1。"
```

## Completion Criterion

- ✅ Checkable：
  - Session 1：返回 `{mode: "original", session: 1, exploration_path, theme_selected, outline_l1_partial_filled, workflow_position: "outline-tingle-step1-done"}` —— exploration_path 指向 `_briefs/book-exploration.md`；outline.md Premise 段 + L1 核心主题/一句话/终点画面已填（草稿）
  - Session 2：返回 `{mode: "original", session: 2, outline_fields_filled: [...], l1_ready, handoff_ready, project_config_path, draft_dir, workflow_position: "outline-tingle-step2-done"}` —— outline.md L1-L3 实质填充（无 `（待定）`），project-config.md 已落盘，草稿目录已创建
  - adaptation stub：返回 `{mode: "adaptation", status: "stub", message: "adaptation mode 待 Commit 8 实现"}`
- ✅ Exhaustive：
  - Session 1：步骤 1.1-1.6 全部执行；idea-explorer mode=book 已调用；outline.md Premise 段 + L1 部分字段已写入；frontmatter 已推进到 step1-done
  - Session 2：步骤 2.1-2.10 全部执行；qing-novelist mode=book 已调用；L1 全部填实（门禁 2 通过）；L2/L3 填实（门禁 3 通过）；project-config.md + 草稿已落盘；frontmatter 已推进到 step2-done
- 🚫 Stop：不调 plan-chapter——让用户自己触发下一章

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `idea-explorer` Skill（mode=book） | Session 1 步骤 1.2 | 🚫 硬阻断——主题发散不可降级 |
| `qing-novelist` Skill（mode=book） | Session 2 步骤 2.2/2.4/2.5 | 🚫 硬阻断——书级 grilling 不可降级 |
| `settings-manager` Skill（init-draft） | Session 2 步骤 2.8 | 🚫 硬阻断——草稿初始化不可跳过 |
| `file-manager` Skill | Session 2 步骤 2.8（init-draft 间接调） | 🚫 硬阻断——草稿目录无法建立 |
| `pre-flight-check` Skill | 启动判定步骤 4 | 🚫 硬阻断——启动门禁不可跳过（C9 待 Commit 6） |
| `novel/outline.md` | 两 session 核心 IO | 🚫 硬阻断——缺失时调 file-manager(ensure-novel) 补齐 v2 模板 |
| `novel/project-config.md` | 启动判定 + Session 2 产出 | ⚠️ 启动判定时缺失按原创模式继续 |

## 与其他组件的关系

| 组件 | 关系 |
|------|------|
| `idea-explorer` Skill | Session 1 调用（mode=book）——premise→候选主题方向，产 `book-exploration.md` |
| `qing-novelist` Skill | Session 2 调用（mode=book）——主题→L1→L2→L3 书级 grilling，产结构决策由本 Skill 写入 outline.md |
| `plan-chapter` Skill | 下游——本 Skill 产出 outline.md L1-L3 填实后，plan-chapter 读大纲跑章节规划 |
| `adaptation-workflow` Skill | 改编流——阶段 0.5 调本 Skill mode="adaptation"（Commit 8 实现）；启动判定检测到改编模式时硬阻断导向 adaptation-workflow |
| `bootstrap-project` Skill | 互补可串——本 Skill 正向产大纲后，bootstrap 可逆向补 voice/character/world（Commit 7 加跳过 1a 逻辑）；启动判定检测到已有成稿时建议 bootstrap |
| `pre-flight-check` Skill | 启动门禁（C9 outline 实质填充检查待 Commit 6 加） |
| `framework/templates/outline.md` | v2 模板（Commit 1 升级）——本 Skill 产出的落点，frontmatter 7 字段状态机 |
| `framework/templates/project-config.md` | 最小集配置模板——本 Skill Session 2 末填充 |
