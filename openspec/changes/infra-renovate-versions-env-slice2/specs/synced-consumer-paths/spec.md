# Spec Delta

## MODIFIED Requirements

### Requirement: Synced paths allowlist document

The repository MUST provide `docs/synced-paths.yaml` as the **sole** canonical path SoT synced from Devinfra into
consumer repos. The YAML MUST expose:

- `profiles` — a map of named profiles (at least `foundation` and `python-product`), each with an `allow` list
  (paths/globs)
- `targets` — a map of sync consumer keys to `{ repo, profiles: [...] }` (at least the three python-product repos and
  `infrastructure`)
- `exclude` — never copy
- optional `overlays` — product-local exceptions

There MUST NOT be a second hand-maintained sync path list and MUST NOT retain a top-level flat `allow` alongside
`profiles` after this change. The same file MUST remain the source of truth for (1) paths consumers MUST NOT hand-edit
after sync (for the profiles that apply to that consumer), (2) `/review-fixer` read-only synced trees in product
checkouts (effective allow = union of that consumer’s profiles), and (3) product-repo sync automation path selection.
The union of `foundation` and `python-product` allows MUST cover concrete paths or globs for all shipped shared surfaces
currently required for python-product consumers (including AI stack, Renovate artifacts, personal-token helpers, quality
scripts/hooks, Dev Container shared fragments, `docker/Dockerfile.product-app.base`, `.github/workflows/codeql.yml`, and
related docs). `exclude` / `overlays` MUST cover at least: product `middleware/`, `openspec/specs/**`,
`openspec/changes/**`, reusable CI workflow YAML (`reusable-*.yml`), and documented overlays (e.g.
`docs/surface-quality-bar.md`, `openspec/principles.md`, `AGENTS.md`). The root `README.md` Docs index MUST link to this
YAML. Sync of this allowlist MUST NOT overwrite product-local overlay files.

#### Scenario: Contributor looks up what not to edit after sync

- **WHEN** a contributor opens `docs/synced-paths.yaml` in Devinfra or after sync into a product repo
- **THEN** they find profile-based allowlists of Devinfra-canonical synced paths
- **AND** they find named product-local overlay paths that remain editable in consumers

#### Scenario: README indexes the allowlist

- **WHEN** a contributor reads the root `README.md` Docs section
- **THEN** they find a link to `docs/synced-paths.yaml`

#### Scenario: Renovate artifacts are on the allowlist

- **WHEN** a contributor checks whether Renovate config or workflow may be hand-edited in a consumer after sync
- **THEN** `renovate.json` and `.github/workflows/renovate.yml` appear under the `foundation` profile (reachable by
  python-product targets and by `infrastructure`)
- **AND** they learn shared Renovate changes land in Devinfra first

#### Scenario: CodeQL workflow is on the allowlist

- **WHEN** a contributor checks whether `.github/workflows/codeql.yml` may be hand-edited in a product repo after sync
- **THEN** that path appears under a profile used by python-product targets
- **AND** they learn shared CodeQL changes land in Devinfra first

#### Scenario: Allowlist is the only sync path SoT

- **WHEN** sync automation or a contributor looks for “what files are copied to products”
- **THEN** `docs/synced-paths.yaml` is the only hand-maintained path list
- **AND** hard excludes for OpenSpec specs trees and `middleware/` are documented there
- **AND** path selection is expressed via `profiles` + `targets`, not a separate manifest

### Requirement: Foundation profile covers Slice-1 agent surfaces

The `foundation` profile `allow` list MUST include the fleet agent skill trees used by m4.2 eng repos (at least
`review-fixer`, `create-issue`, `code-review`, `issue-fixer`, `arctrl`, `gh`, `docker`, `hadolint`, and `uv`), the
matching Cursor commands and GitHub Copilot prompts for those skills, `.cursor/BUGBOT.md`,
`.github/copilot-instructions.md`, the skill-facing docs under `docs/` for those skills, `scripts/ai/**`,
`scripts/bin/m42-ai`, and the personal-token helper scripts/binaries those skills document (`scripts/dev-tokens.sh`,
`scripts/set-dev-tokens.sh`, and allowlisted `scripts/bin` wrappers required for that flow). After the pre-commit split,
`foundation` MUST also allow the helper files that Infra and foundation hooks need (at least commit-path-check, gitleaks
install/ignore, and the Node markdown / commitlint manifests used by those hooks). The `foundation` profile MUST also
allow Renovate config/workflow (`renovate.json`, `.github/workflows/renovate.yml`), Renovate docs (`docs/renovate.md`),
and the foundation pin file (`versions.foundation.env`). The `foundation` profile MUST NOT include
`.pre-commit-config.infrastructure.yaml` (that path MUST live on an Infra-only profile such as `infra-consumer`), the
python-product pin file `versions.env`, `.python-version`, `.devcontainer/**`, the **python-product**
`.pre-commit-config.yaml`, or other python-product-only quality/CI surfaces. Documentation (`docs/sync.md`) MUST state
that Infra receives foundation (+ `gitops` / Infra-only profiles as wired), including Renovate + foundation pins, and
that product `.devcontainer/**` is never part of the Infra sync set (Infra owns its GitOps image until adoption).

#### Scenario: Foundation includes skills and m42-ai plumbing

- **WHEN** a contributor inspects the `foundation` profile allow list
- **THEN** agent skills (including `uv`), matching commands/prompts, skill docs, `scripts/ai/**`, and `m42-ai` / token
  helpers are listed
- **AND** `renovate.json`, `.github/workflows/renovate.yml`, `docs/renovate.md`, and `versions.foundation.env` are
  listed under `foundation`
- **AND** `versions.env`, `.python-version`, Dev Container paths, and python-product `.pre-commit-config.yaml` are not
  listed under `foundation`

#### Scenario: Infra target is foundation-only

- **WHEN** a contributor inspects the `infrastructure` target in `docs/synced-paths.yaml`
- **THEN** its `profiles` list includes `foundation` and MUST NOT include `python-product` (typically `foundation` +
  `gitops` + an Infra-only profile for `.pre-commit-config.infrastructure.yaml`)
- **AND** python-product repos list `foundation`, `python-product`, and `gitops` (or equivalent union that preserves
  today’s product hook set including helm-lint)
- **AND** no `.devcontainer/**` path appears on any profile used by the `infrastructure` target

#### Scenario: Infra effective allow includes Renovate and foundation pins

- **WHEN** sync or a test resolves the effective allow for the `infrastructure` target
- **THEN** `renovate.json`, `.github/workflows/renovate.yml`, and `versions.foundation.env` are included
- **AND** `versions.env` and `.python-version` are not included

## ADDED Requirements

### Requirement: Pin files split by profile

`docs/synced-paths.yaml` MUST allowlist `versions.foundation.env` under `foundation` and MUST allowlist `versions.env`
(and `.python-version`) under `python-product` only. Docs MUST state foundation-eligible pins live in
`versions.foundation.env` and python-product pins in `versions.env`, with no intentional duplicate keys across files.

#### Scenario: Profile split for pin files

- **WHEN** a contributor inspects pin-file allowlist membership
- **THEN** `versions.foundation.env` is on `foundation`
- **AND** `versions.env` and `.python-version` are on `python-product` only
- **AND** docs name the two-file pin split
