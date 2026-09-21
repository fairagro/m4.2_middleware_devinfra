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

### Requirement: Token store and host environment precedence

`scripts/dev-tokens.sh` MUST apply `/commandhistory/tokens.env` (or `DEV_TOKENS_FILE` when set for tests) with this
precedence for each known key (`GH_TOKEN`, `GITGUARDIAN_API_KEY`):

1. If the store has a **non-empty** decoded value for the key, export that value (store wins over process/host env).
2. Else if the process environment already has a **non-empty** value (e.g. host pass-through via Dev Container
   `remoteEnv` `${localEnv:…}`), **keep** it — do not unset solely because the store is missing that key or the store
   file is absent.
3. Else leave the variable unset until prompting (when a TTY is available) or until the caller fails closed.

A differing non-empty process value MUST NOT override a non-empty store value. Empty skip markers MUST NOT be written.
Intentional override of host env is via `scripts/set-dev-tokens.sh` / `DEV_TOKENS_FORCE=1` writing a non-empty store
value.

#### Scenario: Stale process GH_TOKEN loses to store

- **WHEN** the process environment has a non-empty `GH_TOKEN` that differs from the store
- **AND** the store has a non-empty `GH_TOKEN`
- **AND** `scripts/dev-tokens.sh` is sourced (directly or via `scripts/bin/gh`)
- **THEN** `GH_TOKEN` equals the store value
- **AND** the previous process value is not kept

#### Scenario: Missing store key keeps host process env

- **WHEN** the store file exists but has no `GH_TOKEN=` line (or the decoded store value is empty/absent)
- **AND** the process environment has a non-empty `GH_TOKEN` (e.g. from host `remoteEnv`)
- **AND** `scripts/dev-tokens.sh` is sourced
- **THEN** `GH_TOKEN` remains the non-empty process value
- **AND** the helper does not prompt when that value is already set (non-forced)

#### Scenario: Non-empty process env skips prompt

- **WHEN** after store apply `GH_TOKEN` is non-empty
- **AND** `DEV_TOKENS_FORCE` is unset
- **THEN** sourcing `scripts/dev-tokens.sh` does not prompt for `GH_TOKEN`

### Requirement: Prompting without empty skip markers

When prompting on a TTY for `GH_TOKEN` or `GITGUARDIAN_API_KEY`, an empty answer MUST **not** persist a skip marker. The
variable may remain unset for that shell; a later non-forced load MAY use host/process env if present, or prompt again
if still empty. `scripts/set-dev-tokens.sh` MUST force a new prompt and persist **non-empty** values to the store
(override path for host env). Without a TTY, helpers MUST NOT hang; wrappers that need a token MUST fail with a message
pointing at `set-dev-tokens.sh` when neither store nor process env provides a non-empty token.

#### Scenario: Empty TTY answer does not write skip marker

- **WHEN** the user submits an empty answer at the `GH_TOKEN` prompt
- **THEN** no empty skip marker is stored for that variable
- **AND** a later load may use host/process env or prompt again if still empty

#### Scenario: User overrides host via set-dev-tokens

- **WHEN** the process environment has a non-empty host `GH_TOKEN`
- **AND** the user runs `scripts/set-dev-tokens.sh` (or sources it with force) and enters a different non-empty value
- **THEN** that value is exported and stored
- **AND** later loads prefer the store over the host env

### Requirement: gh wrapper loads token then execs real gh

`scripts/bin/gh` MUST source the shared token helper, require a non-empty `GH_TOKEN`, and exec the real system `gh`
binary (not itself). Real-binary discovery MUST prefer `command -v -p gh` (excluding the wrapper) and MAY fall back to
`/usr/bin/gh`. It MUST NOT read tokens from the git worktree. It MUST NOT treat `GITHUB_TOKEN` as a local
developer-token fallback.

#### Scenario: gh succeeds with stored token

- **WHEN** a non-empty `GH_TOKEN` is present in the token store
- **AND** the user invokes `gh` via `scripts/bin` on `PATH`
- **THEN** the wrapper applies the store and execs the real `gh` with the caller's arguments
- **AND** a differing process `GH_TOKEN` does not override the store

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
`git` resolve to the wrappers (which source the token helper). It MUST pass host `GH_TOKEN` and `GITGUARDIAN_API_KEY`
into the remote environment via `remoteEnv` using `${localEnv:GH_TOKEN}` and `${localEnv:GITGUARDIAN_API_KEY}` (empty
when unset on the host). postCreate MAY source the token helper once into the postCreate environment (non-prompting).
The helpers MUST NOT patch `~/.bashrc` or other shell profiles. Documentation MUST describe store-vs-host precedence,
that empty prompts do not persist skip markers, that `set-dev-tokens.sh` is the override path, wrapper-based load, and
`/commandhistory/tokens.env`.

#### Scenario: Contributor looks up token setup

- **WHEN** a contributor reads the root README (or linked Dev Container doc) for personal tokens
- **THEN** they learn store non-empty wins over host env, host/process fills gaps, and `set-dev-tokens.sh` overrides
- **AND** they are directed to `/commandhistory/tokens.env` in the Dev Container
- **AND** they learn that `gh` / `git` on `PATH` load tokens via the wrappers (no `.bashrc` patch)
- **AND** they learn host tokens can arrive via Dev Container `remoteEnv` / `localEnv`

#### Scenario: Stored tokens available via wrappers

- **WHEN** non-empty tokens are already stored and the user invokes `gh` or `git` through `scripts/bin` on `PATH`
- **THEN** the wrapper sources the helper and uses the stored token when present

#### Scenario: Host token available without store line

- **WHEN** the host has `GH_TOKEN` set and the Dev Container `remoteEnv` passes it through
- **AND** the store has no non-empty `GH_TOKEN`
- **AND** the user invokes `gh` via `scripts/bin` on `PATH`
- **THEN** the wrapper uses the host-provided `GH_TOKEN` without requiring a TTY prompt

### Requirement: Token store writes are atomic

`_dev_tokens_write` (or equivalent in `scripts/dev-tokens.sh`) MUST replace `/commandhistory/tokens.env` (or the
resolved store path) with an **atomic** update: write the complete new contents to a temporary file in the same
directory, then replace the destination via `mv` (or equivalent rename). It MUST NOT truncate the destination via shell
redirect (`cat … >store`) after the temp file is complete. Interrupt or ENOSPC during the write MUST NOT leave a
truncated existing store when a prior complete store existed (best-effort: failed rename leaves the previous file
intact).

#### Scenario: Write replaces store via rename

- **WHEN** `_dev_tokens_write` persists a new or updated token value
- **THEN** it finishes the temp file before replacing the store path
- **AND** the replacement uses rename/`mv` rather than redirecting onto the live store file

#### Scenario: Failed mid-write does not wipe prior store via redirect

- **WHEN** writing the temp file fails before rename
- **THEN** the previous tokens store file remains unchanged when it already existed
