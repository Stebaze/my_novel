---
sections:
  - heading: "## 一、200 字结构化摘要协议"
    skills: [sensory-writer, generate-chapter]
    desc: "per-scene 模式必出字段——10 字段 JSON 块+序列化规则+下游消费方式"
  - heading: "## 二、字段填写规则"
    skills: [sensory-writer]
    desc: "core_event/key_actions/key_dialogue/ending_state/foreshadow_touched 的填写细节"
---

# 200 字结构化摘要协议（per-scene 模式）

> **触发条件**：`sensory-writer` mode="per-scene" 调用时必出
> **消费方**：`generate-chapter` Step 2 写入 `_exchanges/scene-summaries.json`；`chapter-review` ai-content 模式 + `generate-chapter` Step 4 Fix 循环精准定位单场景

## 一、200 字结构化摘要协议

返回 prose 前必须输出 summary_200 JSON 块：

```json
{
  "scene_index": {N},
  "scene_name": "{name}",
  "pov": "{角色}",
  "core_event": "{一句话核心事件}",
  "key_actions": ["{动作1}", "{动作2}"],
  "key_dialogue": ["{对话1}", "{对话2}"],
  "pov_state_change": "{POV 开始到结尾状态变化}",
  "ending_state": "{末尾 POV 状态/位置/高点}",
  "next_link": "{与下场景的连接点}",
  "foreshadow_touched": ["{伏笔 ID 或描述}"]
}
```

**强制规则**：
- **200 字以内**（JSON 序列化后字符数）——这是机器消费的约束
- JSON 块置于 prose 之后，单独代码块包裹，便于下游解析
- 字段缺一视为不完整（per-scene 模式 Completion Criterion 不通过）

## 二、字段填写规则

| 字段 | 规则 |
|------|------|
| `core_event` | 一句话讲清"这个场景发生了什么"——给读者做笔记/供评审用 |
| `key_actions` | 2-4 个关键动作；直接引用 prose 中的具体句子（截短） |
| `key_dialogue` | 2-4 句关键对白；直接截取原文 |
| `pov_state_change` | 一句话描述 POV 角色从场景开始到结尾的状态变化 |
| `ending_state` | 一句话描述末尾 POV 状态/物理位置/情绪高点——**必须能直接衔接 next_link** |
| `next_link` | 一句话描述与下场景的连接点（生成-chapter 拼装后用 ending_state + next_link 检查场景断裂） |
| `foreshadow_touched` | 数组，标记本章触及的伏笔 ID（从简报 §3 伏笔清单或 thread-map §三提取）；可空 |

**下游消费方式**：

```
chapter-review ai-content 模式 → 加载 scene-summaries.json → 5 项机器化校验
  - 3c-AI-1 关键事件落地：scene-summaries.key_actions vs 简报 §3 events
  - 3c-AI-2 场景间连贯：scene N.next_link vs scene N+1.core_event
  - 3c-AI-3 突兀收束：scene N.ending_state 是否在互动中途或情绪高点
  - 3c-AI-4 POV 状态连续：scene N.pov_state_change vs scene N+1 POV 起始态
  - 3c-AI-5 伏笔操作核对：scene-summaries.foreshadow_touched vs 简报 §3 伏笔 + thread-map §三
```
