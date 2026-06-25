# 阶段 3：[条件] Brainstorm

> 当作者无方向/卡住时激活。**非必选**——已有明确方向可跳过。

## 触发条件（任一满足即激活）

- 阶段 0 路由中 `need_brainstorming=true`
- 阶段 0 路由中 `exploration_stale=true`
- 作者在阶段 1 期间表示"还是没有方向"
- 用户主动要求"先头脑风暴再规划"
- `thread-map.md` 中本章的规划标记为"待定"或空白（可选触发——向用户确认是否需要）

## 执行步骤

1. **收集上下文**：

   ```
   ├── 阶段 0/1 的 pre-flight-check 结果 + settings-manager 设定快照
   ├── 从 notes.md 提取作者最近的创作状态
   ├── 从 thread-map.md（如存在）提取当前可激活的线程/伏笔
   └── 作者自己表达的困境描述（如有）
   ```

2. **调 `Skill("idea-explorer")`**：

   ```
   传入参数：
     chapter={N}
     draft_dir={draft_dir}
     context_snapshot={
       设定摘要（来自 settings-manager 的 5-8 行合并视图）,
       outline_position（本章在大纲中的定位）,
       available_threads（支线/伏笔/弧光状态摘要）,
       character_states（出场角色状态摘要）,
       author_frustration（用户表达的困境描述，如有）,
       existing_exploration（_briefs/chapter-{N}-exploration.md 路径，stale 重跑时传入）
     }
   ```

3. **思源执行 7 步**：准备 → 发散生成 → 轻量收敛 → 写探索卡 → 产出 `_briefs/chapter-{N}-exploration.md`

4. **检查产出**：
   - 探索卡存在且方向数 ≥ 3 → ✅ 通过
   - 探索卡不存在或方向数 < 3 → ⚠️ 警告"头脑风暴产出较少，部分材料交接给五更"，继续，不阻断

5. **传递到阶段 4**：探索卡路径 → 作为额外参数传递给 qing-novelist，标记 `exploration_completed=true`

## 降级

`idea-explorer` Skill 不可用 → ⚠️ 标注 "思源不可用，直接进入阶段 4" → 跳过阶段 3 → 继续阶段 4。
