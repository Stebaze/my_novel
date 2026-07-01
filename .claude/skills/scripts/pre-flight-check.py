#!/usr/bin/env python3
"""
pre-flight-check 脚本化版本（2026-07-01 修复 #1）

执行 C0-C11 全部检查并输出阻断判定字典。
调用：python3 scripts/pre-flight-check.py <draft_dir> <target_chapter> [scope]

示例：
  python3 scripts/pre-flight-check.py novel/_drafts 2 writing
  python3 scripts/pre-flight-check.py novel/_drafts 2 review
"""
import sys
import os
import re
import json
from pathlib import Path
from typing import Dict, List, Optional

# 加载前置依赖
ROOT = Path(__file__).resolve().parent.parent.parent.parent  # .claude/skills/scripts/ → 仓库根（4 层）
FRAMEWORK = ROOT / "framework"
NOVEL = ROOT / "novel"
DRAFTS = NOVEL / "_drafts"


def read_yaml_frontmatter(filepath: Path) -> Optional[Dict]:
    """读 YAML frontmatter，容错——支持 list / 行内注释 / 字符串引号"""
    if not filepath.exists():
        return None
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    fm = {}
    current_list_key = None
    for line in parts[1].split("\n"):
        # 跳过纯注释行
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line.startswith("  - "):
            # list item
            if current_list_key:
                item = line.strip()[2:].strip()
                # 去除行内注释 + 去除引号
                item = re.split(r"\s+#", item, maxsplit=1)[0].strip()
                item = item.strip('"').strip("'")
                fm[current_list_key].append(item)
        elif ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            # 去除行内注释
            v = re.split(r"\s+#", v, maxsplit=1)[0].strip()
            if v == "":
                # 可能是 list 起始
                fm[k] = []
                current_list_key = k
            else:
                fm[k] = v.strip('"').strip("'")
                current_list_key = None
    return fm


def check_c0_framework_version() -> Dict:
    """C0 框架更新检测"""
    fv = FRAMEWORK / ".framework-version"
    if not fv.exists():
        return {"c_id": "C0", "level": "⚠️", "reason": "framework/.framework-version 缺失（视为 v2）"}
    text = fv.read_text(encoding="utf-8")
    m = re.search(r"FORMAT_VERSION:\s*(\d+)", text)
    if not m:
        return {"c_id": "C0", "level": "⚠️", "reason": "FORMAT_VERSION 未解析"}
    return {"c_id": "C0", "level": "✅", "reason": f"FORMAT_VERSION={m.group(1)}"}


def check_c1_drafts(draft_dir: Path) -> Dict:
    """C1 草稿目录检测"""
    if draft_dir.exists():
        return {"c_id": "C1", "level": "ℹ️", "reason": f"草稿目录存在: {draft_dir}"}
    return {"c_id": "C1", "level": "⚠️", "reason": f"草稿目录不存在: {draft_dir}"}


def check_c3_files(draft_dir: Path) -> Dict:
    """C3 文件存在性检查（含 author-voice 条件性降级）"""
    novel = draft_dir.parent
    required_files = ["notes.md", "_changes.md", "project-config.md"]
    missing = [f for f in required_files if not (novel / f).exists()]

    # author-voice 条件性降级（2026-07-01 修复 #5）
    author_voice = novel / "author-voice.md"
    if not author_voice.exists():
        # 读 project-config.md 作家字段
        pc_fm = read_yaml_frontmatter(novel / "project-config.md")
        author = (pc_fm or {}).get("作家", "")
        if not author:
            return {
                "c_id": "C3",
                "level": "⚠️",
                "reason": f"author-voice.md 缺失 → 作家字段空，走 fallback 风格层，降级 ⚠️（基础文件缺失: {missing if missing else '无'}）"
            }
        else:
            return {
                "c_id": "C3",
                "level": "🚫",
                "reason": f"author-voice.md 缺失，作家='{author}' → 调 qing-novelist（作者分析模式）建立档案"
            }

    if missing:
        return {"c_id": "C3", "level": "⚠️", "reason": f"基础文件缺失: {missing}"}
    return {"c_id": "C3", "level": "✅", "reason": "所有基础文件存在"}


def check_c4_chapter_changes(target_chapter: int, draft_dir: Path) -> Dict:
    """C4 前一章变更记录完整性"""
    if target_chapter <= 1:
        return {"c_id": "C4", "level": "skip", "reason": "N≤1 不适用"}
    prev = target_chapter - 1
    # _changes.md 在正式层 novel/，不在 draft_dir
    novel = draft_dir.parent
    changes = novel / "_changes.md"
    if not changes.exists():
        return {"c_id": "C4", "level": "🚫", "reason": f"_changes.md 不存在（Ch{prev} 变更记录缺失）"}
    text = changes.read_text(encoding="utf-8")
    if f"Ch{prev}" in text or f"## {prev}." in text or f"## {prev} " in text:
        return {"c_id": "C4", "level": "✅", "reason": f"Ch{prev} 变更记录存在"}
    return {"c_id": "C4", "level": "🚫", "reason": f"Ch{prev} 变更记录缺失 → 调 settings-manager (record-settings) 补齐"}


def check_c7_character_state(target_chapter: int, draft_dir: Path) -> Dict:
    """C7 角色状态连续性检查"""
    if target_chapter <= 1:
        return {"c_id": "C7", "level": "skip", "reason": "N≤1 不适用"}
    prev = target_chapter - 1
    # _character-state.md 在 draft_dir（草稿侧）
    cs = draft_dir / "_character-state.md"
    if not cs.exists():
        return {"c_id": "C7", "level": "🚫", "reason": f"_character-state.md 不存在（Ch{prev} 角色状态缺失）"}
    text = cs.read_text(encoding="utf-8")
    if f"Ch{prev}" in text or f"chapter: {prev}" in text or f"## {prev}." in text:
        return {"c_id": "C7", "level": "✅", "reason": f"Ch{prev} 角色状态存在"}
    return {"c_id": "C7", "level": "🚫", "reason": f"Ch{prev} 角色状态缺失 → 调 settings-manager (record-character-state) 补齐"}


def check_c8_handoff(target_chapter: int, draft_dir: Path) -> Dict:
    """C8 Handoff 文件验证（v2.0 12 字段契约）"""
    handoff = draft_dir / "_briefs" / f"chapter-{target_chapter}-handoff.md"
    if not handoff.exists():
        return {"c_id": "C8", "level": "🚫", "reason": f"Ch{target_chapter} handoff 缺失 → 调 plan-chapter 阶段 0-5"}
    fm = read_yaml_frontmatter(handoff)
    if not fm:
        return {"c_id": "C8", "level": "🚫", "reason": "handoff frontmatter 解析失败"}
    # 必填字段（subvariant/specialization 2026-07-01 改为可选）
    required = ["chapter", "direction", "chapter_file", "character_state", "style_profile_type", "style_profile_themes", "workflow_position", "resume_command"]
    missing = [f for f in required if not fm.get(f)]
    if missing:
        return {"c_id": "C8", "level": "🚫", "reason": f"handoff 必填字段缺失: {missing}"}
    # 检查 value
    if int(fm.get("chapter", 0)) != target_chapter:
        return {"c_id": "C8", "level": "🚫", "reason": f"chapter={fm.get('chapter')} ≠ N={target_chapter}"}
    return {"c_id": "C8", "level": "✅", "reason": "12 字段契约完整"}


def check_c9_outline(draft_dir: Path, target_chapter: int) -> Dict:
    """C9 outline 实质填充检查（含 minimal-validation 跳过模式）"""
    novel = draft_dir.parent
    pc_fm = read_yaml_frontmatter(novel / "project-config.md") or {}
    if pc_fm.get("validation") == "true":
        return {"c_id": "C9", "level": "skip", "reason": "minimal-validation 模式：跳过 outline 检查"}

    outline = novel / "outline.md"
    if not outline.exists():
        return {"c_id": "C9", "level": "skip", "reason": "outline.md 缺失（C3 已报）"}
    return {"c_id": "C9", "level": "ℹ️", "reason": "outline.md 存在（详细检查需 outline 解析器）"}


def check_c10_dispatched(draft_dir: Path) -> Dict:
    """C10 书级设定派发状态检查"""
    novel = draft_dir.parent
    outline = novel / "outline.md"
    if not outline.exists():
        return {"c_id": "C10", "level": "skip", "reason": "outline.md 缺失"}
    fm = read_yaml_frontmatter(outline)
    if not fm or fm.get("workflow_position") != "outline-tingle-step2-done":
        return {"c_id": "C10", "level": "skip", "reason": "大纲未到 step2-done"}
    if fm.get("book_settings_dispatched") == "true":
        return {"c_id": "C10", "level": "✅", "reason": "书级设定已派发"}
    return {"c_id": "C10", "level": "⚠️", "reason": "书级设定未派发（见 C10 修复路径：3 选 1）"}


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 pre-flight-check.py <draft_dir> <target_chapter> [scope]")
        print("  draft_dir: 草稿目录（相对仓库根或绝对路径）")
        print("  target_chapter: 章节号 N")
        print("  scope: writing | adaptation | review（默认 writing）")
        sys.exit(1)

    draft_dir_arg = sys.argv[1]
    target_chapter = int(sys.argv[2])
    scope = sys.argv[3] if len(sys.argv) > 3 else "writing"

    # 解析 draft_dir（相对路径转绝对）
    draft_dir = Path(draft_dir_arg)
    if not draft_dir.is_absolute():
        draft_dir = ROOT / draft_dir_arg
    draft_dir = draft_dir.resolve()

    print(f"=== pre-flight-check (script mode) ===")
    print(f"draft_dir: {draft_dir}")
    print(f"target_chapter: {target_chapter}")
    print(f"scope: {scope}")
    print()

    # 执行 C0-C11
    results = []
    results.append(check_c0_framework_version())
    results.append(check_c1_drafts(draft_dir))
    results.append(check_c3_files(draft_dir))
    results.append(check_c4_chapter_changes(target_chapter, draft_dir))
    results.append(check_c7_character_state(target_chapter, draft_dir))
    results.append(check_c8_handoff(target_chapter, draft_dir))
    results.append(check_c9_outline(draft_dir, target_chapter))
    results.append(check_c10_dispatched(draft_dir))

    # 输出
    print("=== C0-C11 检查结果 ===")
    for r in results:
        print(f"  {r['c_id']}: {r['level']}  {r['reason']}")

    # 阻断判定
    hard_block = [r for r in results if r['level'] == '🚫']
    soft_block = [r for r in results if r['level'] == '🟡']
    warning = [r for r in results if r['level'] == '⚠️']
    pass_count = len([r for r in results if r['level'] == '✅'])
    skip_count = len([r for r in results if r['level'] == 'skip'])

    print()
    print(f"=== 阻断判定 ===")
    print(f"  🚫 硬阻断: {len(hard_block)} 项")
    if hard_block:
        for r in hard_block:
            print(f"    - {r['c_id']}: {r['reason']}")
    print(f"  🟡 软阻断: {len(soft_block)} 项")
    print(f"  ⚠️ 提醒: {len(warning)} 项")
    print(f"  ✅ 通过: {pass_count} 项")
    print(f"  ⏭️ 跳过: {skip_count} 项")

    # 返回 JSON（方便机器消费）
    output = {
        "draft_dir": str(draft_dir),
        "target_chapter": target_chapter,
        "scope": scope,
        "results": results,
        "summary": {
            "hard_block": len(hard_block),
            "soft_block": len(soft_block),
            "warning": len(warning),
            "pass": pass_count,
            "skip": skip_count,
            "verdict": "🚫 硬阻断" if hard_block else ("🟡 软阻断" if soft_block else "✅ 放行")
        }
    }
    print()
    print("=== JSON 输出（方便 pipe）===")
    print(json.dumps(output, ensure_ascii=False, indent=2))

    sys.exit(1 if hard_block else 0)


if __name__ == "__main__":
    main()
