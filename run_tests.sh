#!/bin/bash

# Usage: ./run_lines.sh <mode> <max_lines>
MODE="$1"
MAX="$2"

if [[ -z "$MODE" || -z "$MAX" ]]; then
    echo "Usage: $0 <mode> <max_lines>"
    exit 1
fi

WORDS_FILE="testWords.txt"

while IFS= read -r word; do
    echo "Testing word: $word"
    python3 performance.py "$word" -l -m "$MODE" --max "$MAX"
done < "$WORDS_FILE"
