#!/usr/bin/env python3
"""
fingerprint-tracker 脚本化版本（2026-07-01 修复 #1）

执行 2b-gate 指纹追踪——grep 硬计数（V3/V7/fp5/叙述者解码/抽象情感 5 类别）。
调用：python3 scripts/fingerprint-tracker.py <chapter_md> [output_json]

示例：
  python3 scripts/fingerprint-tracker.py novel/_drafts/chapters/chapter-2.md novel/_drafts/_exchanges/fingerprint-tracker.json
"""
import sys
import re
import json
from pathlib import Path
from typing import Dict, List

ROOT = Path(__file__).resolve().parent.parent.parent.parent  # .claude/skills/scripts/ → 仓库根（4 层）

# 5 类指纹词表
V3_WORDS = ["慢慢", "忽然", "原来", "突然", "不禁", "仿佛", "缓缓", "深深", "似乎", "非常", "然后", "美丽", "壮观"]
V7_PATTERN = re.compile(r"不是[^。]*。[^。]*是")
FP5_PATTERNS = ["他没", "她没", "没问自己", "没意识到", "没在脑子里", "没去想", "没想过"]
NARRATOR_DECODE = ["忽然懂了", "忽然明白", "忽然意识到", "懂了一件事", "忽然就懂"]
ABSTRACT_EMOTION = ["斟酌", "复杂", "难以言喻", "说不清", "意味深长", "不容置疑", "难以察觉"]

# Q1 阈值
THRESHOLD = 3


def extract_prose(text: str) -> str:
    """提取正文区（## 正文 之后到 ## 修订记录 之前），剔除元数据"""
    parts = text.split("## 正文")
    if len(parts) < 2:
        return text
    body = parts[1].split("## 修订记录")[0]
    # 剔除时空标签
    body = re.sub(r"『.*?』", "", body)
    # 剔除场景标题
    body = re.sub(r"### 场景[^\n]*\n", "", body)
    # 剔除水平线
    body = re.sub(r"^---$", "", body, flags=re.MULTILINE)
    return body


def count_fingerprints(prose: str) -> Dict:
    """统计 5 类指纹"""
    v3_count = {w: prose.count(w) for w in V3_WORDS}
    v3_total = sum(v3_count.values())
    v7_count = len(V7_PATTERN.findall(prose))
    fp5_count = {p: prose.count(p) for p in FP5_PATTERNS}
    fp5_total = sum(fp5_count.values())
    decode_count = {p: prose.count(p) for p in NARRATOR_DECODE}
    decode_total = sum(decode_count.values())
    emotion_count = {w: prose.count(w) for w in ABSTRACT_EMOTION}
    emotion_total = sum(emotion_count.values())

    return {
        "v3_words": v3_count,
        "v3_total": v3_total,
        "v7_negation": v7_count,
        "fp5_negation": fp5_count,
        "fp5_total": fp5_total,
        "narrator_decode": decode_count,
        "narrator_decode_total": decode_total,
        "abstract_emotion": emotion_count,
        "abstract_emotion_total": emotion_total,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fingerprint-tracker.py <chapter_md> [output_json]")
        sys.exit(1)

    chapter_path = Path(sys.argv[1])
    if not chapter_path.is_absolute():
        chapter_path = ROOT / sys.argv[1]
    chapter_path = chapter_path.resolve()

    output_path = None
    if len(sys.argv) > 2:
        output_path = Path(sys.argv[2])
        if not output_path.is_absolute():
            output_path = ROOT / sys.argv[2]

    if not chapter_path.exists():
        print(f"❌ chapter file not found: {chapter_path}")
        sys.exit(1)

    text = chapter_path.read_text(encoding="utf-8")
    prose = extract_prose(text)
    chinese_chars = len(re.findall(r"[一-鿿]", prose))
    chinese_punct = len(re.findall(r"[，。！？；：、（）《》「」『』""'']", prose))
    total_words = chinese_chars + chinese_punct

    fingerprints = count_fingerprints(prose)

    # 判定 flag
    v3_flag = fingerprints["v3_total"] >= THRESHOLD
    v7_flag = fingerprints["v7_negation"] >= 1
    fp5_flag = fingerprints["fp5_total"] >= THRESHOLD
    decode_flag = fingerprints["narrator_decode_total"] >= 1
    emotion_flag = fingerprints["abstract_emotion_total"] >= 1

    chapter_flag = any([v3_flag, v7_flag, fp5_flag, decode_flag, emotion_flag])

    print(f"=== fingerprint-tracker (script mode) ===")
    print(f"chapter: {chapter_path}")
    print(f"正文字数: {total_words} (中文字符 {chinese_chars} + 标点 {chinese_punct})")
    print()
    print(f"=== 5 类指纹 ===")
    print(f"  V3 累计: {fingerprints['v3_total']} (阈值 {THRESHOLD})  {'🔴 flag' if v3_flag else '✓'}")
    print(f"  V7 否定排比: {fingerprints['v7_negation']}  {'🔴 flag' if v7_flag else '✓'}")
    print(f"  fp5 否定式: {fingerprints['fp5_total']} (阈值 {THRESHOLD})  {'🔴 flag' if fp5_flag else '✓'}")
    print(f"  叙述者解码: {fingerprints['narrator_decode_total']}  {'🔴 flag' if decode_flag else '✓'}")
    print(f"  抽象情感: {fingerprints['abstract_emotion_total']}  {'🔴 flag' if emotion_flag else '✓'}")
    print()
    print(f"=== 判定 ===")
    print(f"  chapter_flag: {chapter_flag}")

    # 输出 JSON
    output = {
        "chapter_path": str(chapter_path),
        "word_count": {
            "chinese_chars": chinese_chars,
            "chinese_punct": chinese_punct,
            "total": total_words,
        },
        "fingerprints": fingerprints,
        "flags": {
            "v3": v3_flag,
            "v7": v7_flag,
            "fp5": fp5_flag,
            "narrator_decode": decode_flag,
            "abstract_emotion": emotion_flag,
            "chapter": chapter_flag,
        },
        "threshold": THRESHOLD,
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  → 写入 {output_path}")

    print(json.dumps(output, ensure_ascii=False, indent=2))
    sys.exit(1 if chapter_flag else 0)


if __name__ == "__main__":
    main()
