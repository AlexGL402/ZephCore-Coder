# Training guide

## Phase 0 — baseline

Before fine-tuning, test the untouched base model as a coding agent on 10–20 real tasks. Preserve results for comparison.

## Phase 1 — pipeline validation on 7B/8B

Use the RTX 3060 laptop to prove that the entire pipeline works:

1. create a small sanitized dataset;
2. train a small LoRA;
3. load the adapter;
4. run eval;
5. optionally merge;
6. export to GGUF;
7. run locally.

Do not optimize quality yet; verify reproducibility first.

## Phase 2 — 14B QLoRA on AI6

Target `Qwen2.5-Coder-14B-Instruct` on the AI6 machine with 3x P104-100.

The initial config is intentionally conservative. P104/Pascal-era cards have limitations versus modern RTX cards, so test short runs before committing to long training.

Watch:
- CUDA / bitsandbytes compatibility;
- whether the selected compute dtype is supported efficiently;
- VRAM per GPU;
- CPU RAM pressure;
- gradient-checkpointing overhead;
- effective tokens/sec.

## What QLoRA changes

QLoRA keeps the base model quantized and trains lightweight LoRA parameters. The valuable output is the adapter, not a second copy of the full base model.

After training you can either:
- run base model + LoRA adapter;
- merge adapter into a full model;
- convert merged model to GGUF for llama.cpp/Ollama.

## Do not overtrain

A small specialized dataset can overfit quickly. Start with 1–2 epochs and evaluate. More epochs are not automatically better.
