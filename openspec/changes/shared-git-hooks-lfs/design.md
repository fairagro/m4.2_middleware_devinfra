# Design: shared-git-hooks-lfs

## Context

Issue #9. Shared pre-commit skeleton (#7) already defines the **pre-push** stage; this change ships the **git hook
files** and installer so `git push` actually runs that stage (after Git LFS).

## Goals / Non-Goals

**Goals**

- Syncable hooks + installer matching the product API layout.
- `pre-push`: `git lfs pre-push` then pre-commit `hook-impl` with `--hook-type=pre-push`.
- Clear docs: commit-stage = `pre-commit install --hook-type pre-commit`; LFS/pre-push files = `setup-git-lfs.sh`.

**Non-Goals**

- Full Dev Container postCreate orchestration (#10) beyond documenting the call.
- Changing `.pre-commit-config.yaml` hook set (already from #7).
- Host package-manager installs (`brew` / `apt-get` auto-install of git-lfs) — unsupported environment.

## Decisions

1. **Port API layout, slim install** — Keep copy-into-`.git/hooks` and `git lfs install --local --skip-smudge --force`.
   If `git-lfs` is missing, **fail with install guidance** (no apt/brew auto-install).
2. **Pre-commit invocation** — Prefer `uv run pre-commit` (repo root), then `.venv` `python -m pre_commit`, then
   `pre-commit` on PATH — aligns with quality scripts / uv-only principles.
3. **Hook comments** — State install via `scripts/setup-git-lfs.sh` (fix API comment that said `setup-git-hooks.sh`).
4. **Overwrite, no backup** — After `git lfs install --force`, always replace the four hooks with project copies. Do not
   leave `.backup` files under `.git/hooks/`.

## Risks / Trade-offs

- **[Risk] pre-push is slow (pytest + CST)** → Mitigation: already accepted in #7; docs warn Docker/tests needed.
- **[Risk] Double LFS install** → `--local --force` + project hooks replace defaults; documented.

## Migration Plan

Sync files to products; run `./scripts/setup-git-lfs.sh` once per clone (and from postCreate when #10 lands).

## Open Questions

None for MVP — follow issue Done when + API shape with uv/DC constraints above.
