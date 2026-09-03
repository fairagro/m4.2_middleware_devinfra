# Personal Token Helpers — Delta

## Purpose

Defines shared personal-token persistence and `gh`/`git` PATH wrappers so agent and developer tooling can authenticate
without hard-coding product config directories, following path conventions.

## ADDED Requirements

### Requirement: Token store paths follow conventions

`scripts/dev-tokens.sh` MUST resolve the token file to `/commandhistory/tokens.env` when `/commandhistory` exists, and
otherwise to `~/.config/<product-slug>/tokens.env` where `<product-slug>` is the value of `PRODUCT_SLUG`. The helpers
MUST NOT infer the slug from directory or remote names and MUST NOT hard-code a single product name such as
`middleware-api`. If `/commandhistory` is absent and `PRODUCT_SLUG` is unset or empty, the helpers MUST fail with an
error that tells the user to set `PRODUCT_SLUG`.

#### Scenario: Dev Container uses volume path

- **WHEN** `dev-tokens.sh` runs inside a Dev Container with `/commandhistory` present
- **THEN** it reads and writes `/commandhistory/tokens.env`
- **AND** it does not write tokens into the git worktree

#### Scenario: Host clone requires PRODUCT_SLUG

- **WHEN** `dev-tokens.sh` runs on a host clone without `/commandhistory`
- **AND** `PRODUCT_SLUG` is set to the product's documented slug
- **THEN** it uses `~/.config/<PRODUCT_SLUG>/tokens.env`
- **AND** two products on one machine keep separate host token files when they use different slugs

#### Scenario: Host clone missing PRODUCT_SLUG

- **WHEN** `dev-tokens.sh` runs without `/commandhistory` and without `PRODUCT_SLUG`
- **THEN** it exits with a non-zero status and an error naming `PRODUCT_SLUG`
- **AND** it does not invent a slug

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
real system `gh` binary (not itself). It MUST NOT read tokens from the git worktree.

#### Scenario: gh succeeds with stored token

- **WHEN** `GH_TOKEN` is available via the token store or environment
- **AND** the user invokes `gh` via `scripts/bin` on `PATH`
- **THEN** the wrapper execs the real `gh` with the caller's arguments

#### Scenario: gh fails without token or TTY setup

- **WHEN** no token is available and prompting cannot complete
- **THEN** the wrapper exits non-zero with guidance to run `./scripts/set-dev-tokens.sh`

### Requirement: git wrapper preserves hooks under Cursor SCM

`scripts/bin/git` MUST invoke `scripts/cursor-git.sh`, which MUST strip Cursor-injected `core.hooksPath=/dev/null` (and
equivalent null hooks pins) from the environment and argv, source the token helper, and exec the real `git` binary.

#### Scenario: Cursor SCM does not disable hooks via null hooksPath

- **WHEN** Cursor injects `core.hooksPath` pointing at a null device
- **AND** git is invoked through `scripts/bin/git`
- **THEN** that null hooksPath pin is removed before exec
- **AND** the real git binary runs the remaining arguments

### Requirement: Dev Container PATH, PRODUCT_SLUG, and stored-token load

This repository's Dev Container configuration MUST put the repo's `scripts/bin` ahead of the default `PATH` so `gh` and
`git` resolve to the wrappers, and MUST set `PRODUCT_SLUG` for this repo (`middleware-devinfra`). postCreate and/or the
interactive shell profile MUST source the token helper in a non-prompting way so already stored non-empty tokens are
exported into the environment. Documentation MUST describe the empty-skip and re-prompt flow, the Kombi (shell load +
wrappers), and point at path conventions for token locations.

#### Scenario: Contributor looks up token setup

- **WHEN** a contributor reads the root README (or linked Dev Container doc) for personal tokens
- **THEN** they find empty-skip and `set-dev-tokens.sh` re-prompt behavior
- **AND** they are directed to the conventions token paths and `PRODUCT_SLUG`

#### Scenario: Stored tokens available in a Dev Container shell

- **WHEN** non-empty tokens are already stored and postCreate or the shell profile has sourced the helper without a TTY
  prompt
- **THEN** `GH_TOKEN` and/or `GITGUARDIAN_API_KEY` are present in the environment for that session when stored
