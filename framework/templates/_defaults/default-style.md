---
profile_id: "project-default-style"
version: "1.0"
design_date: "2026-07-01"
status: "项目默认写作风格 spec（git tracked）"
format: "声明+指向（不重复内容）"
supersedes: null
is_project_default: true
---

# 项目默认写作风格 — 中国网文形式 + 败犬女主风格

> **本 spec 是项目级默认**——fresh clone 后 `novel/project-config.md` 不修改字段时，sensory-writer 走此默认生成章节，**不需要 `profiles/authors/` 下任何文件**（profiles/authors/ 在 `.gitignore` 中，可为空）。
>
> **若用户指定作家**（`project-config.md` 字段 `作家: "<作者名>"`，用户本地 `profiles/authors/<作者名>.md` 存在）——sensory-writer 加载对应 v3.0 档案（POV 4 维 + 设计流程 3 阶段），替代风格 fallback 层。**基底保持不变**——仍走 chinese-webnovel-base。

## 默认 combo

| 维度 | 默认值 | 源文件 | git 状态 |
|------|--------|--------|---------|
| **基底** | `chinese-webnovel-base` | [`framework/templates/_style-bases/chinese-webnovel-base.md`](../_style-bases/chinese-webnovel-base.md) | ✅ tracked |
| **主题** | `romance` | [`framework/templates/_themes/theme-romance.md`](../_themes/theme-romance.md) | ✅ tracked |
| **风格 fallback** | 见 `framework/templates/_styles/` 下 6 个 fallback 之一（默认选败犬女主对应 fallback 文件）| `framework/templates/_styles/<fallback>.md` | ✅ tracked |
| **作家** | `""`（不指定）| 不加载 `profiles/authors/` | — |

## 加载链（作家="" 时）

```
novel/project-config.md
  ├ 作家 = ""                            → 不走 profiles/authors/
  ├ 主风格档案 = "chinese-webnovel-base"  → _style-bases/chinese-webnovel-base.md
  ├ 主题 = ["romance"]                    → _themes/theme-romance.md
  └ 风格 = "<败犬女主对应 fallback 文件名>"  → _styles/<该文件>.md
```

## 默认 combo 的写作语感（给作者/agent 直观感受）

- **中国网文形式**：多 POV / 第三人称、事件-岛弧驱动、信息差机制、规模大、高潮大型、卷末揭/集中揭——**6 坐标轴全向"长/大/重"侧**
- **败犬女主风格**：路人性自嘲叙述者、情感淡描（不直写"她很悲伤"，写"她合上便当盒，盖子没盖紧"）、元叙事自嘲、败犬揭示 5 拍（男主私人场景 → 第三方闯入 → 无意看到 → 败犬认出 → 失败承认式收束）、三人场景+物理小物潜台词、**不自贬不升华**（败犬收束 = "放手的觉悟" ≠ "我好惨"）

**核心反差**（实验性组合的意义）：中国网文"事件-岛弧-大型"骨架 × 败犬女主"路人性自嘲+情感淡描"语感——**大开大合的事件铺陈，落到极私密的物理动作上**。

## 适用场景

- ✅ 校园+多女主+单恋落败（败犬女主原生场景）
- ✅ 末日/穿越/系统背景下的多女主情感线（中国网文形式+败犬情感语感）
- ✅ 长篇网文连载（事件-岛弧驱动匹配网文节奏）
- ⚠️ 推理/悬疑/无感情线题材——败犬女主风格 fallback 不匹配，建议改用 `framework/templates/_styles/` 下其他 fallback（具体由题材决定）

## 何时覆写默认

- `project-config.md` 字段 `作家` 指定具体作者（用户本地 `profiles/authors/<作者名>.md` 存在）→ 走作者档案，**不加载默认风格 fallback**
- `project-config.md` 字段 `主风格档案` 改 `japanese-light-novel-base` → 换基底，**风格 fallback 字段可能也需调整**
- `project-config.md` 字段 `主题` 加叠 `["romance", "mystery"]` → 主题叠加，**基底+风格保持**

## 修订记录

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0 | 2026-07-01 | 初版——声明「中国网文形式+败犬女主风格」= 项目默认（fresh clone 即可用） |
