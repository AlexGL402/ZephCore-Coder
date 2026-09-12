#!/usr/bin/env python3
"""Build curated train/validation JSONL from reviewed records.

Expected input records should already contain a real task and accepted=true.
This script intentionally refuses to label arbitrary git commits as correct
training examples.
"""
import argparse
import json
import random
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--train", default="dataset/train.jsonl")
    p.add_argument("--validation", default="dataset/validation.jsonl")
    p.add_argument("--validation-ratio", type=float, default=0.1)
    p.add_argument("--seed", type=int, default=42)
    args = p.parse_args()

    rows = []
    with open(args.input, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("accepted") is True and row.get("task") and row.get("patch"):
                rows.append(row)

    random.Random(args.seed).shuffle(rows)
    n_val = max(1, int(len(rows) * args.validation_ratio)) if rows else 0
    val, train = rows[:n_val], rows[n_val:]

    for path, data in [(Path(args.train), train), (Path(args.validation), val)]:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as f:
            for row in data:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"train={len(train)} validation={len(val)}")


if __name__ == "__main__":
    main()
