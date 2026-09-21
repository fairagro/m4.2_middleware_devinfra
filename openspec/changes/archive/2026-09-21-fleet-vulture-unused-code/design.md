## Context

See `proposal.md` — Why. Explore lock-in for [#172](https://github.com/fairagro/m4.2_middleware_devinfra/issues/172):
**A1** vulture, **B1** hooks+CI (no IDE), **C1** shared policy via synced pre-commit/CI (no separate whitelist
fragment under D2), **D2** `--min-confidence 100` and **no** fleet whitelist, **E1** vulture only (#173 separate).

Bandit is the pattern: commit-stage hook + reusable CI, named IDE exception in `docs/quality.md`.

## Goals / Non-Goals

**Goals:**

- Single fleet unused-definition gate with identical hook/CI fail bar
- Code-review anti-dup updated so agents do not restate vulture hits
- Docs/parity table + principles Code Quality example updated

**Non-Goals:**

- import-linter (#173)
- IDE extension / workspace vulture settings
- Synced vulture whitelist file or lowering confidence for product comfort
- Changing Ruff unused-import rules

## Decisions

1. **Tool = vulture** — purpose-built for unused definitions; Ruff already covers unused imports.
2. **Surfaces = hooks + CI; IDE exception** — match Bandit; document in parity table.
3. **D2 policy via matching CLI args** — `uv run vulture middleware/ --min-confidence 100` (package root via CI
   `python_package_root` where applicable). No `.vulture` whitelist path on the sync allowlist.
4. **FP handling** — product `# noqa` / delete / use; do not fork synced `.pre-commit-config.yaml`. Document clearly so
   adopt pain is expected and owned by products.
5. **Dependency pin** — add `vulture` to the shared product quality uv dependency set that pre-commit/`uv run` already
   use (same pattern as bandit/ruff). Exact pin in apply.
6. **code-review** — “once landed” → owned for vulture; keep import-linter as once-landed.

## Risks / Trade-offs

- **[Risk] First product sync fails CI hard** → Mitigation: confidence 100 limits noise; products fix real dead code;
  issue comment / PR notes adopt expectation.
- **[Risk] False sense that all dead code is gated** → Mitigation: docs + skill keep judgment-only dead-code for cases
  outside vulture.
- **[Trade-off] No whitelist file** → Less fleet config to maintain; less escape hatch for awkward frameworks.

## Migration Plan

1. Land Devinfra: dep + hook + CI + docs + skill/docs anti-dup + OpenSpec deltas.
2. Sync to products; fix or noqa confidence-100 hits.
3. Do not change #173 in this PR.

## Open Questions

- Exact vulture version pin — choose current stable at apply time.
