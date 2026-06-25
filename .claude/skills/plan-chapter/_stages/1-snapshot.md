# 阶段 1：Settings Snapshot

## 目标

获取截止 Ch{N-1} 的设定合并视图 + 角色状态快照。

## 执行步骤

```
1. 调 Skill("settings-manager", operation="read-settings")
   → 获取截止 Ch{N-1} 的设定合并视图（5-8 行合并视图）

2. 调 Skill("settings-manager", operation="read-character-state")（N > 1 时）
   → 获取出场角色状态快照（9 维度 + 章末位置锚点）

3. 如需初始化草稿 → 调 Skill("settings-manager", operation="init-draft")
   → 自动调 file-manager (ensure-novel → ensure-draft)
```

## 新卷首章感知

如本章为新卷首章 → 激活宏观节拍规划提示：

1. 读 `thread-map.md` §六（宏观节拍追踪）→ 如已有本卷规划则跳过
2. 如本卷尚未划分窗口 → 提示用户 "新卷开始了，是否进行宏观节拍规划？"
   - 是 → 在阶段 4 启发式交谈中激活宏观节拍规划子选项
   - 否 → 跳过
3. [bootstrap 感知] 如 `outline.md` L2 有条目标记为"暂缓确认"（来自 bootstrap Phase 3 暂缓项）：
   - 通知用户 "大纲显示这可能是第 X 卷的开始。Bootstrap 检测到的边界是 Ch{N}，但尚未确认。是否确认此边界并开始规划，还是调整？"

## 输出

`settings_snapshot`（5-8 行合并视图）+ `character_states`（出场角色状态）+ `draft_dir`。
