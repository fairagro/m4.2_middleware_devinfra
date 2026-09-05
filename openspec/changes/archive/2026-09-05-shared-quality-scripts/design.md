# Shared quality scripts — Design

## Context

See proposal.md — Why. This repo already has markdownlint + Prettier ignores for vendor skills; no
`.pre-commit-config.yaml`, quality scripts, or `.bandit` yet. Product repos (primary reference:
`m4.2_advanced_middleware_api`) already use the intended pattern. Package root is `middleware/` (`docs/conventions.md`);
this Devinfra tree has none.

## Goals / Non-Goals

**Goals:**

- Ship a syncable commit-stage + pre-push pre-commit skeleton and helper scripts.
- Keep CST runner shared and parameterized; product Docker paths stay local.
- Align vendor excludes and `middleware/` targeting with existing conventions.

**Non-Goals:**

- Installing pre-push as a git hook (#9) or Dev Container postCreate wiring (#10).
- Running Python quality gates as CI for this Devinfra repo’s empty `middleware/` tree.
- Syncing into product repos in this change (later consumer PRs).

## Decisions

1. **Skeleton mirrors API commit/pre-push split**  
   Commit-stage: formatting/lint/secret/static analysis. Pre-push: `pytest` + CST.  
   **Why:** Matches what products already run; avoids surprising consumers.  
   **Alt:** Single stage for everything — rejected (slow tests on every commit).

2. **`quality-check.sh` / `quality-fix.sh` invoke commit-stage only**  
   Wrap `pre-commit run` (check vs fix) without `--hook-stage pre-push`.  
   **Why:** Issue done-when and scripts stay fast; pre-push stays for push / explicit runs.

3. **CST runner is a thin shared script with env/args for product params**  
   Document required inputs: Dockerfile path, image tag, test YAML glob/dir. Defaults may match common `docker/` layout
   but MUST be overridable.  
   **Why:** One script to sync; products differ slightly.  
   **Alt:** Hardcode API paths — rejected (breaks other products).

4. **`.bandit` at repo root; markdownlint configs already present**  
   Add `.bandit` for `bandit -c`. Keep existing markdownlint files; only adjust if pre-commit needs the same vendor
   excludes (already in ignore files).  
   **Why:** Issue lists them; markdownlint work mostly done in #6.

5. **Pre-commit targets `middleware/` for Python tools; exclude vendor skill trees**  
   Same excludes as markdownlint/Prettier for `.agents/skills/gh` and `scan-secrets`.  
   **Why:** Path conventions + vendor pin contract.

6. **Devinfra local use**  
   Scripts and config live here for sync. Document that Python hooks expect consumer `middleware/`; in this repo,
   commit-stage may still run non-Python hooks (whitespace, markdownlint, ggshield when keyed).  
   **Why:** Avoid fake empty package trees.

## Risks / Trade-offs

- **[Risk] Skeleton drifts from API before sync** → Mitigation: copy from API as source of truth in tasks; note
  follow-up align with sql_to_arc / harvester.
- **[Risk] CST / Docker unavailable in some environments** → Mitigation: pre-push stage only; document that CST needs
  Docker + `container-structure-test` on PATH (Dev Container later).
- **[Risk] ggshield needs `GITGUARDIAN_API_KEY`** → Mitigation: same token helpers as today; hook fails closed when
  missing (document).

## Migration Plan

1. Land files in Devinfra; document sync + install in README/docs.
2. Consumers copy/sync in a later wave; tweak CST params and confirm `middleware/` layout.
3. Rollback: remove synced files in consumer; Devinfra can revert the change commit.
