## Context

See proposal.md — Why. Lock-in: synced `.vscode/extensions.json` recommendations MUST match the Dev Container extension
list; Helm/`vs-kubernetes` settings only in `.vscode/settings.json` (no JSON settings duplicate); suppress
kubeconfig-not-found only.

## Goals / Non-Goals

**Goals:**

- Helm language mode for product + Devinfra template layouts via synced settings.
- Quiet kubeconfig toasts; keep kubectl-not-found alerts.
- One allowlisted recommendations file aligned with `devcontainer.json` + postCreate.

**Non-Goals:**

- Rewriting Helm templates for YAML LS.
- Requiring a real kubeconfig for chart editing.
- Duplicating Helm/`vs-kubernetes` keys under `devcontainer.json` `customizations.vscode.settings`.

## Decisions

1. **`.vscode/extensions.json` on allowlist** with the same IDs as Dev Container / postCreate (including Kubernetes
   Tools). Host checkouts get recommendations; Dev Container still installs via JSON + postCreate.
2. **Settings SoT = `.vscode/settings.json`** for `files.associations` and kubeconfig suppress — applies host and
   container workspace without drifting a second copy in `devcontainer.json`.
3. **Existing Prettier/hadolint keys** may remain in `devcontainer.json` `settings` for this change (out of scope to
   consolidate); do not add Helm/`vs-kubernetes` there.

## Risks / Trade-offs

- [Three places for extension IDs: JSON, postCreate, extensions.json] → Mitigation: docs + OpenSpec require the same
  set; tasks verify equality.
- [Language `helm` needs Kubernetes Tools installed] → Mitigation: recommend + Dev Container install.

## Migration Plan

Land in Devinfra → sync → products inherit settings/recommendations; rebuild Dev Container for extension install.
