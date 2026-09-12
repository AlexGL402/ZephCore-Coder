# Baseline evaluation plan

Before any fine-tuning, measure what the untouched coding model can already do on ZephCore/MeshCore work.

## Why this matters

Without a baseline we cannot know whether QLoRA actually improved the model. A fine-tuned model that merely sounds more familiar with the project but breaks more builds is worse.

## Target

Primary baseline:

`Qwen2.5-Coder-14B-Instruct`

Reference models:

- local 30B coding model;
- Codex/reference solution when available.

## First 10–20 tasks

Choose real tasks that are representative but **not used for training** later.

Good categories for ZephCore-MultiRadio:

1. Zephyr/Kconfig build failure.
2. Device-tree pin mapping mistake.
3. SX1262 TX works but RX recovery fails.
4. Radio busy/IRQ state handling.
5. nRF52840 GPIO or UART mapping correction.
6. ESP-NOW transport/dispatcher integration.
7. Cross-band dedup/TTL logic.
8. CLI/status counter change.
9. Display/board configuration change.
10. Compile-time configuration regression.

Prefer tasks where success can be checked by build/tests/logs instead of subjective review.

## Task record

Each held-out task should contain:

```json
{
  "id": "baseline-001",
  "title": "Short human-readable title",
  "repo": "AlexGL402/ZephCore-MultiRadio",
  "base_ref": "<commit or branch before the fix>",
  "prompt": "Exact task given to the model",
  "allowed_context": [
    "zephcore/...",
    "boards/..."
  ],
  "build_command": "...",
  "expected": {
    "build_pass": true,
    "notes": "observable behavior expected"
  },
  "source_commit": "<accepted-fix-sha-if-known>",
  "holdout": true
}
```

## Rules

- Never train on baseline tasks.
- Keep the original prompt if available.
- Do not reveal the accepted diff to the tested model.
- Start each model from exactly the same base revision.
- Give each model the same allowed repository context and build/test access.
- Save generated patch and logs separately.

## Score

Minimum useful fields:

- patch applies;
- build passes;
- hardware/runtime test passes where available;
- number of manual edits after model output;
- hallucinated symbols/APIs;
- unnecessary files touched.

A model wins only if it improves engineering outcomes, not because its explanation is longer.
