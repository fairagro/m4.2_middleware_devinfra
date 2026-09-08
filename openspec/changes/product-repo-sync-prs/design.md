# Design: product-repo sync PRs

## Context

See `proposal.md`. Explore lock-ins: **A1** allowlist push from Devinfra; **B1′** sole SoT
`docs/synced-paths.global.md`; **C3** live PRs on `main` push; **D** shared bot token for Renovate + sync; **E1**
workflow + expanded allowlist + docs; **F** never middleware / OpenSpec specs / reusable workflow YAML.

## Goals / Non-Goals

**Goals:**

- Machine path set from one markdown allowlist; open PRs in three fixed targets.
- Main-push live sync + dispatch dry-run/skip.
- Expand allowlist to concrete quality/DC/hooks paths.

**Non-Goals:**

- Second sync-manifest.yml as competing SoT.
- Copying `reusable-*.yml` or OpenSpec specs/changes.
- Syncing into product `middleware/`.
- Multi-org or dynamic target discovery.
- Template-sync / Copier engines (A2/A3).

## Decisions

### D1 — Mechanism (A1)

**Choice:** Devinfra-hosted workflow + small script (`scripts/sync-products.sh` or Python under `scripts/ai` only if it
stays thin). For each target: clone or API-based branch, copy allowlisted files, open PR via `gh` with bot token.

**Alternatives:** Consumer-pull template-sync — inverted control; harder to keep allowlist-only.

### D2 — Parsing the allowlist (B1′)

**Choice:** Script extracts path/glob column from the allowlist table in `docs/synced-paths.global.md` (stable table
markers). Expand globs against Devinfra tree; apply hard-exclude denylist in code even if someone mis-lists a path.
Optional: fail CI if table cannot be parsed.

**Alternatives:** Generate markdown from YAML — rejected (two files). Embed HTML comments with JSON — possible later.

### D3 — Triggers (C3)

**Choice:** `on.push` to `main` (optionally path-filtered to allowlisted prefixes to reduce noise) opens PRs.
`workflow_dispatch`: `dry_run`, `skip_api`, `skip_sql_to_arc`, `skip_harvester`.

### D4 — Token (D)

**Choice:** Prefer one secret name documented for both (e.g. `DEVINFRA_BOT_TOKEN` or keep `RENOVATE_TOKEN` and document
reuse). Sync workflow reads the same secret. Scopes: contents R/W + PRs on three products + this repo as needed.

### D5 — PR shape

**Choice:** Branch `chore/devinfra-sync-<shortsha>` (or date); title `chore: sync shared Devinfra paths`; body links
source commit + allowlist. Update existing open sync PR branch if present (optional nicety).

## Risks / Trade-offs

- **[Markdown parse fragility]** → Mitigation: golden fixture test; fail closed; keep table format documented.
- **[Noisy main pushes]** → Mitigation: path filters; skip when no allowlisted files changed.
- **[Token blast radius]** → Mitigation: fine-grained PAT limited to four repos; docs for rotation.
- **[Overlay clobber]** → Mitigation: never list overlays; hard-exclude known overlay names.

## Migration Plan

1. Expand allowlist; land workflow + script; set bot secret; dispatch dry-run.
2. Enable live main-push; merge first sync PRs in products.
3. Rollback: disable workflow; products keep last synced trees.

## Open Questions

None — explore lock-ins bind this design.
