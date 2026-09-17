## Context

See `proposal.md` / [#152](https://github.com/fairagro/m4.2_middleware_devinfra/issues/152). Explore lock-ins: host
pass-through via `remoteEnv`; store non-empty wins; otherwise keep process/host env; **no empty skip markers**; override
host with `set-dev-tokens.sh`.

Today `dev-tokens.sh` unsets known keys when the store lacks them (or when the store file is absent), which would wipe
`${localEnv:…}` injects. `_dev_tokens_ask` also skips prompting whenever a store **line** exists (including empty skip
markers) and persists empty answers as skip markers.

## Goals / Non-Goals

**Goals:**

- Host tokens usable in the Linux Dev Container without re-typing
- Prompt only when store and process env are both empty for that var
- Remove empty-skip persistence; document new precedence
- Spec + tests updated for the contract change

**Non-Goals:**

- Auto-writing host tokens into the store
- Supporting personal tokens without `/commandhistory`
- Changing `GITHUB_TOKEN` bot/automation semantics

## Decisions

### D1: remoteEnv pass-through

In `.devcontainer/devcontainer.json` `remoteEnv`:

```json
"GH_TOKEN": "${localEnv:GH_TOKEN}",
"GITGUARDIAN_API_KEY": "${localEnv:GITGUARDIAN_API_KEY}"
```

Unset host vars become empty strings in the remote env (harmless).

### D2: Apply-store logic

For each known key:

- Store non-empty decoded → `export`
- Else → **do not unset** an existing non-empty process value; only unset if store had an empty skip line we are
  migrating away from (prefer deleting empty skip lines on write paths; do not create new ones)

When the store file is absent: **do not** blanket-unset both vars (preserve host inject).

### D3: Prompt gating

Skip `_dev_tokens_ask` when `DEV_TOKENS_FORCE` is unset and the variable is already non-empty after apply. Do not key
skip solely off “store line exists” for empty markers. Empty TTY answer: do not call write with empty (or do not persist
skip); leave unset.

### D4: set-dev-tokens remains override

`DEV_TOKENS_FORCE=1` / `set-dev-tokens.sh` forces prompt and persists non-empty store values so store wins thereafter.

### D5: Tests

Update/extend `scripts/ai/tests/test_dev_tokens_store.py` (or sibling) for: missing store key keeps process env; store
wins; empty answer does not create skip marker; force override.

## Risks / Trade-offs

- **[BREAKING]** Callers that relied on empty skip markers to suppress prompts forever must use host env, store a real
  token, or re-prompt — Mitigation: document; `set-dev-tokens.sh` for overrides
- **[Risk]** Empty-string `remoteEnv` vs unset — treat empty as absent for “non-empty” checks

## Migration Plan

1. Land script + `devcontainer.json` + docs + tests; draft PR `Fixes #152`.
2. After sync/rebuild, host tokens flow; rebuild container so `remoteEnv` applies.

## Open Questions

None — explore lock-ins applied (no empty skip marker).
