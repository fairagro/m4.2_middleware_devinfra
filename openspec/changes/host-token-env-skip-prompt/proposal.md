## Why

Host-side `GH_TOKEN` / `GITGUARDIAN_API_KEY` are often already set, but the Dev Container does not pass them through
`remoteEnv`, and `scripts/dev-tokens.sh` treats the store as sole source (clearing process env when a key is missing).
Developers are re-prompted or blocked despite having host credentials. Issue
[#152](https://github.com/fairagro/m4.2_middleware_devinfra/issues/152).

## What Changes

- Pass host `GH_TOKEN` / `GITGUARDIAN_API_KEY` into the container via `remoteEnv` `${localEnv:…}`
- Change token load precedence: **non-empty store wins**; otherwise keep non-empty process/host env; prompt only if
  still empty. Override host by writing the store via `scripts/set-dev-tokens.sh` (`DEV_TOKENS_FORCE=1`)
- **Remove empty skip markers** — empty TTY answers are not persisted as “skip forever”
- Update docs (README Personal tokens / `docs/devcontainer.md`) and OpenSpec `personal-token-helpers`
- Linux Dev Container / `/commandhistory` scope unchanged; no secrets in the git worktree or logs

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `personal-token-helpers`: Replace sole-source + empty-skip contract with store-wins-when-non-empty, host/process
  fill-in, no empty skip marker, `remoteEnv` host pass-through, and updated documentation requirements

## Impact

- Devinfra: `scripts/dev-tokens.sh`, `.devcontainer/devcontainer.json`, docs/README, tests under `scripts/ai/tests/` (or
  existing token tests), OpenSpec `personal-token-helpers`
- Products after sync: host tokens flow into DC; prompts only when neither store nor host provides a value
