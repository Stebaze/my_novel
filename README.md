# my_novel

AI 辅助长篇小说写作工程。以 Claude Code 为载体，21 个 Skill 协作完成大纲规划、写作简报、AI 生成、综合评审到发布的完整流程。

> **AI 不写正文**——产出写作简报和修改报告，笔始终在你手里。

## 特性

- **4 session 工作流**：plan → handoff → generate → review → publish，每段独立 session 控制上下文
- **21 个 Skill 协作**：从规划到发布的完整链路，单层 Skill 架构（Skill 可调 Skill）
- **三层稿件体系**：原稿（只读）/ 草稿（自由）/ 正式稿（已发布锁定）
- **设定时间线管理**：所有设定按章节版本化，修改时向前扫描冲突
- **断点续传**：通过检查磁盘产物判断进度，中断后从断点继续
- **AI 生成整章模式**：plan → handoff → generate → review 全自动生成整章，最多 2 轮 Fix 循环

## 快速开始

```bash
git clone <repo>
cd my_novel
claude  # 启动 Claude Code
```

启动后系统自动加载 `CLAUDE.md` 中的项目配置。

**5 分钟上手**：

| 你想做的事 | 说什么 |
|-----------|--------|
| 写新章节 | "写第X章" |
| 评审章节 | "评审第X章" |
| 发布章节 | "发布第X章" |
| 导入已有章节 | "导入章节" |
| 冷启动项目 | "初始化项目" |
| 改编作品 | "改编这个作品" |

完整操作指南见 [`用户使用指南.md`](用户使用指南.md)。

## 4 session 工作流

```
SESSION 1 — 规划（plan）
  /plan-chapter {N}
    ├── 前置检查 + 设定快照 + 草稿初始化
    ├── 五更启发式交谈 → 方向卡
    └── Handoff 输出

[HANDOFF] 新会话 /generate-chapter {N}

SESSION 2 — 生成（generate）
  /generate-chapter {N}
    ├── 写作简报（mo-writer）
    ├── AI 生成整章（sensory-writer per-scene + 200字摘要）
    ├── 自动评审（chapter-review ai-content）
    └── 最多 2 轮 Fix 循环

SESSION 3 — 人工复审（可选）
  /chapter-review {N}（writing mode）

SESSION 4 — 发布（publish）
  /publish-chapter {N}
    ├── 设定合并
    └── 发布前琉璃校验
```

## 21 个 Skill 入口

| Skill | 触发词 | 一句话功能 |
|-------|--------|-----------|
| **plan-chapter** | 写第X章 | 章节规划（系统管道 + 五更交谈 + handoff）|
| **generate-chapter** | /generate-chapter {N} | AI 生成整章（简报 + per-scene + 评审 + Fix）|
| **chapter-review** | 评审第X章 | 3 mode 评审（writing/ai-content/adaptation）|
| **publish-chapter** | 发布第X章 | 设定合并 + 草稿同步 + 琉璃校验 |
| **adaptation-workflow** | 改编这个作品 | 原作画像 + 逐章改编循环 |
| **bootstrap-project** | 初始化项目 | 冷启动（批量导入 + 全文逆向分析 + 工件生成）|
| **import-chapter** | 导入章节 | 多格式导入（md/txt/docx/epub）+ 设定扫描 |
| **pre-flight-check** | （系统调用）| C0-C8 就绪检查 + 阻断判定 |
| **settings-manager** | （系统调用）| 设定读取/写入/合并/角色状态 |
| **file-manager** | （系统调用）| 三层文件补齐 |
| **migration-keeper** | （系统调用）| 格式检测 + 兼容性 + 迁移 |
| **ask-yiyi** | （会话启动）| 会话初始化管道（检测/同步/进度）|
| **mo-writer** | （系统调用）| 7 层写作简报生成 |
| **sensory-writer** | （系统调用）| 感官锚定 AI 章节生成（single/per-scene）|
| **ping-critic** | （系统调用）| 综合评审（心流 + 指纹 + 校对 + 三维）|
| **qing-novelist** | （系统调用）| 12 维启发交谈 + 7 维作者分析 |
| **idea-explorer** | （系统调用）| 7 种头脑风暴方法 |
| **voice-sculptor** | （系统调用）| 角色声音实验（生成式/挖掘式）|
| **technique-selector** | （系统调用）| 技法智能匹配 |
| **yin-illustrator** | （系统调用）| 场景视觉设计 + 插画 prompt |
| **fingerprint-discovery** | 指纹分析 | 未知指纹发现 + 形式化 + 入库 |

## 文档导航

- **[用户使用指南.md](用户使用指南.md)** —— 作者视角的完整操作手册
- **[CLAUDE.md](CLAUDE.md)** —— Agent 视角的强制规则 + 工作流图
- **[framework/_specs/interaction-spec.md](framework/_specs/interaction-spec.md)** —— Skill 命名/调用/handoff 协议
- **[framework/_specs/skill-template.md](framework/_specs/skill-template.md)** —— Skill 5 必含字段模板

## 项目结构

```
my_novel/
├── CLAUDE.md                  # 8 条强制规则 + 工作流
├── 用户使用指南.md              # 作者操作手册
├── .claude/skills/            # 21 个 Skill 定义
├── framework/                 # 通用框架（specs/guides/templates）
└── novel/                     # 当前小说实例（⚠️ 不在 git 中）
```

## 许可

MIT
