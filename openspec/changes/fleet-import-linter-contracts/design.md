## Context

See `proposal.md` — Why. Explore lock-in for [#173](https://github.com/fairagro/m4.2_middleware_devinfra/issues/173):
**A3** baseline + product overlay, **B1** hooks+CI (no IDE), **C3** synced baseline + overlay path, **D1** pydeps
non-gate, **E1** import-linter only. Pack Import policy into contracts **where mechanical**: acyclic + exclude
TYPE_CHECKING. Product follow-ups filed for API / harvester / sql-to-arc overlays.

## Goals / Non-Goals

**Goals:**

- Fleet SoT acyclic gate for `middleware` sibling packages
- Documented overlay path for layers/forbidden/independence
- Code-review treats import-linter as toolchain-owned
- Wrapper/hook/CI parity if upstream accepts one config file

**Non-Goals:**

- Shared fleet layer package names
- pydeps as a gate
- Encoding relative-import / module-level / `sys.path` rules in import-linter

## Decisions

1. **Baseline file** — synced `.importlinter` (INI) with `root_package = middleware`,
   `exclude_type_checking_imports = True`, and `type = acyclic_siblings` with `ancestors = middleware`.
2. **Overlay file** — product-owned `.importlinter.product` (or documented name) listed under `synced-paths.yaml`
   `overlays`; products add `layers` / `forbidden` / `independence` contracts there.
3. **Runner** — small `scripts/run-import-linter.sh` (synced) merges baseline + overlay into a temp config when overlay
   exists, then runs `lint-imports`; used by pre-commit and CI so policy stays identical.
4. **Surfaces** — commit-stage + reusable CI; IDE exception like Bandit/vulture.
5. **pydeps** — mention in docs as optional visualization only.
6. **Dependency** — pin `import-linter` in Devinfra quality deps; products add the same class of dep locally.

## Risks / Trade-offs

- **[Risk] Merge wrapper drifts from upstream config schema** → Keep merge minimal (concat contract sections); pin
  import-linter; document overlay format.
- **[Risk] Products delay overlays** → Baseline still gates cycles; follow-up issues track layers.
- **[Trade-off] Incomplete Import-policy coverage** → Honest docs; code-review keeps judgment for non-graph rules.

## Migration Plan

1. Land Devinfra baseline + runner + hooks/CI + docs + skill anti-dup.
2. Sync; products fix acyclic failures.
3. Product overlay issues (already filed) add layers/forbidden.

## Open Questions

- Exact overlay filename (`.importlinter.product` vs `.importlinter.d/*.ini`) — choose at apply; default
  `.importlinter.product`.
- import-linter version pin — choose current stable at apply.
