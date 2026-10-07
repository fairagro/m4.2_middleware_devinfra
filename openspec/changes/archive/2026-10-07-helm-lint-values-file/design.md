## Context

See proposal.md — Why. Lock-in for this change is **A+C**: Feature-PR `values_file` plus local `HELM_VALUES_FILE` so
commit-stage and CI share overlay semantics. Issue #294’s acceptance criteria require the reusable input; C alone would
not close that issue.

## Goals / Non-Goals

**Goals:**

- Optional overlay for Feature-PR lint/template without secrets in chart defaults.
- Same overlay behaviour for synced `scripts/run-helm-lint.sh` when contributors set `HELM_VALUES_FILE`.
- Empty overlay knobs preserve today’s bare-chart behaviour on both surfaces.

**Non-Goals:**

- Multi-file value lists.
- Auto-discovering a product overlay path (no magic `test_deploy/values.yaml` convention in the runner).
- Requiring products to set the overlay (opt-in only).

## Decisions

1. **CI:** `workflow_call` input `values_file` (string, default `""`).
2. **Local:** env `HELM_VALUES_FILE` (same relative-path semantics). Named differently on purpose: GHA inputs vs shell
   env; docs cross-link them as the parity pair.
3. **`-f` on both `helm lint` and `helm template`** when the overlay is set (both surfaces).
4. **Fail closed** if the overlay path is set but missing (both surfaces).
5. **No pre-commit `env:` hardcode** of a product path — products export `HELM_VALUES_FILE` in their shell / direnv /
   personal workflow when they want local overlay; CI passes `values_file:` in the Feature-PR caller.

## Risks / Trade-offs

- **[Risk]** Contributors forget to export `HELM_VALUES_FILE` while CI passes `values_file` → Mitigation: docs state the
  pair; bare chart remains the default on both sides when unset.
- **[Trade-off]** Env var is opt-in locally (not auto from a fixed path) → avoids wrong overlay in chart-less or multi-
  chart repos; products choose when to set it.

## Migration Plan

1. Land workflow + runner + docs on Devinfra `main`.
2. Products optionally pass `values_file` and/or document `HELM_VALUES_FILE` for local smoke.
