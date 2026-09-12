# Dataset design

The supervised target is **not** generic source-code completion. Each example should represent a real engineering task and its accepted solution.

## Recommended record

```json
{
  "id": "zephcore-000001",
  "task": "SX1262 transmits but does not return to RX after TX",
  "repo": "AlexGL402/ZephCore-MultiRadio",
  "base_commit": "<sha-before-fix>",
  "context": [
    {"path": "src/radio.cpp", "content": "..."},
    {"path": "boards/...conf", "content": "..."}
  ],
  "build_log_before": "...",
  "patch": "diff --git ...",
  "build_log_after": "...",
  "test_result": "RX restored and build passed",
  "accepted": true,
  "source": "codex+manual-review"
}
```

## Positive examples

Keep only final accepted solutions as positive SFT examples. If a generated solution was wrong and then manually corrected, train on the final correct patch.

## Rejected examples

Wrong or incomplete patches go to `dataset/rejected.jsonl`. They may later be useful for preference/ranking training, but should not be mixed into the positive target set.

## Context selection

Avoid dumping the whole repo. Include only files that were relevant to the accepted change, plus limited dependency/config context where needed.

## Sanitization

Before committing any dataset:
- strip API tokens and passwords;
- remove `.env` contents;
- remove private URLs/credentials;
- review Wi-Fi credentials and device identifiers;
- avoid proprietary third-party code you do not have permission to redistribute.

## Split strategy

Do not randomly split near-duplicate tasks across train and validation.

Prefer grouping related commits/tasks so one bug series stays in one split. Keep a truly held-out eval set with tasks that the trained model has never seen.
