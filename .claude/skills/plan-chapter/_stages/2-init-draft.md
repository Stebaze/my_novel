# 阶段 2：Init Draft

## 目标

按需初始化草稿目录（首次进入全书时）。单草稿约束下，`novel/_drafts/` 贯穿全书复用，无"新建另一份草稿"语义。

## 执行步骤

```
调 Skill("settings-manager", operation="init-draft")
  → 检查 novel/_drafts/ 存在性
  → 不存在 → 调 file-manager (ensure-novel → ensure-draft) 建空模板+目录
  → 存在 → 直接复用（贯穿全书）
  → 返回 draft_dir = "novel/_drafts/"
```

## 触发条件

- 阶段 0 检查 `novel/_drafts/` 不存在
- 草稿目录存在但工件文件不完整（C3 检查失败 → file-manager ensure-draft 补齐缺失模板/目录）

## 降级

`settings-manager` 不可用 → 🚫 硬阻断——草稿初始化不可跳过。
