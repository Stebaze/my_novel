# 阶段 0：Pre-Flight Check（+ Resolve Context + Artifact Routing）

## 目标

三件事合一：(1) 解析上下文参数 → (2) 调 pre-flight-check 跑 C0-C7.5 门禁 → (3) 工件存在性检查 + 路由到对应阶段。

## 步骤 1：Resolve Context

```
1. 扫描 novel/_drafts/ → 最新日期目录 → draft_dir；无草稿 → draft_dir = novel/
2. 读 {draft_dir}/notes.md「当前进度」→ target_chapter
3. 读 {draft_dir}/project-config.md「创作模式」→ output_format（默认 "prose"）
4. 从大纲 + 前一章角色状态推断出场角色列表 chapter_characters
5. 工作流模式判定（贯穿阶段 5）：
   └── 统一走 4-Skill 对称架构（阶段 5 写 handoff 后退出）
```

## 步骤 2：调 `pre-flight-check`

```
调 Skill("pre-flight-check")
  传入：target_chapter, draft_dir, scope="writing", chapter_characters
  → 跑 C0-C7.5 基础检查（不含 C8——plan 阶段尚无 handoff）
  → 🚫 硬阻断 → 列出，等待用户解决
  → 🟡 软阻断 → 用户确认后继续
  → ⚠️ 提醒 → 标注，不阻断
```

**与 generate-chapter 的分工**：

- `plan-chapter` 阶段 0 调 pre-flight-check：跑 C0-C7.5，**不包含 C8 handoff 验证**
- `generate-chapter` Step 0 调 pre-flight-check：跑 C8（handoff 验证 + 8 字段契约），是入口硬阻断

## 步骤 3：Artifact Routing

```
检查磁盘产物 → 定位当前进度：

0. _briefs/chapter-{N}-handoff.md 存在？
   → 已生成。提示用户开新会话输入 /generate-chapter {N}。退出。

1. _briefs/chapter-{N}-brief.md 存在？
   → 规划已完成。返回简报路径。如需重规划：用户确认后继续。

2. _briefs/chapter-{N}-direction.md 存在？
   → 方向卡已产出。呈现概要 → 用户确认继续/调整。
   ├── 确认 → 跳到阶段 5
   └── 调整 → 跳到阶段 4（分派 qing-novelist，resume=true）

3. _briefs/chapter-{N}-exploration.md 存在？
   → 探索卡存在。呈现探索卡摘要 → 询问：
   ├── "基于已有探索方向继续启发式交谈" → 跳到阶段 4
   ├── "想重新头脑风暴" → 标记 exploration_stale=true → 继续阶段 3
   └── "不需要探索卡，直接规划" → 跳过阶段 3

4. 都不存在 → 询问作者：
   ├── "我有大致方向" → 从阶段 1 开始
   └── "我卡住了/没有方向" → 标记 need_brainstorming=true → 从阶段 1 开始 → 阶段 3 激活
```

## 输出

- `draft_dir` / `target_chapter` / `scope` / `chapter_characters` / `output_format` 传递给后续阶段
- 路由结果：续跑入口（从阶段 N 继续）/ 全新开始（从阶段 0 开始）
- 阻断摘要：🚫 项列表 + 修复路径（来自 pre-flight-check）

## 降级

- `pre-flight-check` 不可用 → 🚫 硬阻断
- 扫描产物失败 → ⚠️ 标注"工件扫描降级为全量列举"，不阻断
