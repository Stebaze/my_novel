## 关联 Issue

- 关联（必填）：#（填 issue 编号；如无则说明）
- 阻塞 / 被阻塞：列出相关 issue

## 改动类型

勾选所有适用项：

- [ ] 新增 Skill（`.claude/skills/{name}/SKILL.md`）
- [ ] 修改现有 Skill（`.claude/skills/{name}/SKILL.md`）
- [ ] 文档（`README.md` / `用户使用指南.md` / `CLAUDE.md` / `framework/guides/` / `framework/_specs/`）
- [ ] 框架模板（`framework/templates/`）
- [ ] Bug 修复
- [ ] 重构（不影响对外行为）

## 改动摘要

用 1-3 句话说明这次改动的核心：

- 改了什么：
- 为什么改：
- 影响范围（哪些 Skill 会被影响、ask-yiyi 路由是否需要更新、用户操作是否变化）：

## 测试说明

- [ ] 我已在本地验证了改动
- [ ] 我已更新相关 Skill 的 `SKILL.md`（description / 触发词 / 工件列表）
- [ ] 我已更新 `framework/SKILLS.md` 或 `CLAUDE.md`（如适用）
- [ ] 我已添加 / 更新 `framework/guides/` 下的方法论文档（如适用）

具体测试步骤（给 reviewer 复现用）：

1.
2.
3.

## 兼容性

- [ ] 向后兼容（不影响现有项目）
- [ ] 破坏性变更（详见下方）

### 破坏性变更详情（如适用）

- 影响的命令 / Skill：
- 影响的工件 / 文件格式：
- 迁移方案：

## 回退方案

如何回退这次改动？是否需要 `migration-keeper` 做格式迁移？

## 检查清单

- [ ] commit message 符合仓库约定（中文 `feat/fix/docs/refactor/...` 格式）
- [ ] 没有提交 token / 凭据 / `novel/` 实例内容
- [ ] 没有引入新依赖 / 工具链变更
- [ ] 已和现有 Skill 命名 / 协议（`framework/_specs/interaction-spec.md`）保持一致
