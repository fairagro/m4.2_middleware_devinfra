# m42-ai — agent GitHub/git plumbing

Small Python CLI for deterministic GitHub/git work used by `/review-fixer`, `/create-issue`, and `/issue-fixer`.

## Run

From a clone of this repo (or another git checkout where `gh` can resolve the GitHub remote). `--project` may point at
this package from any path; GitHub commands still need a repo context (`gh` cwd / remotes), unless you pass `--owner` /
`--repo` where the command supports them:

```bash
uv run --project scripts/ai m42-ai --help
uv run --project scripts/ai m42-ai review-open --pr 22
```

Auth: uses `gh` on `PATH` (Dev Container: `scripts/bin/gh` + `GH_TOKEN`). No second credential model.

## Commands

| Command                         | Role                                                                                  |
| ------------------------------- | ------------------------------------------------------------------------------------- |
| `auth-status`                   | Probe `gh auth` as JSON; exit `1` when not ok                                         |
| `review-open --pr N`            | One GraphQL fetch; JSON of unresolved AI threads + latest AI review body / suppressed |
| `review-reply`                  | `in_reply_to` on a review comment, or `--conversation` PR comment                     |
| `review-resolve --thread-id ID` | `resolveReviewThread`                                                                 |
| `issue-view --issue N`          | Stable triage JSON (type, labels, body, url, triage:\* extract)                       |
| `issue-create`                  | Type + triage labels (+ optional `--parent`)                                          |
| `issue-branch --issue N`        | Ensure `issue-N-slug` checked out from base (no commit / push / PR)                   |
| `branch-ahead`                  | JSON ahead/behind vs base; exit `1` when tip is not ahead                             |
| `issue-start --issue N`         | Ensure branch, push when ahead of base, draft PR with `Fixes #N` (no empty commit)    |
| `pr-strip-footer --pr N`        | Remove trailing “Made with Cursor” (and similar) footers from a PR body               |

## Tests

```bash
uv run --project scripts/ai pytest
```

Fixtures only — no live GitHub in CI.
