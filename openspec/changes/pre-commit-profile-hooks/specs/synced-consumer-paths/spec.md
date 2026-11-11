## MODIFIED Requirements

### Requirement: Foundation profile covers Slice-1 agent surfaces

The `foundation` profile `allow` list MUST include the fleet agent skill trees used by m4.2 eng repos (at least
`review-fixer`, `create-issue`, `code-review`, `issue-fixer`, `arctrl`, `gh`, `docker`, `hadolint`, and `uv`), the
matching Cursor commands and GitHub Copilot prompts for those skills, `.cursor/BUGBOT.md`,
`.github/copilot-instructions.md`, the skill-facing docs under `docs/` for those skills, `scripts/ai/**`,
`scripts/bin/m42-ai`, and the personal-token helper scripts/binaries those skills document (`scripts/dev-tokens.sh`,
`scripts/set-dev-tokens.sh`, and allowlisted `scripts/bin` wrappers required for that flow). After the pre-commit
profile split, `foundation` MUST also allow the **foundation** pre-commit fragment(s) and any foundation-only composed
root config path the design documents for Infra (or the shared compose inputs needed to build it). The `foundation`
profile MUST NOT include Renovate config/workflow, `versions.env` / `.python-version`, `.devcontainer/**`, the
**python-product** pre-commit fragment, or other python-product-only quality/CI surfaces. Documentation (`docs/sync.md`)
MUST state that Infra / foundation-only consumers receive this profile (plus optional `gitops` when wired) and that
Renovate on Infra is a later slice.

#### Scenario: Foundation includes skills and m42-ai plumbing

- **WHEN** a contributor inspects the `foundation` profile allow list
- **THEN** agent skills (including `uv`), matching commands/prompts, skill docs, `scripts/ai/**`, and `m42-ai` / token
  helpers are listed
- **AND** Renovate / `versions.env` / Dev Container / python-product pre-commit fragment are not listed under
  `foundation`

#### Scenario: Infra target is foundation-only

- **WHEN** a contributor inspects the `infrastructure` target in `docs/synced-paths.yaml`
- **THEN** its `profiles` list is `foundation` or `foundation` + `gitops` (never `python-product`)
- **AND** python-product repos list `foundation`, `python-product`, and `gitops` (or equivalent union that preserves
  today’s product hook set including helm-lint)

## ADDED Requirements

### Requirement: Pre-commit fragments sync by profile

`docs/synced-paths.yaml` MUST allowlist the pre-commit **fragment** paths and compose helper (if any) under the profiles
that own them (`foundation` / `python-product` / `gitops`). The composed root `.pre-commit-config.yaml` MAY be synced as
the effective consumer artifact when that is the documented install entrypoint; when synced, its profile membership MUST
match the consumer matrix (product union vs Infra foundation±gitops) so Infra never receives the python-product hook
set. Live docs MUST NOT use obsolete “Wave A” / “Wave-A” labels for these paths.

#### Scenario: Fragments appear on the right profiles

- **WHEN** a contributor inspects allow entries for pre-commit fragments
- **THEN** the foundation fragment is under `foundation`, the python-product fragment under `python-product`, and the
  gitops fragment under `gitops` (or documented equivalent)
- **AND** Infra’s effective allow does not include the python-product fragment
