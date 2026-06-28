---
format_version: 2
produced_by: template
sections:
  - heading: "## 灵感流"
    skills: [spark, ask-yiyi, outline-tingle]
    desc: "单行 bullet 流——[时间] 内容 [#标签]，零结构负担"
  - heading: "## Agent 行为规范"
    skills: [spark, qing-novelist, plan-chapter]
    desc: "通用原则 + capture/import/读取/不进草稿 的具体规则"
---

# 灵感日志

> **定位**：作者碎片想法的横切记录。不是"写完之后的总结"，是"想到就记"的活文档。
> **横切工件**：绕过草稿隔离，直接落 `novel/inspiration-log.md`，跨章节跨 session 永久累积。
> **入口**：`/spark <一句话>`（capture 单条）/ `/spark import`（批量）/ `/spark`（默认进 import）。

---

## 灵感流

> 单行 bullet 流，每条一行，零结构负担。格式：`- [YYYY-MM-DD HH:MM] 内容 [#标签]`
> 标签可选——`#台词` `#设定` `#第N章` `#悬念` 自由打，不打也行。
> 不分表、不分优先级，记录不筛选。

<!-- 示例（注释行 + 缩进，不会被 grep ^- [ 提取）：
  - [2026-06-28 14:23] 主角妈该有口音 #设定
  - [2026-06-28 22:05] 第7章结尾留个钩子：反派其实知道真相 #悬念 #第7章
-->

---

## Agent 行为规范

### 通用原则

- **即时性**：想法出现时立即记录，不等"合适的时机"
- **原始性**：保留最初的语言，不美化、不整理、不加工
- **可追溯**：每条记录标注时间戳
- **可执行**：Agent 在后续对话中主动回顾未消化的灵感
- **宝库不是欠债**：氛围是"积累的资产"，不是"待办清单压力源"

### 具体规则

#### 写入（spark Skill 专属）

- **capture mode 零交互**：`/spark <一句话>` 直接 append 一行，不追问标签、不确认内容、不评估质量
- **import mode 批量切分**：粘贴多行文本，按 `-` / `*` / `1.` / 换行分隔符切分，每条加时间戳 append
- **append-only**：spark 只追加，不修改、不删除已记录的灵感（作者手改文件始终允许）
- **不评估**：记录不筛选——"这个想法好不好"不是 spark 的事

#### 提示（其他 Skill 的职责）

- **qing-novelist 启发交谈中**冒出好想法 → 提示作者"这个值得 `/spark <内容>` 记一下吗？"，**不自动写入**
- **plan-chapter 头脑风暴中**冒出"不适合本章但有趣"的方向 → 提示作者用 spark，**不自动写入**
- **idea-explorer 发散中**冒出备用方向 → 提示作者用 spark，**不自动写入**

#### 读取

- **ask-yiyi 会话启动**：Read 末尾 50 行，grep `^- \[` 提取真实 bullet（排除 `<!--` 注释），呈现最近 5 条 + 总数，不标记消化状态
- **outline-tingle premise 阶段**：从 `novel/inspiration-log.md` grep bullet 提取，复述确认后写入 outline.md Premise 段
- **文件不存在**：静默跳过——inspiration-log 是可选工件，不报缺失

#### 文件位置契约

- **权威源**：`novel/inspiration-log.md`（绕过草稿，横切工件不进草稿隔离）
- **草稿侧不副本**：file-manager `ensure-draft` 清单不含 inspiration-log.md，避免双副本不一致
- **首次创建**：作者第一次 `/spark` 时由 spark 调 `file-manager(ensure-file)` 单文件补齐
