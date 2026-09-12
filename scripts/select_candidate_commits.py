#!/usr/bin/env python3
"""Rank collected git-history records as dataset candidates.

This is a heuristic filter, not an acceptance decision. Human review remains
required because a commit can build successfully yet still be a poor training
example.
"""
import argparse
import json
import re

POSITIVE = re.compile(
    r"(?i)\b(fix|working|restore|resolve|correct|support|add|implement|rework|rx|tx|kconfig|dts|radio|esp-?now)\b"
)
NEGATIVE = re.compile(r"(?i)\b(wip|tmp|temporary|debug only|revert|merge branch)\b")


def score(row):
    msg = row.get("message", "")
    diff = row.get("diff", "")
    s = 0
    if POSITIVE.search(msg):
        s += 3
    if NEGATIVE.search(msg):
        s -= 5
    if 50 <= len(diff) <= 30000:
        s += 2
    if "diff --git" in diff:
        s += 1
    if len(diff) > 100000:
        s -= 3
    return s


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("--output", default="dataset/processed/candidates.jsonl")
    p.add_argument("--min-score", type=int, default=2)
    args = p.parse_args()

    rows = []
    with open(args.input, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                row = json.loads(line)
                row["candidate_score"] = score(row)
                if row["candidate_score"] >= args.min_score:
                    rows.append(row)

    rows.sort(key=lambda x: x["candidate_score"], reverse=True)
    with open(args.output, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Wrote {len(rows)} candidate commits to {args.output}")


if __name__ == "__main__":
    main()
