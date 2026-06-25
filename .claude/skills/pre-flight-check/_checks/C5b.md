# C5b：角色人设完整度检查

**条件**：scope="writing"，bootstrap 完成后激活

## 执行

1. 对每个出场角色，检查 `characters/{角色名}.md` 存在性 → 不存在 → ⚠️ 提醒
2. 对档案存在的角色，对照 `_character-completeness.md` 模板执行 10 维度评分（0/1/2，0=空 / 1=薄 / 2=完整，总分 20）
3. 维度 4（心理动力结构）对照 `framework/guides/jung-character-framework.md` §10.5
4. 读取 `novel/characters/_reference-roles.md`（如存在）

## 单薄判定

- 总分 < 8 → ⚠️ "角色 [名称] 人设单薄（X/20），建议先丰富再写"
- 维度 3（性格剖面）= 0 且维度 5（语言风格）= 0 → ⚠️ 同上
- 维度 2（角色原型）= 0 → 提示"建议选择至少一个原型作为起点模板"

## 阻断

- 单薄角色 _reference-roles.md 中已有丰富记录 → ✅ 通过（标注"已丰富"）
- 单薄角色无丰富记录 → 🟡 软阻断

## 降级

- `_character-completeness.md` 不存在 → ⚠️ 跳过定量评分，仅基于档案存在性做定性判断
- 角色档案不存在 → 仅 ⚠️ 提醒，不阻断
- `_reference-roles.md` 不存在 → ⚠️ 默认标记为未丰富
