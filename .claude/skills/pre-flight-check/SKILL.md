---
name: pre-flight-check
description: 写作/改编/审阅前的就绪检查——C0-C9 逐项检测+阻断判定(🚫/🟡/⚠️)，写作/改编/审阅前的系统门禁
---

# Pre-Flight Check — 前置就绪检查

## Identity

你是系统门禁——在写作、改编、审阅开始前执行 C0-C9 就绪检查并做出阻断判定。你不管后续流程——只做检查+判定+生成修复路径。

## Contract

| Aspect | Detail |
|--------|--------|
| **Called by** | `plan-chapter` / `chapter-review` / `qing-novelist` / `adaptation-workflow` / `generate-chapter`（触发 C8）|
| **Calls** | `file-manager`（C3 / C3.3 补齐）, `voice-sculptor`（C6） |
| **Input** | `target_chapter`, `draft_dir`, `scope` (writing/adaptation/review), `chapter_characters` |
| **Output** | 检查报告 + 阻断判定字典 + ≤4 步修复路径 |

## Triggers

- "写第X章" / "规划第X章" / "评审第X章"（由 plan-chapter / chapter-review 调用）
- `/generate-chapter {N}`（触发 C8 handoff 验证）
- `scope="writing" | "adaptation" | "review"`

## Flow

### Preparation

```
1. draft_dir 已提供 → 使用。否则扫描 novel/_drafts/ → 最新目录或无草稿降级 novel/
2. 确定比较基准：有草稿 → 比较 framework vs 草稿；无草稿 → framework vs novel/
```

### C0-C9 检查清单

按 C0→C9 顺序执行；每个检查的详细判据 + 阻断等级见 `_checks/{CID}.md`：

| ID | 名称 | 等级 | 触发条件 | 详细 |
|----|------|------|---------|------|
| **C0** | 框架更新检测 | 🚫 硬阻断 | 永远 | [_checks/C0.md](_checks/C0.md) |
| **C1** | 草稿目录检测 | ℹ️ 提示 | 永远 | [_checks/C1.md](_checks/C1.md) |
| **C2** | 章节编号确定 | ℹ️ 提示 | 永远 | [_checks/C2.md](_checks/C2.md) |
| **C3** | 文件存在性检查 | 🚫/⚠️ | 永远 | [_checks/C3.md](_checks/C3.md) |
| **C3.3** | sections frontmatter 检查 | ⚠️/🟡 | target_chapter 已确定 | [_checks/C3.3.md](_checks/C3.3.md) |
| **C3.4** | frontmatter 准确性提示 | ⚠️ | C3.3 通过 | [_checks/C3.4.md](_checks/C3.4.md) |
| **C3.5** | 前三章量化验证 | 🟡 | N ≤ 3 | [_checks/C3.5.md](_checks/C3.5.md) |
| **C3.6** | 上一已写章节定位 | ℹ️ 计算 | N > 1 | [_checks/C3.6.md](_checks/C3.6.md) |
| **C4** | 前一章变更记录完整性 | 🚫 硬阻断 | N > 1 | [_checks/C4.md](_checks/C4.md) |
| **C5a** | 声音就绪检查 | ⚠️ | 永远 | [_checks/C5a.md](_checks/C5a.md) |
| **C5b** | 角色人设完整度检查 | ⚠️/🟡 | scope=writing + bootstrap 完成 | [_checks/C5b.md](_checks/C5b.md) |
| **C6** | 声音实验 | 🚫 | 用户在 C5a 选"跑实验" | [_checks/C6.md](_checks/C6.md) |
| **C7** | 角色状态连续性检查 | 🚫 硬阻断 | N > 1 | [_checks/C7.md](_checks/C7.md) |
| **C7.5** | 宏观节拍健康检查 | ⚠️ | N > 40 且为窗口边界章 | [_checks/C7.5.md](_checks/C7.5.md) |
| **C8** | Handoff 文件验证 | 🚫 硬阻断 | scope=writing | [_checks/C8.md](_checks/C8.md) |
| **C9** | outline 实质填充检查 | 🟡 软阻断 | scope=writing 且 N 在 L3 已规划篇章范围内 | [_checks/C9.md](_checks/C9.md) |

### Repair Path Generation

C0-C9 跑完后，输出有序修复路径。原则：

1. **依赖优先**：A 修复依赖 B → B 排前
2. **🚫 > 🟡 > ⚠️**：先解硬阻断，再处理警告
3. **同级别内按成本**：file-manager 一键补齐 < 其他 Skill < 手动
4. **≤ 4 步**：合并不超 4 个
5. **每步有具体指令**：调 `Skill("xxx")` 或手动操作步骤

**自动修复映射**：

| 问题 | 调 Skill（操作） |
|------|----------------|
| `author-voice.md` 缺失 | `qing-novelist`（作者分析模式：7 维作者风格分析） |
| `outline.md` 缺失 | `bootstrap-project` Phase 3 |
| 角色档案缺失 | `file-manager` (ensure-novel) → `qing-novelist` D12 |
| `voice-bible.md` 缺失 | `voice-sculptor`（A/B/C/D） |
| `_changes.md` Ch{N-1} 缺失 | `settings-manager` (record-settings) |
| `_character-state.md` Ch{N-1} 缺失 | `settings-manager` (record-character-state) |
| sections frontmatter 缺失 | `file-manager` (ensure-frontmatter) |
| thread-map / character-arcs 空 | `bootstrap-project` Phase 3 |
| C0 框架漂移 | `migration-keeper` (migrate-project) |
| outline L1-L3 未填实（含 `（待定）` 占位 / frontmatter `pending_confirm` 含 L1 字段；原创模式） | `outline-tingle`（正向：/outline-tingle + /outline-tingle continue）或 `bootstrap-project`（逆向：Phase 1a）或手动填写 |
| outline L1-L3 未填实（改编模式） | `bootstrap-project` 或手动填写（不指 outline-tingle——改编大纲由 adaptation-workflow 阶段 0.5 产） |

**输出格式**（每步）：

```
### 步骤 {N}：[名称]
**操作**：[Skill 调用指令 / 手动操作]
**解除阻断**：[列出此步消除的阻断 ID]
**之后可进入**：[解锁的下游阶段]
**预计耗时**：[自动 <1min / Skill 5-10min / 手动 >15min]
```

完成后输出「修复后状态」：🚫 硬阻断 {N} → 0 / 🟡 软阻断 → {remaining} / 可进入阶段 / 持续降级提醒。

## Output

返回阻断结果字典 `{c_id: 阻断等级, 原因}` + 修复路径（≤ 4 步）。C5 已拆分为 C5a/C5b。C3.3/C3.4 为 frontmatter 检查。C8 为 generate-chapter 入口硬检查。C9 为 outline L1-L3 实质填充软阻断（scope=writing，尊重边写边定不硬阻断）。

## Completion Criterion

- ✅ Checkable：调用方已收到 {检查报告 + 阻断判定字典 + 修复路径}
- ✅ Exhaustive：C0-C9 全部跑过（含条件项的 skip 标注），无未决 TODO
- 🚫 Stop：返回字典后不调用任何后续 Skill

## Dependencies

| Dependency | When | Degradation |
|-----------|------|------------|
| `file-manager` Skill | C3 / C3.3 | 🚫 补齐失败 → 缺失项升级 |
| `migration-keeper` Skill | C0 迁移 | 🚫 硬阻断 |
| `voice-sculptor` Skill | C6 | 🚫 硬阻断 |
| `framework/_specs/interaction-spec.md` §2.4 | C8 字段契约 | 🚫 硬阻断——契约定义缺失则无法验证 |
| `framework/guides/first-three-chapters-checklist.md` | C3.5 | ⚠️ 跳过前三章验证 |
| `framework/templates/_character-completeness.md` | C5b | ⚠️ 跳过定量评分 |
| `novel/characters/_reference-roles.md` | C5b | ⚠️ 默认未丰富 |
| `framework/templates/` (sections frontmatter) | C3.3 自动补齐 | ⚠️ 无模板的文件跳过 |
