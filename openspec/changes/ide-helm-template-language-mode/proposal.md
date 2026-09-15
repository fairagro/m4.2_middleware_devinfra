## Why

Helm chart templates under `helmchart/**/templates/` and `helm/**/templates/` are Go templates. Synced Red Hat YAML
treats `{{ … }}` as YAML and reports false positives. Kubernetes Tools provides language mode `helm`, but without
suppressing kubeconfig-missing alerts it toasts noise in Dev Containers that have no cluster config. Recommendations and
settings must land in synced Devinfra paths so products inherit on sync
([#118](https://github.com/fairagro/m4.2_middleware_devinfra/issues/118)).

## What Changes

- Add `ms-kubernetes-tools.vscode-kubernetes-tools` to the shared Dev Container extension set (JSON + postCreate).
- Add synced `.vscode/extensions.json` whose `recommendations` match that Dev Container set (same IDs), and allowlist it
  in `docs/synced-paths.yaml`.
- Add synced `.vscode/settings.json` `files.associations` for Helm template paths and
  `vs-kubernetes.suppress-kubeconfig-not-found-alerts: true` (do **not** suppress kubectl-not-found alerts).
- Do **not** duplicate those Helm/`vs-kubernetes` settings under `devcontainer.json` `customizations.vscode.settings`.
- Brief docs note (quality / Dev Container).

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-devcontainer-base`: shared IDE extension set includes Kubernetes Tools; synced `.vscode/extensions.json`
  recommendations match that set; synced `.vscode/settings.json` owns Helm associations and kubeconfig-alert suppress
  (not duplicated in `devcontainer.json` settings).
- `synced-consumer-paths`: `.vscode/extensions.json` on the product sync allowlist.

## Impact

- Synced `.vscode/settings.json`, new `.vscode/extensions.json`, `.devcontainer/devcontainer.json`,
  `scripts/devcontainer-post-create.sh`, `docs/synced-paths.yaml`, short docs.
- Products pick up on next sync; no product hand-edits of allowlisted IDE files.
- Issue: [#118](https://github.com/fairagro/m4.2_middleware_devinfra/issues/118).
