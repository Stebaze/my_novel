---
sections:
  - heading: "## 总览"
    agents: [skill-author, dev]
    desc: "AI 写作文档的导航入口"
  - heading: "## 文件分工"
    agents: [skill-author]
    desc: "生成端 / 评审端 / 人读的精确分工"
  - heading: "## 新指纹入库"
    agents: [fingerprint-discovery]
    desc: "新指纹的最低记录流程"
metadata:
  type: index
  audience: skill-author + dev
  refactor_date: 2026-07-01
---

# AI 写作文档索引

> **本文档是导航入口**。不承载规则，只告诉每个 consumer 该读哪个文件。

---

## 总览

AI 写作相关文档按 consumer 拆分：

| 文件 | 受众 | 包含 | 大小 |
|------|------|------|------|
| [`ai-writing-dna.md`](ai-writing-dna.md) | **生成端**（sensory-writer / mo-writer / plan-chapter） | opus-dna 5 层结构 + 常见 AI 指纹 ❌ 范例（内嵌于第 3.6 节） | ~200 行 |
| [`ai-fingerprint-checklist.md`](ai-fingerprint-checklist.md) | **评审端**（ping-critic） | 10 条检测项清单 | ~30 行 |
| [`ai-writing-context.md`](ai-writing-context.md) | **人读**（项目作者/编辑） | AI 写作常见问题背景 | ~20 行 |

---

## 文件分工

- **生成端**（`sensory-writer` / `mo-writer` / `plan-chapter`）读 `ai-writing-dna.md`——5 层写作决策 + 内嵌 ❌ 范例
- **评审端**（`ping-critic`）读 `ai-fingerprint-checklist.md`——10 条核对清单
- **人**读 `ai-writing-context.md`——背景说明

**违反路由的后果**：本设计下生成/评审端文件无敏感内容（如旧版 fingerprint catalog 的 159 个违例句），错读不会污染生成上下文。

---

## 新指纹入库

新发现 AI 指纹时：
1. 先判断是否已在 [`ai-writing-dna.md`](ai-writing-dna.md) 第 3.6 节被覆盖（合并同类项）
2. 若未覆盖且值得记录：在 [`ai-fingerprint-checklist.md`](ai-fingerprint-checklist.md) 末尾追加一行
3. 调 `fingerprint-discovery` Skill 阶段 4 自动同步校验
4. 完成
