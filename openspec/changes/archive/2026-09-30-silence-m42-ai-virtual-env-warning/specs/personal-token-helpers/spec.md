## ADDED Requirements

### Requirement: m42-ai wrapper unsets VIRTUAL_ENV then runs product project

The repository MUST provide an executable `scripts/bin/m42-ai` that unsets `VIRTUAL_ENV` (when set) and then runs
`uv run --project <repo-root>/scripts/ai m42-ai` with the caller's arguments. `<repo-root>` MUST be derived from the
wrapper's location (`scripts/bin` → repository root). The wrapper MUST be on the product sync allowlist with other
`scripts/bin` helpers. It MUST NOT pass `--active` to uv. It MUST NOT clear Dev Container `remoteEnv.VIRTUAL_ENV`
configuration.

#### Scenario: Wrapper silences mismatch warning

- **WHEN** `VIRTUAL_ENV` points at the repo-root `.venv` and `scripts/bin` is on `PATH`
- **AND** a contributor runs `m42-ai --help` (or another CLI subcommand)
- **THEN** uv does not print the `VIRTUAL_ENV` does not match `scripts/ai/.venv` warning
- **AND** the product `scripts/ai` environment is used

#### Scenario: Wrapper is synced to products

- **WHEN** a product sync allowlist is applied
- **THEN** `scripts/bin/m42-ai` is included alongside other `scripts/bin` helpers
