# personal-token-helpers Specification

## Purpose

Defines shared personal-token persistence and `gh`/`git` PATH wrappers so agent and developer tooling can authenticate
without hard-coding product config directories, following path conventions.

## Requirements

### Requirement: Token store paths follow conventions

`scripts/dev-tokens.sh` MUST resolve the token file to `/commandhistory/tokens.env` when `/commandhistory` exists, and
otherwise to `~/.config/<git-repo-name>/tokens.env` where `<git-repo-name>` is the repository name from the clone's
`origin` remote URL (strip `.git`; last path segment), falling back to the basename of `git rev-parse --show-toplevel`
when `origin` is unavailable. Both git lookups MUST use `git -C <repo_root>` where `<repo_root>` is the repository that
owns `scripts/dev-tokens.sh` (not the caller's CWD). The helpers MUST use the real `git` binary (not `scripts/bin/git`).
The helpers MUST NOT require `PRODUCT_SLUG` and MUST NOT hard-code a single product name such as `middleware-api`. If
`/commandhistory` is absent and the repository name cannot be determined, the helpers MUST fail with a clear error.

#### Scenario: Dev Container uses volume path

- **WHEN** `dev-tokens.sh` runs inside a Dev Container with `/commandhistory` present
- **THEN** it reads and writes `/commandhistory/tokens.env`
- **AND** it does not write tokens into the git worktree

#### Scenario: Host clone uses git repository name

- **WHEN** `dev-tokens.sh` runs on a host clone without `/commandhistory`
- **AND** the clone has a resolvable `origin` remote (or git toplevel)
- **THEN** it uses `~/.config/<git-repo-name>/tokens.env`
- **AND** two products on one machine keep separate host token files when their repository names differ

#### Scenario: Host clone cannot resolve repository name

- **WHEN** `dev-tokens.sh` runs without `/commandhistory` and cannot determine a git repository name
- **THEN** it exits with a non-zero status and an error explaining the host path needs a git clone/remote
- **AND** it does not invent a name or require `PRODUCT_SLUG`

### Requirement: Token file is never executed as shell

`scripts/dev-tokens.sh` MUST NOT `source` the token store file. It MUST load only known keys (`GH_TOKEN`,
`GITGUARDIAN_API_KEY`) by parsing lines. New writes MUST use a non-shell encoding (e.g. `b64:` + base64) on a **single
line** (no wrapped base64). Executing `dev-tokens.sh` directly (instead of sourcing) MUST fail with a clear error. If
the current environment already holds a known key whose value is store-encoded (`b64:` prefix), the helper MUST decode
it in place (or unset it if corrupt) before treating the variable as set.

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
fall back to common absolute paths. It MUST NOT read tokens from the git worktree.

#### Scenario: gh succeeds with stored token

- **WHEN** `GH_TOKEN` is available via the token store or environment
- **AND** the user invokes `gh` via `scripts/bin` on `PATH`
- **THEN** the wrapper execs the real `gh` with the caller's arguments

#### Scenario: gh fails without token or TTY setup

- **WHEN** no token is available and prompting cannot complete
- **THEN** the wrapper exits non-zero with guidance to run `./scripts/set-dev-tokens.sh`

### Requirement: git wrapper preserves hooks under Cursor SCM

`scripts/bin/git` MUST strip Cursor-injected `core.hooksPath=/dev/null` (and equivalent null hooks pins) from the
environment and argv, source the token helper, and exec the real `git` binary (not itself).

#### Scenario: Cursor SCM does not disable hooks via null hooksPath

- **WHEN** Cursor injects `core.hooksPath` pointing at a null device
- **AND** git is invoked through `scripts/bin/git`
- **THEN** that null hooksPath pin is removed before exec
- **AND** the real git binary runs the remaining arguments

### Requirement: Dev Container PATH and stored-token load

This repository's Dev Container configuration MUST put the repo's `scripts/bin` ahead of the default `PATH` so `gh` and
`git` resolve to the wrappers. postCreate and/or the interactive shell profile MUST source the token helper in a
non-prompting way so already stored non-empty tokens are exported into the environment. Documentation MUST describe the
empty-skip and re-prompt flow, the Kombi (shell load + wrappers), and point at path conventions for token locations
(including host derivation from the git repository name).

#### Scenario: Contributor looks up token setup

- **WHEN** a contributor reads the root README (or linked Dev Container doc) for personal tokens
- **THEN** they find empty-skip and `set-dev-tokens.sh` re-prompt behavior
- **AND** they are directed to the conventions token paths (host: git repository name)

#### Scenario: Stored tokens available in a Dev Container shell

- **WHEN** non-empty tokens are already stored and postCreate or the shell profile has sourced the helper without a TTY
  prompt
- **THEN** `GH_TOKEN` and/or `GITGUARDIAN_API_KEY` are present in the environment for that session when stored
