#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage: $0 <merged-model-dir> <output.gguf> [llama.cpp-dir]"
  exit 1
fi

MODEL_DIR="$1"
OUT="$2"
LLAMA_DIR="${3:-../llama.cpp}"

python "$LLAMA_DIR/convert_hf_to_gguf.py" "$MODEL_DIR" --outfile "$OUT"

echo "GGUF written to $OUT"
