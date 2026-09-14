## Context

See proposal.md — Why. Shared `setup-git-hooks.sh` currently deletes LFS `post-*` hooks; issue #112 originally suggested
an optional product-script callback from postCreate. Lock-in: remove LFS coupling from the shared installer; do **not**
add “if `scripts/install-dev-hooks.sh` exists, run it” indirection.

## Goals / Non-Goals

**Goals:**

- Shared hook installer installs quality `pre-push` only and ignores other hooks.
- Shared postCreate stays a fixed sequence with no product-script callbacks.
- Docs match verbatim JSON + `product.env` and product-owned LFS.

**Non-Goals:**

- Shipping `git-lfs` in the shared image.
- Changing shared `pre-push` to chain LFS (would couple Devinfra to LFS).
- Implementing sql-to-arc adopt (#129) or product LFS overlay scripts in this PR.

## Decisions

1. **Delete the LFS removal loop** in `setup-git-hooks.sh` rather than guarding it behind a flag.
   - Alternatives: keep deletion (rejected — Devinfra must not manage LFS); call product restore script (rejected —
     avoids complex shared→product script hooks).

2. **No optional product script from postCreate.** Products that need LFS re-apply overlays themselves after shared hook
   install / rebuild (documented; product-owned).
   - Alternatives: soft-fail `install-dev-hooks.sh` invoke (rejected by lock-in).

3. **Docs-only path-overlay wording** in `quality.md` / `devcontainer.md`: `product.env` + CI inputs instead of
   `remoteEnv` for `MYPYPATH`.

## Risks / Trade-offs

- [Shared `pre-push` still overwrites product combined pre-push] → Mitigation: product re-runs its LFS overlay after
  shared setup (existing sql-to-arc pattern); not a Devinfra callback.
- [Fresh clone without product LFS step has no LFS hooks] → Mitigation: product docs / adopt issues; Devinfra stays
  LFS-agnostic by design.

## Migration Plan

1. Land this change on Devinfra `main` and sync `setup-git-hooks.sh` + docs.
2. sql-to-arc #129: `product.env`, verbatim JSON, keep/adjust product LFS scripts as manual/product process; update
   comments that claimed shared setup “strips LFS”.
