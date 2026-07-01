# 作者风格档案索引（minimal stub）

> **本目录角色**：**可选 enrich**——`project-config.md` 字段 `作家` 指定具体作者时，sensory-writer 加载本目录对应档案替代 fallback 风格层。**基底不变**（仍走 `chinese-webnovel-base`）。
>
> **目录状态**：`.gitignore` 规则 `profiles/authors/*` 隔离——具体作者档案**不进入版本管理**（版权隔离）。
>
> **项目默认风格**（git tracked，fresh clone 即用）：见 [`framework/templates/_defaults/default-style.md`](../../framework/templates/_defaults/default-style.md)。**不依赖本目录**——`作家=""` 时 sensory-writer 走 style_profile 3 维 fallback（基底+主题+风格 fallback）即可正常生成。

---

## 档案命名与结构

- **命名**：文件按作者名命名（如 `{author-name}.md`）—— 调用方按 `project-config.md` 字段 `作家` 匹配
- **作者档案应包含的维度**（v3.0 模板）：
  1. 叙述者声音肖像（语调/幽默机制/情感距离）
  2. 情节设计模式（驱动类型/冲突偏好/高潮模式/情节模板）
  3. 关系设计模式（关系类型/关系组合模板/推进节奏）
  4. 常用技法清单（开头/桥段/断章/事件展开/特殊技法）
  5. 世界观设计风格（构建方式/规则密度/社会结构）
  6. 大纲模板（全书结构/章节模板/节奏模板/信息释放节奏）
  7. 语言指纹（句长/词汇/标点/比喻特征）
- **作者档案 vs fallback 风格层**：作者档案替代 fallback（决策 7）；**基底保持不变**

## 加载链

```
作家="" → 不加载 profiles/authors/ → 走 style_profile 3 维 fallback（git tracked）
作家="具体作者" → 加载 profiles/authors/{作者}.md v3.0 → 替代 fallback 风格层（基底不变）
作家档案缺失 → 降级到 style_profile 3 维 fallback（不阻断）
```

## 何时创建作者档案

- 用户希望**指定具体作者**仿写其风格时 → 调 `qing-novelist`（作者分析模式：7 维分析流程）→ 落盘到本目录
- 用户希望**丰富某一作者的风格细节**（override 默认 fallback）→ 同上路径
- 缺失时无需创建——`作家=""` 走 fallback 风格层已可生成

## 排除原则（编辑本目录时遵守）

- ❌ 不在本目录文件中列入"作者对照矩阵""跨作家基线""典型代表作品"等内容——具体作者姓名+具体作品名是版权敏感素材，仅在本地未跟踪档案中保留，不出现在 git tracked 文件
- ❌ 不在 git tracked 文件（含 `_index.md`、spec 文档、template 注释）中点名具体作家或具体作品
- ✅ git tracked 文件可使用风格/题材/体裁等通用描述（如"日轻校园吐槽风格""中国网文系统流""多女主单恋落败关系模式"）——这些是抽象风格层，非具体作者分析
- ✅ fallback 通用风格层（`framework/templates/_styles/*-style-fallback.md`）的内容是**抽象后**的 3 块 fallback（叙述态度+域词+桥段），不含具体作品分析——可安全 git 跟踪
- ✅ 项目默认风格 spec（`framework/templates/_defaults/default-style.md`）用通用风格名/题材名描述默认 combo——不点名具体作家
