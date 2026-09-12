#!/usr/bin/env python3
"""Collect candidate Git commits and patches for later dataset curation.

This first version deliberately does not pretend every commit is a valid training
example. It exports commit metadata and diff text so accepted engineering tasks
can be curated in the next stage.
"""
import argparse
import json
from pathlib import Path
from git import Repo


def main():
    p = argparse.ArgumentParser()
    p.add_argument("repo", help="Path to source git repository")
    p.add_argument("--output", default="dataset/raw/git_history.jsonl")
    p.add_argument("--max-count", type=int, default=500)
    args = p.parse_args()

    repo = Repo(args.repo)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("w", encoding="utf-8") as f:
        for commit in repo.iter_commits(max_count=args.max_count):
            parents = commit.parents
            if not parents:
                continue
            parent = parents[0]
            diff = repo.git.diff(parent.hexsha, commit.hexsha, "--binary", "--no-ext-diff")
            rec = {
                "commit": commit.hexsha,
                "parent": parent.hexsha,
                "author": str(commit.author),
                "date": commit.committed_datetime.isoformat(),
                "message": commit.message.strip(),
                "diff": diff,
            }
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    print(f"Wrote candidate commit history to {out}")


if __name__ == "__main__":
    main()
