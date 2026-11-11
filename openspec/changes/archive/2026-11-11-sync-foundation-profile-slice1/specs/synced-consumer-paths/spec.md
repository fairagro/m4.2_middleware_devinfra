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

- **WHEN** a contributor checks whether Renovate config or workflow may be hand-edited in a product repo after sync
- **THEN** `renovate.json` and `.github/workflows/renovate.yml` appear under a profile used by python-product targets
  (not required on foundation-only Infra)
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

## ADDED Requirements

### Requirement: Foundation profile covers Slice-1 agent surfaces

The `foundation` profile `allow` list MUST include the fleet agent skill trees used by m4.2 eng repos (at least
`review-fixer`, `create-issue`, `code-review`, `issue-fixer`, `arctrl`, `gh`, `docker`, `hadolint`, and `uv`), the
matching Cursor commands and GitHub Copilot prompts for those skills, `.cursor/BUGBOT.md`,
`.github/copilot-instructions.md`, the skill-facing docs under `docs/` for those skills, `scripts/ai/**`,
`scripts/bin/m42-ai`, and the personal-token helper scripts/binaries those skills document (`scripts/dev-tokens.sh`,
`scripts/set-dev-tokens.sh`, and allowlisted `scripts/bin` wrappers required for that flow). The `foundation` profile
MUST NOT include Renovate config/workflow, `versions.env` / `.python-version`, `.devcontainer/**`,
`.pre-commit-config.yaml`, or python-product-only quality/CI surfaces that belong in `python-product`. Documentation
(`docs/sync.md`) MUST state that Infra / foundation-only consumers receive this profile and that Renovate on Infra is a
later slice.

#### Scenario: Foundation includes skills and m42-ai plumbing

- **WHEN** a contributor inspects the `foundation` profile allow list
- **THEN** agent skills (including `uv`), matching commands/prompts, skill docs, `scripts/ai/**`, and `m42-ai` / token
  helpers are listed
- **AND** Renovate / `versions.env` / Dev Container / pre-commit blob are not listed under `foundation`

#### Scenario: Infra target is foundation-only

- **WHEN** a contributor inspects the `infrastructure` target in `docs/synced-paths.yaml`
- **THEN** its `profiles` list is exactly `foundation` (or equivalent foundation-only set)
- **AND** python-product repos list both `foundation` and `python-product`
