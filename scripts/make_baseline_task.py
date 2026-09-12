#!/usr/bin/env python3
"""Create one held-out baseline task record interactively."""
import argparse
import json
from pathlib import Path


def ask(label, default=""):
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default="eval/tasks.jsonl")
    args = p.parse_args()

    rec = {
        "id": ask("Task id", "baseline-001"),
        "title": ask("Title"),
        "repo": ask("Repo", "AlexGL402/ZephCore-MultiRadio"),
        "base_ref": ask("Base commit/ref"),
        "prompt": ask("Exact task/prompt"),
        "allowed_context": [x.strip() for x in ask("Allowed paths, comma separated").split(",") if x.strip()],
        "build_command": ask("Build/test command"),
        "expected": {
            "build_pass": ask("Expected build pass? y/n", "y").lower().startswith("y"),
            "notes": ask("Expected observable result")
        },
        "source_commit": ask("Accepted fix commit (optional)"),
        "holdout": True
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Added {rec['id']} to {out}")


if __name__ == "__main__":
    main()
