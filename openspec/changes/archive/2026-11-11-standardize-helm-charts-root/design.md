## Context

See proposal.md — Why. Today `scripts/run-helm-lint.sh` and the helm-lint hook discover only `helmchart/*/Chart.yaml`
and `helm/*/Chart.yaml`; `check-yaml` excludes and `.vscode` associations match those two roots; CI docs exemplify
`helmchart/`. Consumer renames (api#653, harvester#591, infra#81) are separate. Explore lock-in: **migration A** —
temporary dual discovery, then strip legacy in a follow-up.

## Goals / Non-Goals

**Goals:**

- Make `charts/<chart>/` the documented and discovered canonical root in Devinfra SoT
- Keep API/Harvester working after sync without waiting for their renames
- Keep OpenSpec / docs / IDE / hooks aligned

**Non-Goals:**

- Renaming trees in consumer repos
- Adding `helmcharts/` discovery
- Removing legacy `helm`/`helmchart` in this change (follow-up after consumers + sync)
- Changing `reusable-helm-lint.yml` inputs beyond docs (callers pass explicit `chart_dir`)

## Decisions

1. **Dual discovery order:** glob `charts/*/Chart.yaml` first, then legacy `helmchart/*/Chart.yaml` and
   `helm/*/Chart.yaml`. Deduplicate by resolved path if a checkout somehow has both (unlikely).
   - Alternative rejected: hard cut to `charts/` only (breaks synced products until rename).
2. **No `helmcharts/` alias:** Infra renames to `charts/` (infra#81); Devinfra must not teach a third root.
3. **Hook `files` filter:** `^(charts|helm|helmchart)/` during migration so chart edits still trigger the hook.
4. **Nested chart `charts/` deps:** discovery stays **one** path segment under the repo-root chart root
   (`charts/<name>/Chart.yaml` only). Dependency subdirs inside a chart (`…/<chart>/charts/<dep>/`) are not repo roots —
   same rule as today’s one-segment discovery.
5. **Legacy removal:** linked follow-up issue after consumer renames merge and sync; not tasks in this change’s done
   criteria beyond documenting deprecation.

## Risks / Trade-offs

- [Dual roots linger] → Docs mark deprecated; follow-up issue tracks strip; do not expand aliases
- [Confusion with in-chart `charts/` dependency dir] → Keep one-segment discovery; document in quality.md
- [CI examples change before products rename] → Examples show `charts/`; note legacy callers until rename PRs land

## Migration Plan

1. Land Devinfra change (this): discovery + docs + specs; sync to products
2. Consumer renames to `charts/` (existing issues)
3. Follow-up: remove `helm`/`helmchart` from runner, hook filters, vscode, specs
