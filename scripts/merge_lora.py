#!/usr/bin/env python3
"""Merge a trained PEFT LoRA adapter into its base model."""
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base", required=True)
    p.add_argument("--adapter", required=True)
    p.add_argument("--output", required=True)
    args = p.parse_args()
    print(f"TODO after training stack validation: merge {args.adapter} into {args.base} -> {args.output}")


if __name__ == "__main__":
    main()
