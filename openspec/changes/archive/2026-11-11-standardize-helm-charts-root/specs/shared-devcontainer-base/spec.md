## MODIFIED Requirements

### Requirement: Synced IDE settings for Helm templates and kubeconfig alerts

Synced `.vscode/settings.json` MUST set `files.associations` so paths under `**/charts/**/templates/**` with extensions
`.yaml`, `.yml`, and `.tpl` use language mode `helm`. During the migration window it MUST also keep the same
associations for `**/helmchart/**/templates/**` and `**/helm/**/templates/**`. It MUST set
`vs-kubernetes.suppress-kubeconfig-not-found-alerts` to `true`. It MUST NOT set
`vs-kubernetes.suppress-kubectl-not-found-alerts` solely for this change. Those Helm/`vs-kubernetes` keys MUST live in
`.vscode/settings.json` and MUST NOT be duplicated under `.devcontainer/devcontainer.json`
`customizations.vscode.settings`. Documentation MUST note that Helm templates use language `helm` via Kubernetes Tools
and that missing-kubeconfig alerts are suppressed for chart editing without a cluster config. Documentation MUST state
that **`charts/`** is the canonical chart root for IDE associations.

#### Scenario: Helm associations and kubeconfig suppress in workspace settings

- **WHEN** a contributor inspects synced `.vscode/settings.json`
- **THEN** `files.associations` maps `charts/**/templates` (and during migration `helmchart` / `helm` template globs) to
  `helm`
- **AND** `vs-kubernetes.suppress-kubeconfig-not-found-alerts` is `true`
- **AND** those keys are absent from `devcontainer.json` `customizations.vscode.settings`
