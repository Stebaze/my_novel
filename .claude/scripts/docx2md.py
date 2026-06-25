#!/usr/bin/env python3
"""
Convert .docx novel manuscript to per-chapter .md files.

Detects chapter boundaries via heading patterns (第X章, Chapter X)
and splits the document into individual markdown files.

Usage:
    python3 docx2md.py <input.docx> [--output-dir <dir>] [--start-num <N>]
"""

import argparse
import os
import re
import sys
from pathlib import Path

try:
    from docx import Document
except ImportError:
    sys.exit("ERROR: python-docx not installed. Run: pip install python-docx")

# ---------------------------------------------------------------------------
# Chinese numeral → integer conversion (supports 1–99)
# ---------------------------------------------------------------------------
_CN_DIGITS = {
    "零": 0, "一": 1, "二": 2, "三": 3, "四": 4,
    "五": 5, "六": 6, "七": 7, "八": 8, "九": 9,
    "十": 10,
}


def _cn_to_int(raw: str) -> int | None:
    """Convert a pure-Chinese-numeral string to int.  Returns None on failure."""
    s = raw.strip()
    if not s:
        return None
    # e.g. "十一" → 11, "二十" → 20, "三十五" → 35
    if s in _CN_DIGITS:
        return _CN_DIGITS[s]
    if s.startswith("十") and len(s) == 2:  # 十X → 1X
        return 10 + _CN_DIGITS.get(s[1], 0)
    if s.endswith("十") and len(s) == 2:  # X十 → X0
        return _CN_DIGITS.get(s[0], 0) * 10
    if len(s) == 3 and s[1] == "十":  # X十Y → XY
        return _CN_DIGITS.get(s[0], 0) * 10 + _CN_DIGITS.get(s[2], 0)
    return None


# ---------------------------------------------------------------------------
# Chapter-boundary regex
# ---------------------------------------------------------------------------
# Matches lines whose primary content is a chapter heading.
# Group 1 = optional markdown heading prefix (# ), group 2 = number string
_CHAPTER_RE = re.compile(
    r"^(#{1,3}\s*)?第\s*([零一二三四五六七八九十百千\d]+)\s*章\s*$"
)

_ARABIC_CHAPTER_RE = re.compile(
    r"^(#{1,3}\s*)?Chapter\s+(\d+)\s*$", re.IGNORECASE
)


def _detect_chapter_number(line: str) -> int | None:
    """Return chapter number (1-based) if *line* is a chapter heading."""
    line = line.strip()
    m = _CHAPTER_RE.match(line)
    if m:
        num_str = m.group(2)
        if num_str.isdigit():
            return int(num_str)
        return _cn_to_int(num_str)
    m = _ARABIC_CHAPTER_RE.match(line)
    if m:
        return int(m.group(2))
    return None


# ---------------------------------------------------------------------------
# Paragraph extraction
# ---------------------------------------------------------------------------

def _extract_paragraphs(doc: Document) -> list[str]:
    """Extract text paragraphs from a python-docx Document, preserving blank-line separators."""
    paragraphs: list[str] = []
    for para in doc.paragraphs:
        text = para.text.rstrip()
        style = para.style.name if para.style else ""
        # Treat empty paragraphs / scene-break indicators as blank-line separators
        if not text:
            paragraphs.append("")
            continue
        # If the paragraph style is a heading, normalize to plain text heading
        if "Heading" in style or "heading" in style:
            text = text.strip()
            if not text.startswith("#"):
                # Try to detect if it looks like a chapter heading already
                pass
        paragraphs.append(text)
    return paragraphs


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def convert_docx(
    input_path: str,
    output_dir: str,
    start_num: int | None = None,
) -> list[dict]:
    """
    Convert *input_path* (.docx) into per-chapter .md files under *output_dir*.

    Returns a list of dicts: { chapter_num, filename, word_count, char_count }
    """
    doc = Document(input_path)
    raw_paragraphs = _extract_paragraphs(doc)

    # Split into chapters
    chapters: list[tuple[int, list[str]]] = []  # [(num, [paragraphs])]
    current_num: int | None = None
    current_body: list[str] = []
    preamble: list[str] = []

    for para in raw_paragraphs:
        num = _detect_chapter_number(para)
        if num is not None:
            # Commit previous chapter
            if current_num is not None:
                chapters.append((current_num, current_body))
            elif current_body:
                # Content before first chapter heading → preamble
                preamble = current_body
            current_num = num
            current_body = [para]  # heading is first line of chapter body
        else:
            current_body.append(para)

    # Final chapter
    if current_num is not None:
        chapters.append((current_num, current_body))

    if not chapters:
        print("WARNING: No chapter boundaries detected. Outputting entire document as one file.")
        # Write whole document as a single file
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, "chapter-01.md")
        with open(out_path, "w", encoding="utf-8") as f:
            for para in raw_paragraphs:
                f.write(para + "\n\n")
        return [{"chapter_num": 1, "filename": "chapter-01.md", "char_count": sum(len(p) for p in raw_paragraphs)}]

    # Override numbering when user provides start_num
    if start_num is not None:
        offset = start_num - chapters[0][0]
        chapters = [(n + offset, body) for n, body in chapters]

    # Write output
    os.makedirs(output_dir, exist_ok=True)
    results: list[dict] = []
    for num, body in chapters:
        filename = f"chapter-{num:02d}.md"
        out_path = os.path.join(output_dir, filename)
        char_count = sum(len(p) for p in body)
        with open(out_path, "w", encoding="utf-8") as f:
            for para in body:
                f.write(para + "\n\n")
        results.append({
            "chapter_num": num,
            "filename": filename,
            "char_count": char_count,
        })

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert .docx novel manuscript to per-chapter .md files"
    )
    parser.add_argument("input", help="Path to .docx file")
    parser.add_argument(
        "--output-dir", "-o",
        default=None,
        help="Output directory (default: same dir as input)",
    )
    parser.add_argument(
        "--start-num", "-n",
        type=int,
        default=None,
        help="Override the starting chapter number",
    )
    args = parser.parse_args()

    if not os.path.exists(args.input):
        sys.exit(f"ERROR: file not found: {args.input}")

    output_dir = args.output_dir or os.path.join(
        os.path.dirname(os.path.abspath(args.input)) or ".",
        "converted",
    )

    results = convert_docx(args.input, output_dir, args.start_num)

    # Summary
    total_chars = sum(r["char_count"] for r in results)
    print(f"Source: {args.input}")
    print(f"Output: {output_dir}/")
    print(f"Chapters detected: {len(results)}")
    print(f"Total characters: {total_chars:,}")
    print()
    for r in results:
        est_words = r["char_count"] // 2  # rough CJK word count
        print(f"  {r['filename']}  →  ~{r['char_count']:,} chars / ~{est_words:,} words")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
