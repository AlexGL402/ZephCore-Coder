# First practical run

The first goal is **not training**. It is to create trustworthy baseline and dataset inputs.

## 1. Clone both repositories side by side

```text
work/
├── ZephCore-Coder/
└── ZephCore-MultiRadio/
```

## 2. Install data-pipeline dependencies

From `ZephCore-Coder`:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux:
# source .venv/bin/activate

pip install -r requirements.txt
```

## 3. Export Git history candidates

```bash
python scripts/collect_git_history.py ../ZephCore-MultiRadio --output dataset/raw/git_history.jsonl --max-count 500
```

This exports commit metadata and diffs. It does **not** automatically mark them as correct training examples.

## 4. Rank likely useful commits

```bash
python scripts/select_candidate_commits.py dataset/raw/git_history.jsonl
```

Review `dataset/processed/candidates.jsonl` manually.

## 5. Build held-out baseline tasks first

Before turning accepted fixes into training data, reserve 10–20 representative tasks for evaluation.

```bash
python scripts/make_baseline_task.py
```

Each run appends one record to `eval/tasks.jsonl`.

## 6. Test the untouched 14B model

Run each baseline task against the plain Qwen2.5-Coder-14B-Instruct coding agent. Save:

- generated patch;
- build log;
- test/hardware result;
- manual corrections;
- token/time data if convenient.

Do not fine-tune until this baseline is recorded.

## 7. Curate training examples

For non-held-out accepted fixes, reconstruct:

`task -> relevant pre-change context -> accepted patch -> build/test evidence`

Then sanitize before any public commit.

## Important

Git history alone rarely contains the original user request. The highest-value dataset will come from combining Git artifacts with the actual task/prompt and final accepted engineering result.
