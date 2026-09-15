## 1. Extension set alignment

- [x] 1.1 Add `ms-kubernetes-tools.vscode-kubernetes-tools` to `.devcontainer/devcontainer.json` and
      `scripts/devcontainer-post-create.sh`
- [x] 1.2 Create `.vscode/extensions.json` with `recommendations` matching that Dev Container / postCreate set exactly
- [x] 1.3 Allowlist `.vscode/extensions.json` in `docs/synced-paths.yaml` (and sync.md inventory if listed)

## 2. Workspace settings

- [x] 2.1 Add Helm `files.associations` (helmchart + helm layouts) and
      `vs-kubernetes.suppress-kubeconfig-not-found-alerts: true` to `.vscode/settings.json`
- [x] 2.2 Confirm those keys are not duplicated under `devcontainer.json` `customizations.vscode.settings`

## 3. Docs + specs

- [x] 3.1 Brief note in `docs/quality.md` and/or `docs/devcontainer.md` (Helm language mode + kubeconfig suppress)
- [x] 3.2 Apply deltas to `openspec/specs/shared-devcontainer-base/spec.md` and
      `openspec/specs/synced-consumer-paths/spec.md`
- [x] 3.3 `openspec validate ide-helm-template-language-mode --strict` and format/lint touched Markdown
