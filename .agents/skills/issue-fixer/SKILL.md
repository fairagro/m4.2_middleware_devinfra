---
name: issue-fixer
description: >-
  Triages a GitHub issue, explores Feature/Refactoring decisions with the user,
  opens a draft PR from one empty bootstrap commit, and implements locally
  without auto-committing fix commits. Use when the user asks to /issue-fixer,
  fix an issue, or start work from an issue URL/number.
---

# Issue fixer

Triage and fix a GitHub issue. You are the **fixer** (precision): implement the smallest correct MVP slice in this PR,
or split deferred work via `/create-issue` when it becomes too large.

You may create a branch and a **draft** PR. To close the issue automatically on merge, the PR body must include:
`Fixes #<issue_number>`.

**Do not** auto-commit or auto-push **fix** commits. You **may** create and push exactly one empty bootstrap commit so
the draft PR can exist. The user commits and pushes the real fixes.

## Input

- Issue number or URL (preferred)

## Auth (`gh`)

`gh` is wrapped (`scripts/bin/gh`, on `PATH` in the Dev Container via `remoteEnv`). Missing `GH_TOKEN` prompts on
`/dev/tty` and is saved to `/commandhistory/tokens.env` in a Dev Container, or `~/.config/<git-repo-name>/tokens.env` on
a local clone (repository name from `origin` — see `docs/conventions.md`). Interactive shells also source
`scripts/dev-tokens.sh` after postCreate (Kombi). Do not read tokens from the git worktree; do not invent them. Never
ask the user to paste a PAT into chat.

**Agent / no TTY:** `/dev/tty` is unavailable in chat, so the wrapper cannot prompt. Before skipping GitHub writes:

1. Tell the user `GH_TOKEN` is missing and that the agent cannot open an interactive prompt here.
2. Ask them to run in a **Dev Container / IDE terminal** (not chat):

   ```bash
   source ./scripts/set-dev-tokens.sh
   ```

   Then reply here when done (or decline).

3. After they confirm, retry `gh` (e.g. `gh auth status`). If auth works, continue with fetch / branch / PR as usual.
4. Only if they decline or auth still fails: skip GitHub writes, print intended branch/PR drafts, and may still work
   locally when appropriate.

## Fetch issue & triage

1. Fetch the issue details (body, labels, URL, type if present) with `gh`.
2. Determine:
   - org issue type: `Bug|Security|Feature|Task|Discussion|Refactoring`
   - triage labels: `severity:*`, `practicality:*`, `cost:*` (if set)
   - problem statement; affected paths; acceptance criteria / “done when”

3. Early exits:
   - Missing actionable info → comment with at most 3 questions and stop (no code / no PR).
   - Already resolved / not applicable → comment briefly and stop.
   - Type `Discussion` → do **not** create branch/PR by default; ask for a decision or retype. Proceed only if the user
     explicitly requests a concrete implementation.
   - Type `Security` → may implement, but require clear acceptance criteria and a realistic path; prefer the smallest
     correct fix; no speculative hardening with no path.

## Explore pause (before any branch / commit / PR)

After triage, **before** GitHub writes:

| Type                      | Explore?                                                                  |
| ------------------------- | ------------------------------------------------------------------------- |
| `Feature`, `Refactoring`  | **Required** — surface open threads, recommend defaults, wait for lock-in |
| `Discussion`              | Explore is the whole response (no implement by default)                   |
| `Bug`, `Security`, `Task` | Only if criteria missing, multiple plausible fixes, or user asks          |

During explore: read the codebase, open numbered decision threads, recommend defaults as proposals. **Do not** create
branches, commits, or PRs. Wait for user lock-in, `go`, or `skip explore`.

**`/opsx-explore` is optional.** In-skill explore (above) is enough; you MAY offer `/opsx-explore` as a thinking aid,
but MUST NOT require it and MUST NOT block on it.

## OpenSpec propose (required before branch / PR / implement)

**`/opsx-propose` is mandatory** on every run that will implement.

After triage and explore lock-in (when explore ran), and **before** any branch, empty commit, draft PR, or
implementation: **always** run `/opsx-propose`.

1. Require a local `openspec/` tree. If it is missing, stop and tell the user — do not skip propose and implement
   anyway.
2. Read and follow [`.cursor/skills/openspec-propose/SKILL.md`](../../../.cursor/skills/openspec-propose/SKILL.md)
   (same as invoking `/opsx-propose`): create a change name from the issue, generate proposal / specs / design / tasks.
3. Name the change from the issue (kebab-case slug + issue context). Fold explore lock-ins into design/tasks.
4. **Spec-review pause:** After artifacts exist, **stop**. Show the change name/path and ask the user to review
   proposal / specs / design / tasks. Do **not** create a branch, empty commit, draft PR, or start implementation until
   they confirm (e.g. `go`, `approved`, or an `/opsx-update` pass then `go`). If they request changes, run
   `/opsx-update` (or edit artifacts) and pause again.
5. Only after that confirmation: proceed to branch + draft PR, then implement (prefer `/opsx-apply` against that
   change’s `tasks.md`).

Early exits that never implement (missing info, already resolved, `Discussion` without an explicit implement request)
skip propose. Once the user asks to implement a `Discussion`, propose is required first.

## Branch + draft PR (empty bootstrap commit)

Assumptions: base branch is `main`. Prefer the plumbing CLI when the tree is clean:

```bash
uv run --project scripts/ai m42-ai issue-start --issue <issue_number> [--slug <slug>]
```

That creates `issue-<issue_number>-<slug>`, one empty commit `Start issue #<issue_number>`, pushes, and opens a
**draft** PR with `Fixes #<issue_number>`. See [`scripts/ai/README.md`](../../../scripts/ai/README.md).

Manual equivalent if the CLI is unavailable:

1. Create local branch: `issue-<issue_number>-<slug>` from `main`.
2. Ensure working tree **and** index are clean. Then create **exactly one** empty commit (do **not** use `--no-verify`):

   ```bash
   git commit --allow-empty -m "Start issue #<issue_number>"
   ```

3. Push the branch and create a **draft** PR:

   ```bash
   gh pr create --draft --base main --title "..." --body "$(cat <<'EOF'
   ## Summary
   - MVP scope: …

   Fixes #<issue_number>
   EOF
   )"
   ```

4. Do **not** mark the PR ready for review. Remind the user to mark ready after they push real commits.

## Implement fixes (locally)

After the draft PR exists:

- Implement in the working tree on the PR branch.
- Do **not** commit or push fix commits.
- If too large: split (below) and implement only the MVP slice here.
- When the consumer has product `middleware/` packages: run focused `uv run pytest` on affected packages and
  `uv run ruff format --config pyproject.toml` / `ruff check` on touched files (same bar as `/review-fixer`). This
  Devinfra repo has no product `middleware/` tree — skip those commands here.

### For the user

Ask them to review the working tree, commit, push, then mark the PR ready when the slice is the review surface.

## Split / deferred work (via create-issue)

Split only when ≥2 **logically independent**, independently mergeable blocks exist. Within a block, ~50 new production
lines is a **guideline**, not a hard cap. Extra signals only when blocks exist: new abstraction, spec-contract change,
prerequisite refactor.

Open deferred slices by reading and following [`.agents/skills/create-issue/SKILL.md`](../create-issue/SKILL.md) (one
invocation per issue, max 3–6). Do **not** call `gh issue create` with an issue-fixer-only inline template.

**Relation (lock-in G):**

- Still part of this issue’s acceptance criteria / done-when → `relation: sub-of #<issue_number>` (GitHub native
  sub-issue).
- Distinct follow-up problem (not in done-when) → `relation: linked`.
- Unclear → ask once; default `linked`.

Types for slices: `Refactoring` when structural; `Task` when the parent is only subdivided; keep Bug/Feature/Security
when the slice retains that nature.

Link deferred issue URLs from the PR body. If create-issue is missing in a consumer checkout, say so and print intended
create-issue inputs — do not invent an off-allowlist create path.

## Fix quality

- Follow Type Safety in [`openspec/principles.global.md`](../../../openspec/principles.global.md): no wide types (`Any`,
  `object`, unnecessary `T | None`).
- Update specs only when the real contract changes.

## Output to the user

Provide:

- Issue URL + number + org issue type
- Whether explore ran and what was locked
- OpenSpec change name / path from `/opsx-propose`, and whether the user approved the spec-review pause
- Branch name
- Draft PR URL (or “skipped PR creation” + draft)
- Created sub-issue / linked-issue URLs (or none)
- Reminder: user commits, pushes, and marks the PR ready; agent does not auto-commit fix commits
