# Quality tools environment parity

## Why

Quality tools already run in the IDE, in pre-commit / pre-push hooks, and in GitHub Actions, but the contract that
**those three surfaces must produce the same outcomes** is only implied. Without an explicit requirement, configs and
CLI flags can drift (extra rule overrides on the command line, IDE settings pointing at a different config, CI using
different switches), and contributors get “green locally, red in CI” or the reverse.

## What Changes

- Add an explicit **environment parity** requirement: every shared quality tool that gates product or Devinfra work MUST
  be runnable in (1) the IDE, (2) pre-commit / pre-push hooks, and (3) GitHub pipelines, with **matching results** for
  the same tree and toolchain pin.
- Require **shared config files** as the single source of truth for tool policy; CLI (and IDE settings) MAY pass the
  config-file path and target paths, and MUST NOT restate rule/severity/version policy as command-line flags unless
  there is no config-file equivalent (document any exception).
- Align documentation (`docs/quality.md`, principles Code Quality section) and audit existing hook / CI / IDE
  invocations for parity gaps introduced by extra CLI args or divergent config pointers.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-quality-tooling`: Add cross-environment parity + minimal CLI config surface for all shared quality tools
  (hooks, scripts, reusable CI, IDE baseline).
- `shared-python-quality-config`: Tighten that fragment files are the only policy surface; invocations only need
  config-file path (+ target paths / product path overlays).
- `global-principles`: Record the three-environment parity rule under Code Quality so finders/fixers and humans share
  the same bar.

## Impact

- Specs / principles / `docs/quality.md`; possibly small edits to `.pre-commit-config.yaml`,
  `.github/workflows/reusable-code-quality.yml`, `.vscode/settings.json`, and `scripts/quality-check.sh` where an audit
  finds extra CLI policy flags or mismatched config paths.
- No new runtime services; product sync (#13) inherits the documented contract after merge.
