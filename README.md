# ZephCore-Coder

Local coding-model project focused on ZephCore / MeshCore development workflows.

The goal is not to memorize the whole repository. The goal is to train a model on the way successful engineering changes are made in this codebase:

`task -> relevant repo context -> correct patch/diff -> build/test result -> accepted final state`

## Project goals

- Build a local coding model specialized for ZephCore / MeshCore.
- Reduce dependence on remote coding agents for routine embedded-development tasks.
- Keep current source code outside model weights and provide it dynamically as context/RAG.
- Fine-tune behavior, patch style, debugging patterns, and project-specific engineering habits.
- Evaluate improvements objectively with held-out tasks.

## Recommended base model

Primary target: `Qwen2.5-Coder-14B-Instruct`.

Why 14B:
- practical inference on 2x P104-100 8 GB;
- realistic QLoRA target for AI6 with 3x P104-100;
- stronger than a small 7B baseline while still manageable;
- 30B-class models are better kept as stronger reference/teacher models.

Prototype target: a 7B/8B coding model for validating the pipeline on an RTX 3060 8 GB laptop.

## Hardware roles

### Laptop — RTX 3060 8 GB + 16 GB RAM
Use for scripts, tiny datasets, 7B/8B QLoRA prototypes, dataset/eval validation.

### Huanan — 2x P104-100 8 GB
Use for inference, baseline tests, local coding-agent experiments, and model comparison.

### AI6 — 3x P104-100 8 GB
Primary machine for 14B QLoRA training and adapter generation.

## Training philosophy

Do **not** train on hidden chain-of-thought or raw conversation transcripts.

Do **not** simply dump the full source tree into supervised fine-tuning data.

Prefer real, verifiable engineering artifacts:
- requested task;
- repository state before the change;
- relevant files/context;
- git diff / patch;
- build output;
- test result;
- final accepted fix;
- manual corrections after an initially wrong generated patch.

Only successful/accepted examples should be positive supervised targets. Broken attempts belong in `dataset/rejected.jsonl` for later analysis or preference/ranking work.

## High-level pipeline

```text
Codex history / Git history / accepted patches
        |
        v
scripts/collect_git_history.py
        |
        v
scripts/build_dataset.py
        |
        v
dataset/train.jsonl + validation.jsonl
        |
        v
scripts/train_qlora.py
        |
        v
LoRA adapter
        |
        +--> evaluate adapter directly
        |
        v
scripts/merge_lora.py
        |
        v
merged model
        |
        v
scripts/export_gguf.sh
        |
        v
llama.cpp / Ollama / local coding agent
```

## Repository layout

```text
ZephCore-Coder/
├── README.md
├── requirements.txt
├── .gitignore
├── configs/
│   ├── qlora_7b.yaml
│   ├── qlora_14b.yaml
│   └── eval.yaml
├── docs/
│   ├── DATASET.md
│   ├── TRAINING.md
│   ├── EVALUATION.md
│   └── ROADMAP.md
├── scripts/
│   ├── collect_git_history.py
│   ├── build_dataset.py
│   ├── sanitize_dataset.py
│   ├── train_qlora.py
│   ├── eval_model.py
│   ├── merge_lora.py
│   └── export_gguf.sh
├── dataset/
│   ├── raw/
│   ├── processed/
│   ├── train.jsonl
│   ├── validation.jsonl
│   └── rejected.jsonl
├── lora/
└── eval/
    ├── tasks.jsonl
    └── results/
```

## Git policy

Good candidates for GitHub:
- scripts;
- configs;
- docs;
- eval tasks;
- small sanitized datasets;
- LoRA adapters via Git LFS when appropriate.

Do not commit normally:
- base model weights;
- merged multi-GB checkpoints;
- large GGUF files;
- Hugging Face caches;
- temporary checkpoints;
- raw datasets containing secrets.

The most valuable reproducible artifacts are:

`dataset + configs + scripts + eval set + LoRA adapter`

## Fine-tuning vs runtime context

Fine-tuning should teach how to modify the project correctly: patch style, debugging patterns, Zephyr/Kconfig/DTS behavior, embedded-radio habits, and project conventions.

Runtime context/RAG should provide the current repo state, APIs, board configs, build logs, and task-specific files. This keeps the model useful as the repository evolves.

## Before training: baseline first

Connect the plain base 14B model to a real repo and run roughly 10–20 representative tasks. Save task, provided context, produced patch, apply/build/test results, manual corrections, and optional timing/token metrics.

After training, evaluate on held-out tasks not present in train.

Compare:
- base 14B;
- fine-tuned 14B;
- local 30B reference;
- Codex/reference result where available.

## Success criteria

Prefer measurable engineering outcomes:
- patch applies;
- build passes;
- tests pass;
- no regression;
- focused diff;
- fewer manual corrections;
- correct file selection;
- fewer hallucinated APIs/symbols.

## First milestones

1. Freeze held-out eval set.
2. Implement dataset schema.
3. Implement Git history collector.
4. Build/sanitize dataset v1.
5. Validate pipeline on 7B/8B.
6. Run first 14B QLoRA on AI6.
7. Compare base vs fine-tuned 14B.
8. Merge/export only if eval proves improvement.
9. Integrate best model into a local coding-agent workflow.

See `docs/ROADMAP.md` for the detailed plan.
