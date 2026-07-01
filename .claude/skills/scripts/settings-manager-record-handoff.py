#!/usr/bin/env python3
"""
settings-manager record-handoff 脚本化版本（2026-07-01 修复 #1+#7）

验证 12 字段 handoff 契约（含 3 维档案兼容性——subvariant/specialization 可空）。
调用：python3 scripts/settings-manager-record-handoff.py <handoff_path>

示例：
  python3 scripts/settings-manager-record-handoff.py novel/_drafts/_briefs/chapter-2-handoff.md
"""
import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent.parent.parent  # .claude/skills/scripts/ → 仓库根（4 层）
FRAMEWORK = ROOT / "framework"


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


def check_5d_files(style_profile: Dict) -> List[str]:
    """校验 5 维档案对应文件存在性

    文件命名规则（v2.0）：
    - style-bases: {type}.md（无前缀）—— japanese-light-novel-base.md
    - themes: theme-{theme}.md（theme- 前缀）—— theme-daily-life.md
    - styles: {variant}.md（无前缀）—— kuiguannan-style.md
    """
    errors = []
    sp_type = style_profile.get("style_profile_type", "")
    if sp_type:
        type_path = FRAMEWORK / "templates" / "_style-bases" / f"{sp_type}.md"
        if not type_path.exists():
            errors.append(f"基底文件不存在: {type_path}")

    themes = style_profile.get("style_profile_themes", [])
    for t in themes:
        theme_path = FRAMEWORK / "templates" / "_themes" / f"theme-{t}.md"
        if not theme_path.exists():
            errors.append(f"主题文件不存在: {theme_path}")

    variant = style_profile.get("style_profile_variant", "")
    if variant:  # 空字符串合法，不查
        variant_path = FRAMEWORK / "templates" / "_styles" / f"{variant}.md"
        if not variant_path.exists():
            errors.append(f"风格层文件不存在: {variant_path}（降级 ⚠️，5 维评审基线退化为基底默认）")

    # subvariant 嵌入在 variant 文件中，无需单独查
    # specialization 可选
    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 settings-manager-record-handoff.py <handoff_path>")
        sys.exit(1)

    handoff_path = Path(sys.argv[1])
    if not handoff_path.is_absolute():
        handoff_path = ROOT / sys.argv[1]
    handoff_path = handoff_path.resolve()

    if not handoff_path.exists():
        print(f"❌ handoff 文件不存在: {handoff_path}")
        sys.exit(1)

    print(f"=== settings-manager record-handoff 验证 ===")
    print(f"handoff: {handoff_path}")
    print()

    fm = read_yaml_frontmatter(handoff_path)
    if not fm:
        print("❌ frontmatter 解析失败")
        sys.exit(1)

    # 必填字段（2026-07-01 修复 #7：subvariant/specialization 改为可选）
    required = [
        "chapter", "direction", "chapter_file", "character_state",
        "style_profile_type", "style_profile_themes",
        "workflow_position", "resume_command"
    ]
    missing = [f for f in required if not fm.get(f)]
    # variant 必填但允许空字符串
    if "style_profile_variant" not in fm:
        missing.append("style_profile_variant")

    if missing:
        print(f"❌ 必填字段缺失: {missing}")
        sys.exit(1)

    # 检查 chapter 值
    target_chapter = int(re.search(r"chapter-(\d+)-handoff", str(handoff_path)).group(1))
    if int(fm["chapter"]) != target_chapter:
        print(f"❌ chapter={fm['chapter']} ≠ N={target_chapter}")
        sys.exit(1)

    # 检查 path 字段（path 字段默认以 {draft_dir} 为根的相对路径）
    # 从 handoff 路径推断 draft_dir：handoff 总是 _drafts/_briefs/chapter-N-handoff.md
    handoff_parent = handoff_path.parent  # _drafts/_briefs
    if handoff_parent.name == "_briefs":
        draft_dir = handoff_parent.parent  # _drafts
    else:
        draft_dir = handoff_parent

    direction_path = draft_dir / fm["direction"]
    if not direction_path.exists():
        print(f"❌ direction 文件不存在: {direction_path}")
        sys.exit(1)

    character_state_path = draft_dir / fm["character_state"]
    if not character_state_path.exists():
        print(f"❌ character_state 文件不存在: {character_state_path}")
        sys.exit(1)

    # brief 在 plan 阶段可空，generate 阶段必查
    workflow_position = fm.get("workflow_position", "")
    brief = fm.get("brief", "")
    if workflow_position.startswith("generate-") and brief:
        brief_path = draft_dir / brief
        if not brief_path.exists():
            print(f"❌ brief 文件不存在: {brief_path}")
            sys.exit(1)

    # 5 维档案文件存在性
    style_profile = {
        "style_profile_type": fm.get("style_profile_type", ""),
        "style_profile_themes": fm.get("style_profile_themes", []),
        "style_profile_variant": fm.get("style_profile_variant", ""),
        "style_profile_subvariant": fm.get("style_profile_subvariant", ""),
        "style_profile_specialization": fm.get("style_profile_specialization", ""),
    }
    file_errors = check_5d_files(style_profile)

    print("=== 12 字段校验 ===")
    for f in required + ["style_profile_variant"]:
        v = fm.get(f, "")
        print(f"  {f}: {v if v else '(空)'}  ✓")
    print(f"  style_profile_subvariant: {fm.get('style_profile_subvariant', '') or '(空) ✓ 可选'}")
    print(f"  style_profile_specialization: {fm.get('style_profile_specialization', '') or '(空) ✓ 可选'}")

    print()
    print("=== 5 维档案文件存在性 ===")
    if not file_errors:
        print("  ✓ 全部文件存在（subvariant 嵌入在 variant 文件中，specialization 可选）")
    else:
        for e in file_errors:
            print(f"  ⚠️ {e}")

    print()
    print(f"=== 验证结果 ===")
    if file_errors:
        print(f"  ⚠️ 降级通过（5 维档案部分缺失）")
        sys.exit(0)  # 降级不阻断
    else:
        print(f"  ✅ 12 字段契约完整 + 5 维档案全部文件存在")
        sys.exit(0)


if __name__ == "__main__":
    main()
