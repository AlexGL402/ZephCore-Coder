#!/usr/bin/env python3
"""QLoRA training entrypoint placeholder.

The exact stack should be validated on the target GPU before long runs.
See docs/TRAINING.md and configs/*.yaml.
"""
import argparse
import yaml


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args()
    with open(args.config, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    print("Loaded training config:")
    print(yaml.safe_dump(cfg, sort_keys=False))
    print("TODO: wire validated Transformers/PEFT/TRL training implementation after GPU smoke test.")


if __name__ == "__main__":
    main()
