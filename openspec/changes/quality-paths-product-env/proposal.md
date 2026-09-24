## Why

Products duplicate colon-separated `MYPYPATH` (and comma-separated pylint roots) across `.devcontainer/product.env`,
caller workflow `with:` inputs, and docs. Drift breaks local hooks vs CI. Compose only loads `product.env` at container
create, so edits need a rebuild unless quality tooling re-reads the file on each invoke (#215; comment lock-in).

## What Changes

- Treat product-owned `.devcontainer/product.env` as the SoT for `MYPYPATH=` and `PYLINT_SOURCE_ROOTS=` (lock-in **A**).
- `reusable-code-quality.yml`: when `mypy_path` / `pylint_source_roots` inputs are empty, load those keys from
  `.devcontainer/product.env` (optional input for alternate path MAY exist; default that file). Explicit inputs still
  override.
- `scripts/run-quality-cli.sh` (or a tiny sourced helper it calls): before exec, soft-load the same file into the
  environment when vars are unset — so commit-stage mypy/pylint see updates without Dev Container rebuild.
- Document the contract in `docs/ci.md`, `docs/quality.md`, and/or `docs/devcontainer.md`; link Harvester adopter
  follow-up [#299](https://github.com/fairagro/m4.2_middleware_harvester/issues/299).

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `reusable-ci-workflows`: reusable code-quality MUST derive path overlays from product env file when inputs empty.
- `shared-quality-tooling`: quality CLI runner MUST re-read product env path overlays on each invoke when unset.

## Impact

- `.github/workflows/reusable-code-quality.yml`, `scripts/run-quality-cli.sh` (+ optional helper), docs, possibly sync
  allowlist if a new helper script is added.
- Products migrate by dropping duplicate `mypy_path:` literals (Harvester #299) — not implemented in this Devinfra PR.
