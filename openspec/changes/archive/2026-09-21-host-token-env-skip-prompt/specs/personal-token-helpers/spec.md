## REMOVED Requirements

### Requirement: Token store overrides process environment

**Reason:** Replaced by store-wins-when-non-empty plus host/process fill-in (issue #152); sole-source unset of missing
keys blocked `remoteEnv` host pass-through.

**Migration:** Use the new “Token store and host environment precedence” requirement; rebuild the Dev Container so
`remoteEnv` `${localEnv:…}` applies.

### Requirement: Empty prompt skips until re-prompt

**Reason:** Empty skip markers are removed; override of host env is via `set-dev-tokens.sh` writing a non-empty store
value.

**Migration:** Do not rely on empty prompts to suppress future asks; set host env, store a real token, or run
`source ./scripts/set-dev-tokens.sh`.

## ADDED Requirements

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

## MODIFIED Requirements

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
