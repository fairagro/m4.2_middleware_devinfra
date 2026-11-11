## MODIFIED Requirements

### Requirement: Foundation profile covers Slice-1 agent surfaces

The `foundation` profile `allow` list MUST include the fleet agent skill trees used by m4.2 eng repos (at least
`review-fixer`, `create-issue`, `code-review`, `issue-fixer`, `arctrl`, `gh`, `docker`, `hadolint`, and `uv`), the
matching Cursor commands and GitHub Copilot prompts for those skills, `.cursor/BUGBOT.md`,
`.github/copilot-instructions.md`, the skill-facing docs under `docs/` for those skills, `scripts/ai/**`,
`scripts/bin/m42-ai`, and the personal-token helper scripts/binaries those skills document (`scripts/dev-tokens.sh`,
`scripts/set-dev-tokens.sh`, and allowlisted `scripts/bin` wrappers required for that flow). After the pre-commit split,
`foundation` MUST also allow the helper files that Infra and foundation hooks need (at least commit-path-check, gitleaks
install/ignore, **actionlint install**, **kubeconform install and runner**, and the Node markdown / commitlint manifests
used by those hooks). The `foundation` profile MUST also allow Renovate config/workflow (`renovate.json`,
`.github/workflows/renovate.yml`), Renovate docs (`docs/renovate.md`), and the pin file `versions.env`. The `foundation`
profile MUST NOT include `.pre-commit-config.infrastructure.yaml` (that path MUST live on an Infra-only profile such as
`infra-consumer`), `.python-version`, `.devcontainer/**`, the **python-product** `.pre-commit-config.yaml`, or other
python-product-only quality/CI surfaces. Documentation (`docs/sync.md`) MUST state that Infra receives foundation (+
`gitops` / Infra-only profiles as wired), including Renovate + `versions.env`, that unused pins do not install tools by
themselves, and that product `.devcontainer/**` is never part of the Infra sync set (Infra owns its GitOps image until
adoption).

#### Scenario: Foundation includes skills and m42-ai plumbing

- **WHEN** a contributor inspects the `foundation` profile allow list
- **THEN** agent skills (including `uv`), matching commands/prompts, skill docs, `scripts/ai/**`, and `m42-ai` / token
  helpers are listed
- **AND** `renovate.json`, `.github/workflows/renovate.yml`, `docs/renovate.md`, and `versions.env` are listed under
  `foundation`
- **AND** `.python-version`, Dev Container paths, and python-product `.pre-commit-config.yaml` are not listed under
  `foundation`

#### Scenario: Infra target is foundation-only

- **WHEN** a contributor inspects the `infrastructure` target in `docs/synced-paths.yaml`
- **THEN** its `profiles` list includes `foundation` and MUST NOT include `python-product` (typically `foundation` +
  `gitops` + an Infra-only profile for `.pre-commit-config.infrastructure.yaml`)
- **AND** python-product repos list `foundation`, `python-product`, and `gitops` (or equivalent union that preserves
  today’s product hook set including helm-lint)
- **AND** no `.devcontainer/**` path appears on any profile used by the `infrastructure` target

#### Scenario: Infra effective allow includes Renovate and versions.env

- **WHEN** sync or a test resolves the effective allow for the `infrastructure` target
- **THEN** `renovate.json`, `.github/workflows/renovate.yml`, and `versions.env` are included
- **AND** `.python-version` and `.devcontainer/**` paths are not included

#### Scenario: Foundation allowlists kubeconform install and runner

- **WHEN** a contributor inspects the `foundation` profile allow list for quality helpers
- **THEN** `scripts/install-kubeconform.sh` and `scripts/run-kubeconform.sh` are listed
- **AND** product helm-lint hooks are not required to call that runner
