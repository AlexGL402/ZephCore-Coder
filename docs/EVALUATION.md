# Evaluation

The key question is not "does the answer sound good?" but "does the engineering change work?"

## Compare

- base 14B;
- fine-tuned 14B;
- local 30B reference model;
- Codex/reference patch when available.

## Keep eval held out

Evaluation tasks must not be present in the supervised dataset. Avoid near-duplicate commits from the same bug series.

## Core metrics

1. Patch applies cleanly.
2. Build passes.
3. Tests pass.
4. Runtime behavior is correct where hardware tests exist.
5. Manual corrections required.
6. Hallucinated symbols/APIs.
7. Unnecessary files changed.
8. Regression count.

## Suggested result record

```json
{
  "task_id": "eval-001",
  "model": "qwen2.5-coder-14b-zephcore-v1",
  "patch_applies": true,
  "build_pass": true,
  "tests_pass": true,
  "manual_fix_count": 0,
  "hallucinated_symbol_count": 0,
  "notes": "RX state restored correctly"
}
```
