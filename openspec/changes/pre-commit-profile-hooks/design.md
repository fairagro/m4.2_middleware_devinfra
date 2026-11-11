## Context

#351 (parent #347): Infra cannot take the python-product pre-commit blob. #350 already keeps `.pre-commit-config.yaml`
off foundation. Explore locked **composable fragments**, the hook map, **MVP C** (products + Infra wiring), and dropping
obsolete “Wave A” wording from live SoT.

## Goals / Non-Goals

**Goals**

- Editable SoT = profile fragments; deterministic compose → root `.pre-commit-config.yaml`
- Products: foundation ∪ python-product ∪ gitops (preserve helm-lint + middleware gates)
- Infra: foundation ± gitops via sync profiles; never python-product hooks
- Docs/specs/README: no “Wave A” / “Wave-A” in live SoT this change touches
- Migration note for the three python-product consumers

**Non-Goals**

- Implementing actionlint (#353) or kubeconform (#348) hooks (slots/docs only if needed)
- Renovate on Infra (#354)
- Rewriting archive OpenSpec history that still says “Wave A”
- Changing CI reusable workflow matrices beyond what’s required for compose docs

## Decisions

1. **Fragment layout** — Prefer `.pre-commit.d/{foundation,python-product,gitops}.yaml` (or `.yml`) as partial `repos:`
   lists the compose tool merges. Exact filenames locked at apply if a cleaner layout appears.
2. **Compose** — Small Devinfra script (e.g. `scripts/compose-pre-commit.py`) reads selected fragments and writes root
   `.pre-commit-config.yaml`. Checked-in root stays the install entrypoint for `pre-commit` / git hooks. CI or a
   pre-commit meta-check MAY verify root matches compose output (apply decides; prefer fail-closed if cheap).
3. **Sync profiles** — Add `gitops` profile for the gitops fragment (+ any gitops-only runners already needed). Update
   targets: products → foundation + python-product + gitops; infrastructure → foundation + gitops (helm-lint on Infra
   when that fragment is wanted; if Infra should stay foundation-only for hooks first, apply MAY stage gitops onto Infra
   as opt-in — default locked MVP C includes gitops on Infra).
4. **Generated root on sync** — Sync the composed root appropriate to each target (product union vs Infra compose), not
   a single blob to all consumers. Fragments sync by owning profile so orphans/deletes stay per-target.
5. **Wave A cleanup** — Replace live README / `product-repo-sync` (and any other touched live docs) wording with
   profile/allowlist language. No archive rewrites.

## Risks / Trade-offs

- **[Risk] Dual SoT (hand-edited root vs fragments)** → Mitigation: docs + optional compose-check; PR template/quality
  docs say edit fragments first.
- **[Risk] Infra gets gitops helm-lint without charts/`helm` pin parity** → Mitigation: existing helm-lint no-op without
  charts; document `HELM_VERSION` / runner expectations in quality/sync docs.
- **[Risk] Product sync churn on first compose** → Mitigation: compose should be byte-stable vs today’s root aside from
  intentional fragment comments; spot-check hook ids.
- **[Trade-off] Third sync profile (`gitops`)** vs stuffing helm into foundation → Profiles stay honest; products take
  three profiles.

## Migration Plan

1. Land fragments + compose; regenerate Devinfra root; verify hook ids match prior config for product union.
2. Update `docs/synced-paths.yaml` profiles/targets; sync products get new fragments + composed root.
3. Enable Infra sync of foundation+gitops hook artifacts (still default-skip live Infra push until operators unskip).
4. Document product cutover (no hand-edit of root); remove Wave A strings from live SoT.

## Open Questions

- None for propose — apply may choose compose-check strictness and whether Infra gitops is default-on in YAML targets vs
  documented optional second compose flavor (default: **on**, per MVP C).
