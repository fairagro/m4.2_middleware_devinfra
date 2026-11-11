## Context

See proposal.md — Why. `scripts/sync-products.py` loads a flat `allow` from `docs/synced-paths.yaml` and copies the same
file set to `api` / `sql_to_arc` / `harvester`. Explore lock-in: layout **B** (profiles in one YAML); Slice 1 =
skills/commands/prompts/skill-docs + `scripts/ai`/`m42-ai`/token helpers + `uv` skill; Renovate deferred to #354.

## Goals / Non-Goals

**Goals:**

- Profile-aware path resolution from a single SoT file
- Infra target receives foundation only; products keep today’s coverage as foundation ∪ python-product
- Documented dry-run / skip for `infrastructure`

**Non-Goals:**

- Granting Infra bot token / landing Renovate (#354)
- Hook or Dev Container sync (#351 / #352)
- Changing orphan-delete or SYNC-FOLLOWUP mechanics beyond per-target file sets

## Decisions

1. **YAML shape (B):**

   ```yaml
   exclude: [...]
   overlays: [...]
   profiles:
     foundation:
       allow: [...]
     python-product:
       allow: [...]
   targets:
     api: { profiles: [foundation, python-product] }
     sql_to_arc: { profiles: [foundation, python-product] }
     harvester: { profiles: [foundation, python-product] }
     infrastructure: { profiles: [foundation] }
   ```

   Shared `exclude` / `overlays` apply to every target. Effective allow = ordered union of named profiles (dedupe).

2. **No top-level flat `allow` after migration** — avoids dual SoT. Loader fails closed if `profiles` missing or a
   target references an unknown profile. Alternative rejected: keep flat `allow` plus optional profiles (two ways to
   mean “product set”).

3. **TARGETS in YAML `targets` + Python fallback** — prefer reading repos/profile lists from YAML so Infra is
   SoT-driven; Python keeps orchestration (git/gh). Minimal: YAML profiles + `targets` map with `repo` + `profiles`.

4. **`--list-files` / push gate:** default resolves **product union** (foundation ∪ python-product) so the “did
   allowlist content change?” gate still matches what products receive. Add `--target KEY` (or `--profile`) for
   Infra-specific listing/orphan math when syncing that consumer.

5. **Orphans per target:** orphan delta uses that target’s resolved file set at base vs HEAD (Infra must not `git rm`
   Wave-A paths it never owned).

6. **Foundation membership (Slice 1):** skills trees (review-fixer, create-issue, code-review, issue-fixer, arctrl, gh,
   docker, hadolint, uv), matching `.cursor/commands` / `.github/prompts`, `.cursor/BUGBOT.md`,
   `.github/copilot-instructions.md`, skill docs under `docs/`, `scripts/ai/**`, `scripts/bin/m42-ai`,
   `scripts/dev-tokens.sh`, `scripts/set-dev-tokens.sh`, and bin wrappers those helpers require (`scripts/bin/gh`,
   `scripts/bin/git` if already allowlisted for token flow). Do **not** put `versions.env`, Renovate, `.devcontainer`,
   `.pre-commit-config.yaml`, or quality/CI Wave-A docs into foundation.

7. **Live Infra sync** may no-op on auth until #354; dry-run MUST work without Infra token. Default
   `skip_infrastructure` on push MAY be true until operators enable it (document); dispatch can unskip for dry-run.

## Risks / Trade-offs

- [YAML migrate breaks old loader] → Single PR updates loader + YAML together; validate in CI/tests
- [Orphan deletes wrong if gate uses union for Infra] → Per-target resolve for sync/orphan paths
- [Infra gets skills without uv runtime] → Document that `m42-ai` needs uv on PATH / Dev Container later (#352); Slice 1
  still ships plumbing files
- [review-fixer synced-path matching] → Consumers still treat union of profiles that apply to them as read-only;
  document “product = both profiles”

## Migration Plan

1. Land profile YAML + loader + Infra target (default skip on push until ready)
2. Dry-run Infra; note on Infra#80
3. #354 bot token + optional unskip for live foundation sync
