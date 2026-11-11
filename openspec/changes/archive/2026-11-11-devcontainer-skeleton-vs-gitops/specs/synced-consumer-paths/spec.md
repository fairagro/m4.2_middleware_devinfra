## ADDED Requirements

### Requirement: Dev Container paths stay on python-product only

The `python-product` profile MUST allow the shared product Dev Container entry files (at least
`.devcontainer/Dockerfile`, `.devcontainer/devcontainer.json`, `.devcontainer/docker-compose.yml`, and
`.devcontainer/starship.toml`). The `foundation`, `gitops`, and `infra-consumer` profiles MUST NOT allow any
`.devcontainer/**` path. The `infrastructure` target’s effective allow MUST NOT include `.devcontainer/**`. Product
targets that include `python-product` MAY sync those files; Infra MUST keep owning its GitOps Dev Container locally
until a dedicated adoption issue explicitly changes that contract. Documentation (`docs/sync.md` and/or
`docs/devcontainer.md`) MUST state this split and MUST list pin-ownership buckets: shared / foundation-eligible
(including Helm, minikube as the current product local-cluster tool, and git-lfs as shared-eligible),
python-product-only app/quality pins, and Infra-owned gitops pins (at least argocd, kind, and chart-testing / `ct`)
until adoption.

#### Scenario: Product profile lists Dev Container files

- **WHEN** a contributor inspects the `python-product` profile allow list
- **THEN** the shared `.devcontainer/` entry files above are listed
- **AND** those paths are absent from `foundation`, `gitops`, and `infra-consumer`

#### Scenario: Infra effective allow excludes Dev Container

- **WHEN** sync or a test resolves the effective allow for the `infrastructure` target
- **THEN** no `.devcontainer/` path is included
- **AND** docs state Infra keeps its fat GitOps Dev Container until an adoption issue says otherwise

#### Scenario: Pin ownership is documented

- **WHEN** a contributor reads sync or Dev Container docs for profile overlays
- **THEN** they find shared vs python-product vs Infra-owned pin buckets
- **AND** they learn argocd / kind / ct stay Infra-owned until adoption
- **AND** they learn product minikube→kind is a separate follow-up, not implied by this allowlist split

## MODIFIED Requirements

### Requirement: Foundation profile covers Slice-1 agent surfaces

The `foundation` profile `allow` list MUST include the fleet agent skill trees used by m4.2 eng repos (at least
`review-fixer`, `create-issue`, `code-review`, `issue-fixer`, `arctrl`, `gh`, `docker`, `hadolint`, and `uv`), the
matching Cursor commands and GitHub Copilot prompts for those skills, `.cursor/BUGBOT.md`,
`.github/copilot-instructions.md`, the skill-facing docs under `docs/` for those skills, `scripts/ai/**`,
`scripts/bin/m42-ai`, and the personal-token helper scripts/binaries those skills document (`scripts/dev-tokens.sh`,
`scripts/set-dev-tokens.sh`, and allowlisted `scripts/bin` wrappers required for that flow). After the pre-commit split,
`foundation` MUST also allow the helper files that Infra and foundation hooks need (at least commit-path-check, gitleaks
install/ignore, and the Node markdown / commitlint manifests used by those hooks). The `foundation` profile MUST NOT
include `.pre-commit-config.infrastructure.yaml` (that path MUST live on an Infra-only profile such as
`infra-consumer`), Renovate config/workflow, `versions.env` / `.python-version`, `.devcontainer/**`, the
**python-product** `.pre-commit-config.yaml`, or other python-product-only quality/CI surfaces. Documentation
(`docs/sync.md`) MUST state that Infra receives foundation (+ `gitops` / Infra-only profiles as wired), that Renovate on
Infra is a later slice, and that product `.devcontainer/**` is never part of the Infra sync set (Infra owns its GitOps
image until adoption).

#### Scenario: Foundation includes skills and m42-ai plumbing

- **WHEN** a contributor inspects the `foundation` profile allow list
- **THEN** agent skills (including `uv`), matching commands/prompts, skill docs, `scripts/ai/**`, and `m42-ai` / token
  helpers are listed
- **AND** Renovate / `versions.env` / Dev Container / python-product `.pre-commit-config.yaml` are not listed under
  `foundation`

#### Scenario: Infra target is foundation-only

- **WHEN** a contributor inspects the `infrastructure` target in `docs/synced-paths.yaml`
- **THEN** its `profiles` list includes `foundation` and MUST NOT include `python-product` (typically `foundation` +
  `gitops` + an Infra-only profile for `.pre-commit-config.infrastructure.yaml`)
- **AND** python-product repos list `foundation`, `python-product`, and `gitops` (or equivalent union that preserves
  today’s product hook set including helm-lint)
- **AND** no `.devcontainer/**` path appears on any profile used by the `infrastructure` target
