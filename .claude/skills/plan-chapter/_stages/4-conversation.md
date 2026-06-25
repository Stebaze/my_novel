# 阶段 4：Heuristic Conversation

## 目标

调 `qing-novelist` Skill 进行 12 维启发式交谈，产出方向卡 `_briefs/chapter-{N}-direction.md`。

## 执行步骤

```
调 Skill("qing-novelist")
  → 五更加载到当前会话，与作者进行启发式交谈
  → 传递数据：
      ├── 阶段 1 的设定快照（settings_snapshot）
      ├── 阶段 1 的角色状态快照（character_states，N>1 时）
      ├── 阶段 3 的探索卡路径（exploration_file，如有）
      ├── [R8] 阶段 0 preflight-check C5b 标记的 thin_characters
      └── 新卷首章时默认激活 D0b（本卷设计概览），子选项 f+g 为高潮+宏观节拍规划
  → 交谈中调 Agent(ping-critic) 做琉璃校验
  → 产出：_briefs/chapter-{N}-direction.md
  → 用户确认方向
```

## 五更内部职责

- Step 1：自行读取 `_character-state.md` 确认状态可用
- Step 2：如 `exploration_file` 存在，优先消费探索卡方向作为交谈起点
- 12 维启发式：按需激活对应维度，D0b（卷设计）/ D0c（章设计）/ D12（角色人设丰富）等
- 调 `ping-critic` 做心流校验 + 设定一致性校验

## 输出

`_briefs/chapter-{N}-direction.md`（必含：方向选择 / 出场角色 / 关键节拍 / 设定更新 / 风险标注）

## 降级

`qing-novelist` 不可用 → 🚫 硬阻断——方向卡必须产出。
