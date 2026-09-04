# m42-ai — agent GitHub/git plumbing

Small Python CLI for deterministic GitHub/git work used by `/review-fixer`, `/create-issue`, and `/issue-fixer`.

## Run

From the repo root (or any cwd; `--project` points at this package):

```bash
uv run --project scripts/ai m42-ai --help
uv run --project scripts/ai m42-ai review-open --pr 22
```

Auth: uses `gh` on `PATH` (Dev Container: `scripts/bin/gh` + `GH_TOKEN`). No second credential model.

## Commands

| Command | Role |
| ------- | ---- |
| `review-open --pr N` | One GraphQL fetch; JSON of unresolved AI threads + latest AI review body / suppressed |
| `review-reply` | `in_reply_to` on a review comment, or `--conversation` PR comment |
| `review-resolve --thread-id ID` | `resolveReviewThread` |
| `issue-create` | Type + triage labels (+ optional `--parent`) |
| `issue-start --issue N` | Branch, empty bootstrap commit, draft PR with `Fixes #N` |

## Tests

```bash
uv run --project scripts/ai pytest
```

Fixtures only — no live GitHub in CI.
