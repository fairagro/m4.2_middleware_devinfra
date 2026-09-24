# Design: sync-one-pr-per-run

## Context

See proposal.md — Why. Today `scripts/sync-products.py` uses a fixed `SYNC_BRANCH = "chore/devinfra-sync"`,
`git push --force`, and updates an existing open PR when present. Spec/docs still say “open or update”. Sync remains a
full allowlist copy (add/update only); no stack or merge queue.

## Goals / Non-Goals

**Goals:**

- One new product sync PR per live sync run that has changes, branch `chore/devinfra-sync-<shortsha>`
- Close older open sync PRs for that consumer with a Superseded comment
- Document the shape in `docs/sync.md`; keep workflow triggers/auth unchanged

**Non-Goals:**

- Auto-merge, merge queue, or `gh stack`
- Incremental/delta syncs
- Deleting allowlisted files in products
- Changing targets, allowlist SoT, or bot secret model
- Cleaning up remote branches after close (optional nicety, out of scope)

## Decisions

### D1 — Branch naming

**Choice:** `chore/devinfra-sync-<7-char-source-sha>` from the Devinfra commit being synced.

**Alternatives:** date stamp; sequential counter. SHA ties the PR to a reproducible SoT revision.

### D2 — How to find PRs to supersede

**Choice:** After creating the new PR, list open PRs whose head ref starts with `chore/devinfra-sync` (covers
`chore/devinfra-sync` and `chore/devinfra-sync-<sha>`), exclude the new PR’s number, then comment + `gh pr close`.

**Alternatives:** label-only filter; author=bot only. Prefix is enough and matches what we create; legacy rolling branch
is included by the same prefix.

### D3 — Push semantics

**Choice:** Create branch from product default tip (shallow clone as today), commit allowlist copy, push **without**
`--force` to a **new** branch name. If the branch somehow exists (retry), fail or use a unique suffix — do not force
onto another open sync’s branch.

**Alternatives:** keep force-push to unique branches (unnecessary if names are unique per SHA).

### D4 — Supersede comment text

**Choice:** Short prose, e.g. `Superseded by #<new>. Newer full allowlist sync from Devinfra \`<sha>\`.`

**Alternatives:** HTML/details. Keep plain for `gh` and humans.

### D5 — Docs only for operator behavior

**Choice:** Update `docs/sync.md` PR-shape section; no new secret or workflow inputs.

## Risks / Trade-offs

- **[Many closed PRs over time]** → Acceptable; GitHub history keeps audit trail. Optional later: delete remote
  branches.
- **[Human wanted the older snapshot]** → Unlikely with full-tree sync; they can restore from the closed PR’s branch tip
  if the branch still exists. Mitigation: comment states superseded reason.
- **[Race: two sync runs same SHA]** → Second run finds no file diff vs product tip after first merged, or same branch
  already pushed — handle “no changes” / push failure without closing the wrong PR. Prefer: only supersede after new PR
  create succeeds.
- **[Open non-sync PR matching prefix]** → Unlikely; prefix is bot-owned convention. Do not close PRs outside the
  prefix.

## Migration Plan

1. Land script + docs on Devinfra `main`.
2. Next live sync opens SHA-scoped PRs and closes existing `chore/devinfra-sync` PRs as superseded.
3. Rollback: revert the script commit; old rolling behavior returns (may need to recreate fixed branch).

## Open Questions

None — explore lock-in: Option A (new PR + supersede), no auto-merge/stack/queue.
