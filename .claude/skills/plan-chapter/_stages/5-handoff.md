# 阶段 5：Handoff（+ Present）

> **核心改造点**：阶段 5 在 4-Skill 对称架构下**只写 handoff** 并退出；mo / yin / 5c 全部移到 generate-chapter Session 2 执行。
>
> **好处**：
> - 规划阶段控制在 1 个会话内（避免单 session 长流程的上下文衰减）
> - mo 简报生成与 sensory 章节生成紧耦合（共享 brief 上下文）
> - 5c 评审改由 generate-chapter 内部自动触发

---

## Part A：执行步骤

### 写 handoff

#### 执行步骤

1. **准备 handoff 8 字段契约**（参见 `framework/templates/chapter-handoff-template.md`）：

   ```
   chapter: N
   direction: _briefs/chapter-{N}-direction.md（阶段 4 产出）
   brief: ""（空——generate-chapter 阶段 1 补生成）
   chapter_file: chapters/chapter-{N}.md
   character_state: _character-state.md（settings-manager 提供路径）
   style_profile: author-voice.md
   workflow_position: "plan-step5-handoff"
   resume_command: "/generate-chapter {N}"
   ```

2. **调 `Skill("settings-manager", operation="read-character-state")`** → 获取最新角色状态快照路径 → 填入 `character_state` 字段。失败 → 🚫 硬阻断。

3. **调 `Skill("settings-manager", operation="record-handoff")`** → 落盘 handoff 文件：
   - 路径：`{draft_dir}/_briefs/chapter-{N}-handoff.md`
   - frontmatter 必含：`format_version` / `produced_by: "settings-manager"` / `produced_at` / `chapter` / 8 字段
   - 缺失或字段无效 → generate-chapter C8 入口硬阻断

4. **跳到 Part B**（handoff 提示 + 退出）

---

## Part B：Present（最终呈现 + 退出）

```
呈现 handoff 摘要：
  - 章节号：Ch{N}
  - 方向卡：{draft_dir}/_briefs/chapter-{N}-direction.md
  - 简报：待 generate-chapter 阶段 1 补生成
  - 角色状态：{draft_dir}/_character-state.md
  - 文风档案：{draft_dir}/author-voice.md
  - 续跑命令：/generate-chapter {N}

提示用户：
  "Ch{N} 规划完成。Session 1 结束。

   下一步：在新会话中输入 /generate-chapter {N}
   - pre-flight-check C8 将验证 handoff 存在
   - Session 2 内完成简报生成 + 章节 AI 生成 + 自动评审 + 最多 2 轮 Fix 循环

   复制以下提示到新会话：
   ┌─────────────────────────────────────────────┐
   │ 继续 Ch{N} 写作——handoff 如下：              │
   │ chapter: {N}                                │
   │ direction: _briefs/chapter-{N}-direction.md │
   │ style: author-voice.md                     │
   │ resume: /generate-chapter {N}              │
   └─────────────────────────────────────────────┘"
```

---

## 退出

- 呈现 handoff 提示后**不继续调用任何 Skill**——等用户开新会话输入 `/generate-chapter {N}`

## 产出物

- `{draft_dir}/_briefs/chapter-{N}-handoff.md`（8 字段契约完整）
