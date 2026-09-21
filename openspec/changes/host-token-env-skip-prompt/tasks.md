## 1. Token helper behavior

- [x] 1.1 Change `scripts/dev-tokens.sh` store apply so non-empty store wins, missing store key (or absent store file)
      keeps non-empty process/host env, and empty skip markers are not written; verify with focused tests
- [x] 1.2 Change `_dev_tokens_ask` to skip when the var is already non-empty (non-forced) and to not persist empty
      answers as skip markers; verify empty prompt + host-env keep tests
- [x] 1.3 Keep `set-dev-tokens.sh` / `DEV_TOKENS_FORCE=1` as the path that forces prompt and writes non-empty store
      values; verify force override beats host env in tests

## 2. Dev Container + docs

- [x] 2.1 Add `remoteEnv` `${localEnv:GH_TOKEN}` and `${localEnv:GITGUARDIAN_API_KEY}` in
      `.devcontainer/devcontainer.json`; verify the keys are present
- [x] 2.2 Update README Personal tokens and `docs/devcontainer.md` for store-vs-host precedence, no empty skip marker,
      and `set-dev-tokens.sh` override; verify `npm run lint:md` is clean

## 3. Validate

- [x] 3.1 Run `openspec validate host-token-env-skip-prompt --strict` and focused token tests until green
