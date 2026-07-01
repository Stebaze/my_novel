#!/bin/bash
# pre-flight-check 脚本化包装（2026-07-01 修复 #1）
# 调用：./pre-flight-check.sh <draft_dir> <target_chapter> [scope]
#
# 等价于：
#   python3 scripts/pre-flight-check.py <draft_dir> <target_chapter> [scope]

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"
SCRIPTS_DIR="$ROOT/.claude/skills/scripts"

if [ $# -lt 2 ]; then
    echo "Usage: $0 <draft_dir> <target_chapter> [scope]"
    exit 1
fi

python3 "$SCRIPTS_DIR/pre-flight-check.py" "$@"
