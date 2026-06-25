# Framework — 小说写作通用框架

> **定位**：本目录存放不随小说变化的方法论指南和模板。`novel/` 是当前小说的**实例**，`framework/` 是生成实例的**工厂**。

## 目录结构

```
framework/
├── README.md           ← 本文件
├── guides/             ← 方法论文档（阅读参考，不复制到 novel/）
│   ├── qing-conversation-guide.md       启发式交谈方法论
│   ├── narrative-engineering.md         叙事工程：五级大纲体系
│   ├── flow-review-methodology.md       心流评审方法论
│   ├── psychology-guide.md              心理叙事工具箱
│   ├── ai-risk-mitigation.md            AI 写作质量增强
│   ├── ling-detection-methodology.md    AI 指纹检测与校对方法论
│   ├── cn-webnovel-guide.md             中国网文平台指南
│   ├── decision-exploration.md          情节决策探索方法
│   ├── first-three-chapters-checklist.md 前三章验证清单
│   ├── illustration-guide.md            插画叙事策略
│   ├── multi-pov-guide.md               多主角叙事指南
│   ├── voice-experiments.md             角色声音实验方法
│   ├── villain-design-guide.md          反派设计指南
│   ├── draft-system.md                  稿件三层体系文档
│   ├── reference-material.md            参考素材库
│   ├── bootstrap-workflow-guide.md      冷启动工作流指南
│   └── character-enrichment-guide.md    角色人设丰富指南
├── _specs/              ← 架构规范（Skill 模板与交互规范）
│   ├── agent-template.md               Agent 标准结构模板（可选优化手段）
│   ├── skill-template.md               Skill 标准结构模板
│   └── interaction-spec.md             Skill-Skill 交互规范
├── templates/           ← 模板（复制到 novel/ 后填写）
│   ├── project-config.md               项目配置模板
│   ├── notes.md                        写作笔记模板
│   ├── outline.md                      全书大纲模板
│   ├── author-voice.md                 作者文风档案模板
│   ├── voice-bible.md                  叙事声音圣经模板
│   ├── vocabulary-bank.md              个人词汇资产库模板
│   ├── inspiration-log.md              灵感日志模板
│   ├── style-guide.md                  写作风格手册模板
│   ├── technique-library.md            技法素材库模板
│   ├── world/                          世界观模板
│   │   ├── rules.md                    规则体系
│   │   ├── setting.md                  舞台设定
│   │   └── timeline.md                 故事时间线
│   ├── characters/                     角色模板
│   │   ├── _template.md                角色档案模板
│   │   └── _language-fingerprint-template.md  角色语言指纹模板
│   ├── chapters/
│   │   └── _chapter-template.md        章节写作模板
│   ├── _character-completeness.md      角色人设完整度评分模板
│   ├── _reference-roles.md             参考角色映射记录模板
│   ├── _bootstrap-progress.md          冷启动进度追踪模板
│   └── _drafts/                        草稿管理模板
│       ├── _index.md                   草稿会话索引
│       └── session-context.md          跨 Skill 交接文件模板
```

## 初始化新小说

> **自动初始化**：以下步骤已由 `file-manager` Skill 的 `ensure-novel` 操作自动化。在 Claude Code 环境中，调用 file-manager ensure-novel 即可完成相同操作。手动初始化仍可参照以下步骤。

从 framework 模板创建新小说实例的步骤：

### 1. 创建 novel/ 目录

```bash
mkdir -p novel/{world,characters,chapters/_experiments,_drafts,_reference}
```

### 2. 复制模板

```bash
# 核心文件
cp framework/templates/project-config.md novel/
cp framework/templates/notes.md novel/
cp framework/templates/outline.md novel/
cp framework/templates/author-voice.md novel/
cp framework/templates/voice-bible.md novel/
cp framework/templates/vocabulary-bank.md novel/
cp framework/templates/inspiration-log.md novel/
cp framework/templates/style-guide.md novel/
cp framework/templates/technique-library.md novel/

# 世界观
cp framework/templates/world/*.md novel/world/

# 角色（模板保留，实例从 _template 创建）
cp framework/templates/characters/_template.md novel/characters/
cp framework/templates/characters/_language-fingerprint-template.md novel/characters/

# 章节
cp framework/templates/chapters/_chapter-template.md novel/chapters/

# 草稿管理
cp framework/templates/_drafts/_index.md novel/_drafts/
# session-context.md 模板在 framework/templates/_drafts/session-context.md，新建草稿时复制到 {draft}/session-context.md
```

### 3. 填写 project-config.md

这是**第一步必须做的事**。定义：
- 叙事配置（人称/POV/基调/驱动方式）
- 类型配置（主类型/子类型/超自然元素/战斗元素）
- 关系线配置（恋爱线比重/关系模式/情感基调）
- 平台配置（目标平台/每章字数/VIP机制）
- 参考作品（风格基准 + 参考维度）

### 4. 后续填写顺序

| 优先级 | 文件 | 填写时机 |
|--------|------|---------|
| 🔴 立即 | `project-config.md` | Day 1 — 所有 Agent 行为依赖此配置 |
| 🔴 立即 | `notes.md` | Day 1 — session zero 记录 |
| 🟡 写前 | `outline.md` | 开始写作前 |
| 🟡 写前 | `world/rules.md`, `world/setting.md` | 世界观构建时 |
| 🟡 写前 | `world/timeline.md` | 开始写作前 |
| 🟢 写中 | `author-voice.md` | 写完 3-5 章后分析 |
| 🟢 写中 | `voice-bible.md` | 角色声音确立后（~5 章） |
| 🟢 写中 | `style-guide.md` | 风格确立后逐步填充 |
| 🟢 写中 | `technique-library.md` | 分析参考作品后提取 |
| 🔵 持续 | `vocabulary-bank.md` | 写作过程中持续积累 |
| 🔵 持续 | `inspiration-log.md` | 随时记录 |

## 模板自定义

模板是**有观点的起点**，不是不可更改的教条。你可以：
- 添加新字段（如果项目需要模板未覆盖的信息）
- 删除不适用的章节（如果项目不使用多 POV，可删除相关章节）
- 调整注释风格（将 HTML 注释改为更适合自己的格式）

修改后提交到版本控制，以便下一个项目受益。

## 指南与模板的关系

- **guides/** 是知识库——Agent 在写作/评审时**引用**它们，不复制到 novel/
- **templates/** 是骨架——**复制**到 novel/ 后填写为当前小说的实例
- 指南中的方法论通过模板落地为具体文件结构
