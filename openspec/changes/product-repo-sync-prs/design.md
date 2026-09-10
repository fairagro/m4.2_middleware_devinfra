# Design: product-repo sync PRs

## Context

See `proposal.md`. Explore lock-ins: **A1** allowlist push from Devinfra; **B1′** sole SoT
`docs/synced-paths.yaml`; **C3** live PRs on `main` push; **D** shared bot token for Renovate + sync; **E1**
workflow + expanded allowlist + docs; **F** never middleware / OpenSpec specs / reusable workflow YAML.

## Goals / Non-Goals

**Goals:**

- Machine path set from one YAML allowlist; open PRs in three fixed targets.
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

**Choice:** `docs/synced-paths.yaml` is the sole path SoT (`allow`, `exclude`, optional `overlays`). The sync script
loads it with **PyYAML** from the Devinfra `uv` project environment (`uv run python scripts/sync-products.py`). CI
installs the same lock via `uv sync --frozen`. Expand globs against the Devinfra tree; apply `exclude` even if a path
is also under `allow`. No second hardcoded path/exclude list in the script.

**Alternatives:** Markdown table as SoT — rejected (fragile parse). Optional stdlib YAML subset — rejected (environment
is always `uv`-managed; declare PyYAML). Script-enforced “required exclude” constants — rejected (second SoT).

### D3 — Triggers (C3)

**Choice:** `on.push` to `main` with **no** YAML `paths:` filter (avoids a second hand-edited path list). Noise
reduction: script `--skip-if-unchanged` exits when `git diff HEAD~1..HEAD` intersects no allowlisted file.
`workflow_dispatch`: `dry_run`, `skip_api`, `skip_sql_to_arc`, `skip_harvester`.

### D4 — Token (D)

**Choice:** One repository Actions secret `DEVINFRA_BOT_TOKEN` for Renovate and product sync (combined scopes). No
`RENOVATE_TOKEN` alias/fallback. Local developer `gh` uses only `GH_TOKEN` (no `GITHUB_TOKEN` fallback). Automatic
`secrets.GITHUB_TOKEN` remains for same-repo reusable release/Helm/GHCR jobs where it is enough.

### D5 — PR shape

**Choice:** Branch `chore/devinfra-sync-<shortsha>` (or date); title `chore: sync shared Devinfra paths`; body links
source commit + allowlist. Update existing open sync PR branch if present (optional nicety).

## Risks / Trade-offs

- **[Markdown parse fragility]** → Mitigation: golden fixture test; fail closed; keep table format documented.
- **[Noisy main pushes]** → Mitigation: `--skip-if-unchanged` against allowlist (not a second YAML path list).
- **[Token blast radius]** → Mitigation: fine-grained PAT limited to four repos; docs for rotation.
- **[Overlay clobber]** → Mitigation: never list overlays; hard-exclude known overlay names.

## Migration Plan

1. Expand allowlist; land workflow + script; set bot secret; dispatch dry-run.
2. Enable live main-push; merge first sync PRs in products.
3. Rollback: disable workflow; products keep last synced trees.

## Open Questions

None — explore lock-ins bind this design.
