## ADDED Requirements

### Requirement: Optional secondary PyInstaller binary via build-args

The shared product-app base (`docker/Dockerfile.product-app.base`) MUST support building **at most one** optional
secondary PyInstaller binary in addition to the primary `--onedir` binary. When secondary identity build-args are
**unset or empty**, behavior MUST match the existing single-primary export (no secondary artifact under `/dist`).

When a secondary binary name is set, the base MUST:

- Resolve the secondary entry from a secondary import path (preferred) or an explicit secondary entry path after wheel
  install, using the same lockfile-deterministic environment as the primary build
- Build the secondary with PyInstaller `--onefile` by default when a secondary is requested, unless a documented
  build-arg opts into `--onedir` for the secondary
- Place both primary and secondary artifacts under the export stage’s stable `/dist` path so a product Bake last stage
  can consume them from the **same** export context (no second base Dockerfile required)

The base MUST NOT require products to fork or hand-edit `Dockerfile.product-app.base` to obtain a secondary binary. The
base MUST NOT encode product-specific HEALTHCHECK / CMD wiring for the secondary — that remains product-local last-stage
finishing.

#### Scenario: No secondary args — single primary only

- **WHEN** a Bake/base build omits secondary binary identity args (or sets them empty)
- **THEN** `export-binaries` contains the primary onedir tree under `/dist` as today
- **AND** no secondary binary artifact is produced

#### Scenario: Secondary onefile lands beside primary

- **WHEN** a product passes a secondary binary name plus a secondary import (or entry) on the shared base target
- **THEN** `/dist` includes both the primary onedir artifact and the secondary binary
- **AND** the secondary is built as `--onefile` unless the product opts the secondary into `--onedir` via the documented
  arg
- **AND** the product last stage can `COPY` both from the same Bake export context

#### Scenario: Secondary without identity fails closed

- **WHEN** a secondary is requested without a resolvable secondary import or entry after wheel install
- **THEN** the binary-builder stage fails with a clear error
- **AND** it does not silently skip the secondary

### Requirement: Optional secondary binary contract is documented

Documentation in this repository (at least `docs/ci.md`, and example stubs under `docker/examples/` when present) MUST
describe the secondary build-arg names, the empty/no-op default, onefile-vs-onedir behavior for the secondary, and how a
product last stage copies secondary artifacts from the shared export context. Documentation MUST state that deleting
product-local secondary Dockerfiles (e.g. harvester healthcheck) is a product follow-up after sync, not a Devinfra base
requirement.

#### Scenario: Contributor learns secondary ARG surface

- **WHEN** a contributor reads the product-app Bake / base Dockerfile docs after this change
- **THEN** they learn which build-args enable an optional secondary binary
- **AND** they learn that omitting those args preserves single-primary builds
- **AND** example stubs illustrate copying a secondary from the export context when applicable
