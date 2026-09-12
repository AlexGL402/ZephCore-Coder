#!/usr/bin/env python3
"""Conservative text sanitizer for dataset JSONL.

This is only a first-pass safety filter. Human review is still required before
publishing dataset records.
"""
import argparse
import json
import re

PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|token|password|passwd|secret)\s*[:=]\s*[^\s,;]+"), r"\1=<REDACTED>"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"), "<REDACTED_GITHUB_TOKEN>"),
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "<REDACTED_API_KEY>"),
]


def clean_text(value):
    if not isinstance(value, str):
        return value
    for pattern, repl in PATTERNS:
        value = pattern.sub(repl, value)
    return value


def walk(obj):
    if isinstance(obj, dict):
        return {k: walk(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk(v) for v in obj]
    return clean_text(obj)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("input")
    p.add_argument("output")
    args = p.parse_args()
    with open(args.input, encoding="utf-8") as src, open(args.output, "w", encoding="utf-8") as dst:
        for line in src:
            if line.strip():
                dst.write(json.dumps(walk(json.loads(line)), ensure_ascii=False) + "\n")
    print(f"Sanitized dataset written to {args.output}; manual review still required")


if __name__ == "__main__":
    main()
