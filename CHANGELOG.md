# Changelog

All notable changes to my_novel will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-25

### Added
- 21 个 Claude Code Skill 协作体系（plan / generate / review / publish 全链路）
- ask-yiyi 统一入口（取代 project-memory）：会话初始化 + 路由 + QA + 智能推荐
- 4-Skill 对称架构（plan → handoff → generate → review → publish）
- 三层稿件体系（原稿 / 草稿 / 正式稿）
- 设定时间线管理（章节锚定 + 向前扫描 + 冲突分级）
- AI 指纹检测 + 心流五维 18 项评审
- AI 生成整章模式（最多 2 轮 Fix 循环）
- 改编工作流（原作画像 + 逐章改编循环）
- 冷启动工作流（批量导入 + 全文逆向分析 + 工件生成）
- 17 篇方法论指南 + 初始化模板库
- Apache-2.0 许可证
- CHANGELOG.md（v1.0 首发）
- GitHub Issue / PR 模板

### Changed
- 项目结构从单 session 长流程重构为 4 session 短流程
- 用户手册视角从"按 Skill walkthrough"重构为"ask-yiyi 入口视角"
- README 强调 ask-yiyi 统一入口 + 状态机智能建议
- 项目许可证从 MIT 切换到 Apache-2.0

[1.0.0]: https://github.com/Stebaze/my_novel/releases/tag/v1.0.0
