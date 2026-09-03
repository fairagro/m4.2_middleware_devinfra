## Purpose

Defines how this shared Devinfra repo presents itself as the canonical source of truth: root entry documentation, a growing docs index, empty shared-path skeleton, and where Dev Container and tool-version guidance live.

## ADDED Requirements

### Requirement: Root README states purpose and ownership
The repository MUST include a root `README.md` that states the repo purpose, names the three consumer product repositories, states that canonical shared files live here, and states that consumers MUST NOT hand-edit synced shared paths (shared changes land here first).

#### Scenario: Contributor opens the repository
- **WHEN** a contributor opens the repository root
- **THEN** `README.md` identifies this repo as the shared Devinfra source of truth for `m4.2_advanced_middleware_api`, `m4.2_sql_to_arc`, and `m4.2_middleware_harvester`
- **AND** it states the ownership rule that synced paths in consumers are not hand-edited

### Requirement: Root README indexes feature docs
The root `README.md` MUST remain a thin purpose document and MUST link to feature documentation under `docs/` rather than embedding full operator guides. As new feature docs are added over time, they MUST be linked from this index.

#### Scenario: Dev Container doc is the only feature doc
- **WHEN** the bootstrap layout is complete
- **THEN** `README.md` links to `docs/devcontainer.md`
- **AND** it does not duplicate the full Dev Container operator guide

### Requirement: Tool versioning is visible from the root README
The root `README.md` MUST mention the global tool versioning system: `versions.env` as the pin source of truth and `.python-version` as the Python pin kept aligned with `PYTHON_VERSION`. Detailed change/rebuild steps MAY live in `docs/devcontainer.md`.

#### Scenario: Contributor looks for where versions are pinned
- **WHEN** a contributor reads the root `README.md`
- **THEN** they learn that toolchain pins live in `versions.env` and that `.python-version` tracks `PYTHON_VERSION`

### Requirement: Shared path skeleton exists
The repository MUST contain the following directories, tracked in git via `.gitkeep` when otherwise empty: `docs/`, `.agents/skills/`, `.cursor/`, and `.github/`. Existing populated paths (`.devcontainer/`, `scripts/`) remain and do not require `.gitkeep`.

#### Scenario: Empty shared directories are present
- **WHEN** the bootstrap layout is complete
- **THEN** `.agents/skills/`, `.cursor/`, and `.github/` each contain a `.gitkeep`
- **AND** `docs/` exists and holds feature documentation (and may also use `.gitkeep` only if needed alongside docs)

### Requirement: Dev Container documentation lives under docs
Dev Container operator documentation MUST live at `docs/devcontainer.md`. The path `.devcontainer/README.md` MUST NOT exist.

#### Scenario: Operator needs Dev Container guidance
- **WHEN** an operator needs to open, rebuild, or understand the Dev Container
- **THEN** they use `docs/devcontainer.md` (linked from the root README)
- **AND** `.devcontainer/README.md` is absent

### Requirement: No product code in bootstrap
The bootstrap MUST NOT add product application code. Layout and documentation only.

#### Scenario: Bootstrap change is applied
- **WHEN** this change is implemented
- **THEN** the repository still contains no product middleware/application packages
- **AND** only documentation, skeleton placeholders, and existing shared tooling files are present for this change
