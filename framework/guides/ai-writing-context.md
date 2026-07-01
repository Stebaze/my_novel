---
sections:
  - heading: "## AI 写作常见问题"
    agents: [human-reviewer]
    desc: "5 类常见问题的背景说明"
metadata:
  type: human-background
  audience: human-reviewer (项目作者/编辑)
  loaded_by: 无（人读，不入任何 skill 加载链）
---

# AI 写作背景说明（人读）

> **本文件不进入任何 Skill 的加载链**——给项目作者/编辑提供背景知识。

---

## AI 写作常见问题

AI 生成的文本有 5 类常见问题（读者下意识感到「不像人写的」）：

- **过度平滑**——句子长度均匀、过渡词密集、没有破句
- **声音均化**——超过 10 章后角色说话方式趋同
- **合理偏置**——对话总选「最合理的回答」而非「最有趣的回答」
- **语境衰减**——伏笔揭示时失去埋入时的气氛和措辞
- **叙述者闯入**——叙述者解码角色意图（用抽象情感标签命名语气、破折号插入态度旁白、引导内放入角色未说出口的态度转述）

5 类的共同根因：AI 被训练为「清晰地传达信息」，不信任读者能自己推理。

详见 [`ai-writing-dna.md`](ai-writing-dna.md)（生成端如何避免）/ [`ai-fingerprint-checklist.md`](ai-fingerprint-checklist.md)（评审端如何检测）。
