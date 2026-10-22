## ADDED Requirements

### Requirement: Commit-msg path check gates feat/fix against staged paths

The shared commit-stage quality tooling MUST run a path-aware check on the **commit-msg** hook (in addition to
commitlint type-enum). The check MUST read the commit message and the staged file list
(`git diff --cached --name-only`). It MUST reject commits whose Conventional Commits type is `feat` or `fix` when the
staged index is **only**:

- OpenSpec planning under `openspec/changes/**` excluding `openspec/changes/archive/**`, or
- OpenSpec archive and/or main-spec sync (`openspec/changes/archive/**` and/or `openspec/specs/**`) without any
  shipped-behaviour paths outside those trees, or
- test-only paths (paths under a `tests/` segment and/or filenames matching common unit-test patterns such as
  `test_*.py` / `*_test.py`), with no non-test shipped paths.

The check MUST reject type `docs` when the commit is an OpenSpec archive operation (staged paths under
`openspec/changes/archive/**`, optionally with `openspec/specs/**` sync) and the subject indicates archive — operators
MUST use `chore` (optional scope `openspec`) instead. The check MUST allow Renovate-style `deps` commits and MUST soft
pass when there are no staged paths (empty index / hook edge). Failure output MUST name the path-check gate and state
the expected type. Documentation MUST describe the gate and note that `--no-verify` remains an escape hatch. This MUST
NOT replace agent handoff Suggested commit messages from `/issue-fixer` / `/review-fixer`.

#### Scenario: feat rejected for propose-only index

- **WHEN** a contributor commits with type `feat` and the staged index contains only files under
  `openspec/changes/<name>/` (not under `archive/`)
- **THEN** the commit-msg path check fails
- **AND** the failure message identifies the path-check gate

#### Scenario: feat rejected for archive plus main-spec sync only

- **WHEN** a contributor commits with type `feat` and the staged index is only `openspec/changes/archive/**` and/or
  `openspec/specs/**`
- **THEN** the commit-msg path check fails

#### Scenario: fix rejected for test-only index

- **WHEN** a contributor commits with type `fix` and the staged index contains only test paths
- **THEN** the commit-msg path check fails

#### Scenario: chore archive allowed

- **WHEN** a contributor commits with type `chore` and the staged index is an OpenSpec archive (and optional main-spec
  sync)
- **THEN** the path check does not fail solely because of those paths

#### Scenario: feat allowed when shipped paths are staged

- **WHEN** a contributor commits with type `feat` and the staged index includes at least one shipped-behaviour path
  outside OpenSpec planning/archive/spec-only and test-only sets
- **THEN** the path check does not reject the commit for path/type mismatch
