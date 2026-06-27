# my_novel

AI 辅助长篇小说写作工程。以 Claude Code 为载体，22 个 Skill 协作完成书级大纲、章节规划、写作简报、AI 生成、综合评审到发布的完整流程。

> **AI 不写正文**——产出写作简报和修改报告，笔始终在你手里。

## 特性

- **ask-yiyi 统一入口**：会话启动自动加载项目状态、智能推荐下一步、菜单按场景分组
- **书级前置 → 章节循环**：outline-tingle（premise→L1→L2→L3）先形成大纲，再进 4-Skill 章节循环
- **4-Skill 对称工作流**：plan → handoff → generate → review → publish，每段独立 session 控制上下文
- **22 个 Skill 协作**：从冷启动到发布的完整链路，单层 Skill 架构（Skill 可调 Skill）
- **三层稿件体系**：原稿（只读）/ 草稿（自由）/ 正式稿（已发布锁定）
- **设定时间线管理**：所有设定按章节版本化，修改时向前扫描冲突
- **断点续传**：通过检查磁盘产物判断进度，中断后从断点继续
- **AI 生成整章模式**：plan → handoff → generate → review 全自动生成整章，最多 2 轮 Fix 循环
- **改编工作流**：支持从已有作品反向提取原作画像 + 逐章改编
- **单场景模式**：每章场景数配置驱动，移动端减负

## 快速开始

```bash
git clone https://github.com/Stebaze/my_novel
cd my_novel
claude  # 启动 Claude Code
```

启动后 **ask-yiyi 自动接管会话初始化**：
1. 检测项目格式（migration-keeper）
2. 加载项目状态（设定 / 草稿 / 章节进度）
3. 给出 5 字段摘要 + 智能推荐下一步

**5 分钟上手**：

| 你想做的事 | 说什么 |
|-----------|--------|
| 从零写新书（先形成大纲）| "从零写新书" / "形成大纲" / `/outline-tingle` |
| 写新章节 | "写第X章" |
| AI 生成整章 | "继续" / "/generate-chapter {N}" |
| 评审章节 | "评审第X章" |
| 发布章节 | "发布第X章" |
| 导入已有章节 | "导入章节" |
| 冷启动项目 | "初始化项目" |
| 改编作品 | "改编这个作品" |
| 答疑 | "/ask-yiyi qa" / "怎么用" |

完整操作指南见 [`用户使用指南.md`](用户使用指南.md)。

## ask-yiyi 统一入口

ask-yiyi 是会话级入口，启动后自动加载。**5 种操作**：

| 操作 | 触发词 | 用途 |
|------|--------|------|
| `init` | 会话启动（自动）| 加载项目状态 + 给出摘要 + 推荐下一步 |
| `route` | `/ask-yiyi` / "创作工坊" / "工坊" | 列出主菜单并路由 |
| `next` | "继续" / "下一步" | 根据状态机直接给推荐操作 |
| `qa` | `/ask-yiyi qa` / "怎么用" | 答疑（工具用法）|
| `qa check` | `/ask-yiyi qa check` / "检查" | 异常审计 |

**主菜单三组**：
- **继续写这本书**：plan-chapter / generate-chapter / chapter-review / publish-chapter / import-chapter
- **创建新书**：bootstrap-project / outline-tingle / adaptation-workflow
- **其他工具**：idea-explorer / qing-novelist / qa / qa check

**状态机 → 智能建议**（init 时根据磁盘工件自动判断）：

| 状态 | 推荐 |
|------|------|
| `NO_PROJECT` | bootstrap / outline-tingle / adaptation |
| `OUTLINE_MISSING` | outline-tingle（书级大纲未填实，🟡 软阻断） |
| `NO_HANDBOFF` | plan-chapter |
| `BRIEF_READY` | generate-chapter |
| `CHAPTER_WRITTEN_NO_REVIEW` | chapter-review |
| `REVIEWED` | publish-chapter |
| `ANOMALY` | qa check |

**书级阶段判定**（`outline.md` frontmatter `workflow_position`）：
- 缺失/空 → 大纲未形成（📝 建议 outline-tingle）
- `outline-tingle-step1-done` → Session 1 完成（🌱）
- `outline-tingle-l1-confirmed` → L1 已确认（🌿）
- `outline-tingle-step2-done` → 大纲形成完成（🌳，可进 plan-chapter）

## 书级前置 + 4-Skill 对称工作流

```
SESSION 0 — 书级大纲形成（首次规划前必跑）
  /outline-tingle
    Session 1：premise → 主题 → L1
    Session 2：L2 → L3 → outline.md (workflow_position=outline-tingle-step2-done)
  改编流由 adaptation-workflow 阶段 0.5 编排（mode="adaptation"）

SESSION 1 — 规划（plan）
  /plan-chapter {N}
    ├── 前置检查 (C0-C9) + 设定快照 + 草稿初始化
    ├── 五更启发式交谈 → 方向卡
    └── Handoff 输出

[HANDOFF] 用户开新会话

SESSION 2 — 生成（generate）
  /generate-chapter {N}
    ├── 写作简报 (mo-writer)
    ├── AI 生成整章 (sensory-writer per-scene + 200字摘要)
    ├── 自动评审 (chapter-review ai-content)
    └── 最多 2 轮 Fix 循环

[USER 轻编辑 — 可选]
SESSION 3 — 人工复审
  /chapter-review {N}（writing mode）

SESSION 4 — 发布（publish）
  /publish-chapter {N}
    ├── 设定合并
    └── 发布前琉璃校验
```

> 原创项目首次规划时，pre-flight-check C9 软阻断检测 `outline.md` L1-L3 实质填充度，未填实则引导 outline-tingle。

## 22 个 Skill 入口

| Skill | 触发词 | 一句话功能 |
|-------|--------|-----------|
| **ask-yiyi** | （会话启动）| 统一入口：会话初始化 + 路由 + QA + 智能推荐 |
| **outline-tingle** | 从零写新书 / 形成大纲 | 书级大纲形成（premise→L1→L2→L3，2 session；original/adaptation 双 mode）|
| **plan-chapter** | 写第X章 | 章节规划（系统管道 + 五更交谈 + handoff）|
| **generate-chapter** | /generate-chapter {N} | AI 生成整章（简报 + per-scene + 评审 + Fix）|
| **chapter-review** | 评审第X章 | 3 mode 评审（writing/ai-content/adaptation）|
| **publish-chapter** | 发布第X章 | 设定合并 + 草稿同步 + 琉璃校验 |
| **adaptation-workflow** | 改编这个作品 | 原作画像 + 阶段 0.5 outline-tingle + 逐章改编循环 |
| **bootstrap-project** | 初始化项目 | 冷启动（批量导入 + 全文逆向分析 + 工件生成）|
| **import-chapter** | 导入章节 | 多格式导入（md/txt/docx/epub）+ 设定扫描 |
| **pre-flight-check** | （系统调用）| C0-C9 就绪检查 + 阻断判定 |
| **settings-manager** | （系统调用）| 设定读取/写入/合并/角色状态 |
| **file-manager** | （系统调用）| 三层文件补齐 |
| **migration-keeper** | （系统调用）| 格式检测 + 兼容性 + 迁移 |
| **mo-writer** | （系统调用）| 7 层写作简报生成 |
| **sensory-writer** | （系统调用）| 感官锚定 AI 章节生成（single/per-scene）|
| **ping-critic** | （系统调用）| 综合评审（心流 + 指纹 + 校对 + 三维）|
| **qing-novelist** | （系统调用）| 12 维启发交谈 + 7 维作者分析 + 8 维书级 grilling |
| **idea-explorer** | （系统调用）| 7 种头脑风暴方法（章节级 + 书级 premise 发散）|
| **voice-sculptor** | （系统调用）| 角色声音实验（生成式/挖掘式）|
| **technique-selector** | （系统调用）| 技法智能匹配 |
| **yin-illustrator** | （系统调用）| 场景视觉设计 + 插画 prompt |
| **fingerprint-discovery** | 指纹分析 | 未知指纹发现 + 形式化 + 入库 |

## 文档导航

- **[用户使用指南.md](用户使用指南.md)** —— 作者视角的完整操作手册（ask-yiyi 入口视角）
- **[CLAUDE.md](CLAUDE.md)** —— Agent 视角的强制规则 + 工作流图
- **[framework/_specs/interaction-spec.md](framework/_specs/interaction-spec.md)** —— Skill 命名/调用/handoff 协议
- **[framework/_specs/skill-template.md](framework/_specs/skill-template.md)** —— Skill 5 必含字段模板
- **[framework/guides/](framework/guides/)** —— 17 篇方法论文档
- **[framework/templates/](framework/templates/)** —— 初始化模板 + 高潮模式库

## 项目结构

```
my_novel/
├── CLAUDE.md                  # 9 条强制规则 + 工作流
├── 用户使用指南.md              # 作者操作手册（ask-yiyi 视角）
├── .claude/skills/            # 22 个 Skill 定义
├── framework/                 # 通用框架（specs/guides/templates）
│   ├── _specs/                # 协议 + 模板
│   ├── guides/                # 方法论 17 篇
│   └── templates/             # 初始化模板 + 高潮模式库
├── reference/                 # 原作存放点（用户上传）
└── novel/                     # 当前小说实例（⚠️ 不在 git 中）
```

## 许可

Apache-2.0
