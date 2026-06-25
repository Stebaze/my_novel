# 阶段 2：Init Draft

## 目标

按需初始化草稿目录（首次进入 / 用户明确要求新建草稿）。

## 执行步骤

```
调 Skill("settings-manager", operation="init-draft")
  → force_new=false 时扫描最新草稿复用
  → 新建走 file-manager (ensure-novel → ensure-draft)
  → 更新 _index.md
  → 返回 draft_dir
```

## 触发条件

- 阶段 0 扫描 `novel/_drafts/` 无结果
- 用户明确指令 "新建草稿"
- 草稿目录存在但文件不完整（C3 检查失败）

## 降级

`settings-manager` 不可用 → 🚫 硬阻断——草稿初始化不可跳过。
