---
sections:
  - heading: "## 创作模式"
    skills: [plan-chapter, adaptation-workflow, ask-yiyi]
    desc: "原创/改编模式+写作类型+节拍窗口大小+原作来源——决定工作流路由的核心配置"
  - heading: "## 叙事配置"
    skills: [mo-writer, qing-novelist, plan-chapter]
    desc: "叙事人称/叙述者身份/叙事基调/驱动方式——声音和视角的基础约束"
  - heading: "## 类型配置"
    skills: [mo-writer, qing-novelist, technique-selector]
    desc: "主类型/子类型/超自然元素/战斗元素——决定技法库和对话风格的选取"
  - heading: "## 关系线配置"
    skills: [mo-writer, qing-novelist]
    desc: "核心关系线定义+类型+进展阶段"
  - heading: "## 平台配置"
    skills: [mo-writer]
    desc: "发布平台+字数约束+章节频率——影响简报的篇幅和节拍设计"
  - heading: "## 节拍配置"
    skills: [mo-writer, plan-chapter]
    desc: "宏观节拍窗口大小+高潮密度+冷却比例——大尺度节奏约束"
  - heading: "## 3 维风格档案（v3.0）"
    skills: [mo-writer, sensory-writer, chapter-review, generate-chapter]
    desc: "基底+主题+风格 fallback——sensory-writer Step 0.1 加载链的字段源"
  - heading: "## 项目默认风格"
    skills: [mo-writer, sensory-writer, ask-yiyi, pre-flight-check]
    desc: "声明本项目默认 = 中国网文形式+败犬女主风格——指向 framework/templates/_defaults/default-style.md"
  - heading: "## 参考作品"
    skills: [qing-novelist, mo-writer]
    desc: "风格/结构/角色参考来源作品列表"
  - heading: "## Agent 行为指引"
    skills: [mo-writer, ping-critic, qing-novelist]
    desc: "各Skill在写作/评审/交谈时的行为约束"
---

# 项目配置

> **默认填值（2026-07-01 v2.1）**：本模板的默认字段值 = 项目默认写作风格「中国网文形式+败犬女主风格」（见 `framework/templates/_defaults/default-style.md`）。
>
> **Fresh clone 行为**：`file-manager ensure-novel` 复制本模板到 `novel/project-config.md` 后即用——sensory-writer 走 `chinese-webnovel-base + amamorin-style-fallback` 链，不需要 `profiles/authors/` 下任何文件。
>
> **覆写方式**：用户可在本文件中改任意字段（`作家` 字段指定具体作者时 → 加载 `profiles/authors/{作家}.md` 替代 amamorin-style fallback）。

## 创作模式

- **创作模式**：original
- **输出格式**：prose
- **写作类型**：中篇(300-800章)
- **节拍窗口大小**：30
- **原作来源**：（改编模式时填写。例如：`novel/_import/trpg_settings_logs/` 或 `reference/manuscripts/{作品名}/`）
- **原作类型**：（改编模式时填写。选择：TRPG跑团记录 / 小说 / 剧本 / 其他）
- **改编风格参照**：（改编模式时填写。例如：参考 `framework/templates/_styles/` 下某 fallback 文件的 3 块风格作为改编目标）

## 叙事配置

- **叙事人称**：第三人称
- **叙述者身份**：多 POV 切换（中国网文基底默认；败犬情感线用自由间接引语带 POV 角色腔调）
- **叙事基调**：温-自嘲-吐槽 + 中国网文大开大合事件铺陈
- **驱动方式**：事件-岛弧驱动（中国网文基底）+ 关系-对话辅线（败犬女主风格）

## 类型配置

- **主类型**：中国网文+校园/末日/系统背景 + 恋爱败犬线
- **子类型**：多女主 + 单恋落败 + 物理小物潜台词
- **是否有超自然元素**：可选（默认无；中国网文基底支持加叠 system/scifi-fantasy/doomsday 主题）
- **是否有战斗/动作元素**：中度（中国网文事件-岛弧驱动通常含动作场景）

## 关系线配置

- **是否有恋爱主线**：是
- **恋爱线比重**：主线
- **关系模式**：多女主 + 单恋落败 + 8+ 女主轮换焦点（败犬女主风格）
- **情感基调**：放手的觉悟（不自贬不升华）

## 平台配置

- **目标平台**：起点中文网
- **每章目标字数**：~2500-3000（中国网文连载节奏）
- **是否有上架/VIP收费机制**：是（按起点规则简述）

## 节拍配置

- **节拍窗口**：30（中篇 30 章/卷）
- **每章场景数**：3（多场景模式；设为 1 启用单场景模式）
- **单场景模式**：false

## 3 维风格档案（v3.0）

```yaml
# 3 维正交风格档案——基底+主题+风格 fallback；指定作家时回退到 profiles/authors/{作家}.md
作家: ""  # 默认空字符串→走 fallback 风格层；指定时 sensory-writer 加载 profiles/authors/{作家}.md
主风格档案: "chinese-webnovel-base"  # 基底（必填 1 个，2 选 1：japanese-light-novel-base / chinese-webnovel-base）
主题:  # 主题（必填 1-N 个，可叠加）
  - "romance"
风格: "amamorin-style-fallback"  # 风格 fallback（不指定作家时用，6 选 1：kuiguannan/amamorin/shiniki/yuantong/fengyue/buluofeng）
```

**加载路径（git tracked ✅ 即可用）**：

| 维度 | 字段值 | 加载路径 |
|------|--------|---------|
| 基底 | `chinese-webnovel-base` | `framework/templates/_style-bases/chinese-webnovel-base.md` |
| 主题 | `romance` | `framework/templates/_themes/theme-romance.md` |
| 风格 fallback | `amamorin-style-fallback` | `framework/templates/_styles/amamorin-style.md` |

## 项目默认风格

> **本项目默认 = 中国网文形式 + 败犬女主风格**。
>
> 详细 spec：[`framework/templates/_defaults/default-style.md`](_defaults/default-style.md)
>
> 加载链：
> - 基底 `chinese-webnovel-base`（多 POV/第三人称 + 事件-岛弧 + 信息差 + 大规模 + 大型高潮 + 卷末揭/集中揭）
> - 主题 `romance`（物理小物 + 败犬揭示 5 拍 + 自由间接引语）
> - 风格 fallback：`framework/templates/_styles/` 下败犬女主对应文件（路人性自嘲 + 情感淡描 + 元叙事自嘲 + 物理小物潜台词 + 不自贬不升华）
>
> **覆写方式**：本文件任一字段改值即覆写——例如改 `作家: "<用户本地存在的作者名>"` 则加载 `profiles/authors/<作者名>.md` 替代默认风格 fallback；改 `主风格档案: "japanese-light-novel-base"` 则换基底。

## 参考作品

> Agent 在使用技法素材库时优先选择与参考作品匹配的模式。

<!-- 列出 1-3 部风格基准作品，每部附核心技法和参考维度。注：避免在 git tracked 文本中点名具体作家——用通用风格名/题材名描述 -->
1. （败犬女主对应 fallback 风格文件）——描述见 `framework/templates/_styles/` 下对应文件
   - 核心技法：路人性自嘲叙述 + 败犬揭示 5 拍 + 物理小物潜台词 + 不自贬不升华
   - 参考维度：校园+多女主+单恋落败的关系-对话语感
2. （可选）
3. （可选）

## Agent 行为指引

> Agent 在读取本配置后，自动做出以下调整。根据上方的配置参数填写。

| 参数 | Agent 行为调整 |
|------|--------------|
| `作家 = ""` | 不加载 `profiles/authors/`；走 style_profile 3 维链（基底+主题+风格 fallback）|
| `主风格档案 = "chinese-webnovel-base"` | mo-writer 读 6 坐标轴（多 POV/事件-岛弧/信息差/大规模/大型高潮/卷末揭）|
| `主题 = ["romance"]` | mo-writer 读 romance 主题 5 字段（物理小物 + 败犬揭示 5 拍 + 自由间接引语 + 恋人关系原型 + 言情域词）|
| `风格 = "amamorin-style-fallback"` | sensory-writer 读 3 块 fallback（叙述态度+域词+桥段）；指定作家时不加载本层 |
| `目标平台 = 起点中文网` | mo-writer 按网文连载节奏定节拍（章末悬念 + 字数 2500-3000 + 跨章钩子）|
| `关系模式 = 多女主+单恋落败` | 技法库优先选败犬揭示+物理小物+三人场景；POV 角色=路人性锚点 |
