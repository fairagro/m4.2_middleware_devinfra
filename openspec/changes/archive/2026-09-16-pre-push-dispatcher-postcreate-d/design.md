## Context

See `proposal.md` for motivation (#114 decision → #155). Today `setup-git-hooks.sh` copies a monolith quality `pre-push`
over `.git/hooks/pre-push`, and postCreate must not call product LFS scripts by name. Products that compose LFS +
quality lose the overlay on every shared install / create unless they re-run product setup manually.

## Goals / Non-Goals

**Goals:**

- Idempotent shared installer for dispatcher + `50-quality` only
- Stable product extension via `pre-push.d/` numbering
- T-late hard-fail `devcontainer-post-create.d/` without hard-coded LFS names
- Spec/docs aligned so sync consumers know the adopt contract

**Non-Goals:**

- Shipping Git LFS or `setup-git-lfs.sh` from Devinfra
- `.d` compose for `post-checkout` / `post-commit` / `post-merge` in this MVP
- Implementing sql_to_arc drop-ins/fragments in this repo (document only; product follow-up)

## Decisions

1. **SoT layout under `scripts/git-hooks/`**
   - `pre-push` — dispatcher source (installed to `.git/hooks/pre-push`)
   - `pre-push.d/50-quality` — current quality logic (moved from today’s monolith body)
   - Alternative considered: keep quality as `scripts/git-hooks/pre-push` and generate dispatcher elsewhere — rejected;
     runtime paths should mirror SoT names for mental model.

2. **Dispatcher behavior**
   - `nullglob`, sort order = lexicographic filename order, skip non-executable with hard error (same bar as postCreate
     drop-ins) OR skip non-files; prefer fail-closed on non-executable regular files so mis-chmod is visible.
   - Buffer stdin once; replay to each fragment.
   - Alternative: soft-skip non-executable fragments — rejected for operator footguns.

3. **Foreign fragment preservation**
   - Setup only `cp`s dispatcher + `50-quality`; never `rm` on `pre-push.d/*`.
   - Alternative: wipe and rebuild `pre-push.d` — rejected (breaks product fragments).

4. **postCreate C2**
   - Glob `scripts/devcontainer-post-create.d/*` at end of script; hard-fail.
   - Directory is product-owned and **not** on the sync allowlist (only the shared runner lives in synced
     `devcontainer-post-create.sh`).
   - Alternative: C1 single `product-post-create.sh` — superseded by lock-in to C2.

5. **`git lfs install` interaction (product guidance)**
   - Products must install fragments **after** any `git lfs install --force` that rewrites `.git/hooks/pre-push`, and
     must restore/ensure the shared dispatcher remains the entrypoint (re-run shared `setup-git-hooks.sh` then product
     fragment install, or only write into `pre-push.d/`).

## Risks / Trade-offs

- [Products still overwrite dispatcher] → Docs + adopt checklist; hard-fail drop-in makes missing LFS setup loud when
  drop-in exists but broken.
- [Empty `pre-push.d` after only product fragment without shared setup] → postCreate always runs shared setup first.
- [Lexicographic vs numeric intent] → Convention `NN-name`; document `10-git-lfs` before `50-quality`.

## Migration Plan

1. Land Devinfra change; sync to products.
2. sql_to_arc: replace monolith compose `pre-push` install with `pre-push.d/10-git-lfs`; add
   `scripts/devcontainer-post-create.d/50-git-lfs.sh` → `setup-git-lfs.sh`; update product docs that still say shared
   setup “strips post-*”.
3. Rollback: revert to monolith copy (lossy for foreign fragments already present — acceptable for rollback).
