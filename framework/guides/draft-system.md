---
sections:
  - heading: "## 三层体系"
    agents: [file-manager, settings-keeper, ask-yiyi]
    desc: "原稿/草稿/正式稿三层定义——目录/性质/修改权限"
  - heading: "## 目录结构"
    agents: [file-manager]
    desc: "草稿目录树标准结构"
  - heading: "## 草稿会话管理"
    agents: [file-manager, settings-keeper]
    desc: "会话命名规则/创建/切换/跨会话对比"
  - heading: "## 共享文件"
    agents: [file-manager]
    desc: "草稿复用正式环境文件的清单"
  - heading: "## 迁移到正式目录"
    agents: [file-manager, settings-keeper]
    desc: "草稿章节验证通过后的迁移步骤"
---

# 草稿

> **定位**：三层稿件体系中的**草稿层**。支持多份独立草稿会话，按日期时间区分。每个会话有独立的 `chapters/` 和 `notes.md`。

## 三层体系

| 层 | 目录 | 性质 | 修改 |
|----|------|------|------|
| **原稿** | `novel/_reference/` | 用户上传的原始素材，只读 | 禁止 |
| **草稿** | `novel/_drafts/` ← 本目录 | 多会话草稿空间，AI 生成/人工改写 | 自由 |
| **正式稿** | `novel/chapters/` | 已确认的发布版本 | 谨慎 |

## 目录结构

```
_drafts/
├── README.md                    # 本文件
├── _index.md                    # 草稿会话索引（活跃会话、会话列表）
├── notes.md                     # 草稿层总体摘要
│
├── YYYY-MM-DD-label/             # 会话目录（按日期区分）
│   ├── notes.md                  # 本次会话的决策记录
│   └── chapters/                 # 草稿章节
│       └── chapter-NN.md
```

## 草稿会话管理

### 会话命名

格式：`YYYY-MM-DD[-label]`

- `2026-05-27-new-ch3` — Ch3 的实验性改写
- `2026-05-28-alt-ch5` — Ch5 的另一个版本

### 创建新会话

对 Agent 说"在新草稿中写 ChX"或"创建新的草稿会话"。

### 切换会话

对 Agent 说"切换到 2026-05-27-ai-rewrite 的草稿"。

### 跨会话对比

对 Agent 说"对比两个草稿会话的 Ch5"。

## 共享文件

草稿复用以下正式环境的文件（不复制，直接读取）：

- `novel/_reference/` — 原稿（作者风格基准）
- `novel/characters/` — 角色档案
- `novel/world/` — 世界观设定
- `novel/author-voice.md` — 作者文风档案
- `novel/style-guide.md` — 写作风格手册
- `novel/technique-library.md` — 技法素材库
- `novel/project-config.md` — 项目类型配置
- `novel/outline.md` — 全书大纲

## 迁移到正式目录

草稿章节验证通过后：

1. 确认章节不依赖草稿独有的设定变更
2. 将 `.md` 文件复制到 `novel/chapters/`
3. 更新正式 `novel/notes.md` 和角色档案
4. 在草稿会话 notes.md 中标记"已迁移"
