## MODIFIED Requirements

### Requirement: Foundation profile covers Slice-1 agent surfaces

The `foundation` profile `allow` list MUST include the fleet agent skill trees used by m4.2 eng repos (at least
`review-fixer`, `create-issue`, `code-review`, `issue-fixer`, `arctrl`, `gh`, `docker`, `hadolint`, and `uv`), the
matching Cursor commands and GitHub Copilot prompts for those skills, `.cursor/BUGBOT.md`,
`.github/copilot-instructions.md`, the skill-facing docs under `docs/` for those skills, `scripts/ai/**`,
`scripts/bin/m42-ai`, and the personal-token helper scripts/binaries those skills document (`scripts/dev-tokens.sh`,
`scripts/set-dev-tokens.sh`, and allowlisted `scripts/bin` wrappers required for that flow). After the pre-commit split,
`foundation` MUST also allow the helper files that Infra and foundation hooks need (at least commit-path-check, gitleaks
install/ignore, **actionlint install**, and the Node markdown / commitlint manifests used by those hooks). The
`foundation` profile MUST NOT include `.pre-commit-config.infrastructure.yaml` (that path MUST live on an Infra-only
profile such as `infra-consumer`), Renovate config/workflow, `versions.env` / `.python-version`, `.devcontainer/**`, the
**python-product** `.pre-commit-config.yaml`, or other python-product-only quality/CI surfaces. Documentation
(`docs/sync.md`) MUST state that Infra receives foundation (+ `gitops` / Infra-only profiles as wired) and that Renovate
on Infra is a later slice.

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

#### Scenario: Foundation allowlists actionlint install helper

- **WHEN** a contributor inspects the `foundation` profile allow list for quality install helpers
- **THEN** `scripts/install-actionlint.sh` is listed (alongside gitleaks install)
- **AND** `versions.env` remains off `foundation` (python-product / later Infra Renovate slice)
