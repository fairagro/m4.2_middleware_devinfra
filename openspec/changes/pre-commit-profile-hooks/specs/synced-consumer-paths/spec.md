## MODIFIED Requirements

### Requirement: Foundation profile covers Slice-1 agent surfaces

The `foundation` profile `allow` list MUST include the fleet agent skill trees used by m4.2 eng repos (at least
`review-fixer`, `create-issue`, `code-review`, `issue-fixer`, `arctrl`, `gh`, `docker`, `hadolint`, and `uv`), the
matching Cursor commands and GitHub Copilot prompts for those skills, `.cursor/BUGBOT.md`,
`.github/copilot-instructions.md`, the skill-facing docs under `docs/` for those skills, `scripts/ai/**`,
`scripts/bin/m42-ai`, and the personal-token helper scripts/binaries those skills document (`scripts/dev-tokens.sh`,
`scripts/set-dev-tokens.sh`, and allowlisted `scripts/bin` wrappers required for that flow). After the pre-commit split,
`foundation` MUST also allow `.pre-commit-config.infrastructure.yaml` and the helper files that Infra hooks need (at
least commit-path-check, gitleaks install/ignore, and the Node markdown / commitlint manifests used by those hooks). The
`foundation` profile MUST NOT include Renovate config/workflow, `versions.env` / `.python-version`, `.devcontainer/**`,
the **python-product** `.pre-commit-config.yaml`, or other python-product-only quality/CI surfaces. Documentation
(`docs/sync.md`) MUST state that Infra receives foundation (+ optional `gitops`) and that Renovate on Infra is a later
slice.

#### Scenario: Foundation includes skills and m42-ai plumbing

- **WHEN** a contributor inspects the `foundation` profile allow list
- **THEN** agent skills (including `uv`), matching commands/prompts, skill docs, `scripts/ai/**`, and `m42-ai` / token
  helpers are listed
- **AND** Renovate / `versions.env` / Dev Container / python-product `.pre-commit-config.yaml` are not listed under
  `foundation`

#### Scenario: Infra target is foundation-only

- **WHEN** a contributor inspects the `infrastructure` target in `docs/synced-paths.yaml`
- **THEN** its `profiles` list is `foundation` or `foundation` + `gitops` (never `python-product`)
- **AND** python-product repos list `foundation`, `python-product`, and `gitops` (or equivalent union that preserves
  today’s product hook set including helm-lint)

## ADDED Requirements

### Requirement: Pre-commit roots sync by consumer matrix

`docs/synced-paths.yaml` MUST allowlist `.pre-commit-config.yaml` under a profile used by python-product targets and
`.pre-commit-config.infrastructure.yaml` under `foundation` (or equivalent). The helm lint runner MUST be allowlisted
under `gitops` (or another profile included by both product and Infra targets). Live docs MUST NOT use obsolete lettered
“wave” adopt labels for these paths.

#### Scenario: Pre-commit roots appear on the right profiles

- **WHEN** a contributor inspects allow entries for pre-commit configs
- **THEN** the product root is not on Infra’s effective allow
- **AND** the Infra root is on foundation (reachable by the infrastructure target)
- **AND** `scripts/run-helm-lint.sh` is available to both product and Infra targets via their profile unions
