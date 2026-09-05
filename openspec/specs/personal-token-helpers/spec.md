# personal-token-helpers Specification

## Purpose

Defines shared personal-token persistence and `gh`/`git` PATH wrappers so agent and developer tooling can authenticate
in the Linux Dev Container, following path conventions.

## Requirements

### Requirement: Token store paths follow conventions

`scripts/dev-tokens.sh` MUST resolve the token file to `/commandhistory/tokens.env` when `/commandhistory` exists. The
helpers MUST NOT require `PRODUCT_SLUG` and MUST NOT hard-code a single product name such as `middleware-api`. If
`/commandhistory` is absent, the helpers MUST fail with a clear error that personal tokens are supported in the Linux
Dev Container only (no host `~/.config/…` fallback).

#### Scenario: Dev Container uses volume path

- **WHEN** `dev-tokens.sh` runs inside a Dev Container with `/commandhistory` present
- **THEN** it reads and writes `/commandhistory/tokens.env`
- **AND** it does not write tokens into the git worktree

#### Scenario: Missing commandhistory fails clearly

- **WHEN** `dev-tokens.sh` runs without `/commandhistory`
- **THEN** it exits with a non-zero status and an error that the Linux Dev Container is required
- **AND** it does not invent a host path under `~/.config/`

### Requirement: Token file is never executed as shell

`scripts/dev-tokens.sh` MUST NOT `source` the token store file. It MUST load only known keys (`GH_TOKEN`,
`GITGUARDIAN_API_KEY`) by parsing lines. New writes MUST use a non-shell encoding (e.g. `b64:` + GNU `base64 -w0`) on a
**single line** (no wrapped base64). Executing `dev-tokens.sh` directly (instead of sourcing) MUST fail with a clear
error. If the current environment already holds a known key whose value is store-encoded (`b64:` prefix), the helper
MUST decode it in place (or unset it if corrupt) before treating the variable as set.

#### Scenario: Corrupt tokens.env cannot run arbitrary commands via source

- **WHEN** `tokens.env` contains shell metacharacters intended as command substitution
- **THEN** loading does not execute those commands as part of sourcing the file
- **AND** known-key values still load when stored in the supported encoding

#### Scenario: Direct execution of dev-tokens.sh fails clearly

- **WHEN** a user runs `bash scripts/dev-tokens.sh` (or executes the file) instead of sourcing it
- **THEN** the script exits non-zero with a message to source it

#### Scenario: Accidental source of tokens.env is sanitized

- **WHEN** the environment already contains `GH_TOKEN` (or `GITGUARDIAN_API_KEY`) whose value starts with `b64:`
  (typical after mistakenly sourcing the token store file)
- **AND** `scripts/dev-tokens.sh` is sourced (directly or via `scripts/bin/gh`)
- **THEN** the helper decodes that value in place (or unsets it if corrupt)
- **AND** it does not leave the encoded `b64:` form as the live credential

### Requirement: Empty prompt skips until re-prompt

When prompting on a TTY for `GH_TOKEN` or `GITGUARDIAN_API_KEY`, an empty answer MUST persist a skip marker so later
non-forced loads do not re-prompt. `scripts/set-dev-tokens.sh` MUST force a new prompt (including after a skip) and
persist non-empty values. Without a TTY, helpers MUST NOT hang; wrappers that need a token MUST fail with a message
pointing at `set-dev-tokens.sh`.

#### Scenario: User skips GH_TOKEN once

- **WHEN** the user submits an empty answer at the `GH_TOKEN` prompt
- **THEN** the skip is remembered in the token file
- **AND** a later `source scripts/dev-tokens.sh` without force does not prompt again for that variable

#### Scenario: User re-prompts after skip

- **WHEN** the user runs `scripts/set-dev-tokens.sh` (or sources it) after a skip
- **THEN** they are prompted again for the skipped variable
- **AND** a non-empty value is exported and stored

### Requirement: gh wrapper loads token then execs real gh

`scripts/bin/gh` MUST source the shared token helper, require a non-empty `GH_TOKEN` (or `GITHUB_TOKEN`), and exec the
real system `gh` binary (not itself). Real-binary discovery MUST prefer `command -v -p gh` (excluding the wrapper) and
MAY fall back to `/usr/bin/gh`. It MUST NOT read tokens from the git worktree.

#### Scenario: gh succeeds with stored token

- **WHEN** `GH_TOKEN` is available via the token store or environment
- **AND** the user invokes `gh` via `scripts/bin` on `PATH`
- **THEN** the wrapper execs the real `gh` with the caller's arguments

#### Scenario: gh fails without token or TTY setup

- **WHEN** no token is available and prompting cannot complete
- **THEN** the wrapper exits non-zero with guidance to run `./scripts/set-dev-tokens.sh`

### Requirement: git wrapper preserves hooks under Cursor SCM

`scripts/bin/git` MUST strip Cursor-injected `core.hooksPath=/dev/null` from `GIT_CONFIG_*` environment entries, source
the token helper, and exec the real `git` binary (not itself).

#### Scenario: Cursor SCM does not disable hooks via null hooksPath

- **WHEN** Cursor injects `core.hooksPath=/dev/null` via `GIT_CONFIG_*`
- **AND** git is invoked through `scripts/bin/git`
- **THEN** that null hooksPath pin is removed before exec
- **AND** the real git binary runs the remaining arguments

### Requirement: Dev Container PATH and stored-token load

This repository's Dev Container configuration MUST put the repo's `scripts/bin` ahead of the default `PATH` so `gh` and
`git` resolve to the wrappers (which source the token helper). postCreate MAY source the token helper once into the
postCreate environment (non-prompting). The helpers MUST NOT patch `~/.bashrc` or other shell profiles. Documentation
MUST describe the empty-skip and re-prompt flow, wrapper-based load, and `/commandhistory/tokens.env`.

#### Scenario: Contributor looks up token setup

- **WHEN** a contributor reads the root README (or linked Dev Container doc) for personal tokens
- **THEN** they find empty-skip and `set-dev-tokens.sh` re-prompt behavior
- **AND** they are directed to `/commandhistory/tokens.env` in the Dev Container
- **AND** they learn that `gh` / `git` on `PATH` load tokens via the wrappers (no `.bashrc` patch)

#### Scenario: Stored tokens available via wrappers

- **WHEN** non-empty tokens are already stored and the user invokes `gh` or `git` through `scripts/bin` on `PATH`
- **THEN** the wrapper sources the helper and uses the stored token when present
