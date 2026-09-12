# Roadmap

## Stage 1 — repository and baseline

- [x] Create ZephCore-Coder repository.
- [x] Define project structure and training philosophy.
- [ ] Select 10–20 held-out baseline tasks.
- [ ] Connect plain 14B base model to a real ZephCore repo as a coding agent.
- [ ] Record build/test/manual-fix metrics.

## Stage 2 — dataset v1

- [ ] Implement Git history collector.
- [ ] Collect accepted commits and patches.
- [ ] Attach original task descriptions where available.
- [ ] Reconstruct relevant pre-change context.
- [ ] Add build/test result metadata.
- [ ] Implement secret sanitization.
- [ ] Separate accepted and rejected solutions.
- [ ] Create train/validation split without leakage.

## Stage 3 — training pipeline prototype

- [ ] Validate dependencies on RTX 3060.
- [ ] Run QLoRA on 7B/8B model.
- [ ] Load adapter and run eval.
- [ ] Test merge and GGUF export.

## Stage 4 — ZephCore-Coder v1

- [ ] Validate P104 training stack on AI6.
- [ ] Run short 14B smoke-test training.
- [ ] Inspect loss, VRAM, throughput, output quality.
- [ ] Run full v1 QLoRA only after smoke test succeeds.
- [ ] Save adapter + exact config + dataset version.

## Stage 5 — objective comparison

- [ ] Base 14B eval.
- [ ] Fine-tuned 14B eval.
- [ ] 30B local reference eval.
- [ ] Codex/reference comparison.
- [ ] Reject v1 if it does not beat base 14B on held-out engineering metrics.

## Stage 6 — local coding agent

- [ ] Repo file search/context retrieval.
- [ ] Git diff generation.
- [ ] Build/test tool execution.
- [ ] Iterative error repair.
- [ ] Safety checks before applying patches.
- [ ] Optional RAG/index for repository navigation.

## Later ideas

- preference training from accepted vs rejected patches;
- automated harvesting of future successful coding-agent sessions;
- per-domain adapters (Zephyr, ESP32, RF/radio, UI);
- continual dataset versioning rather than blindly continual fine-tuning.
