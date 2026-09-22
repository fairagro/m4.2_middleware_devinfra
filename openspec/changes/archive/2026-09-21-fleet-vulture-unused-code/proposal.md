## Why

Dead/unused definitions are a `/code-review` goal, but the fleet has no static unused-code gate—only Ruff unused
**imports**. Agents must not invent mechanical dead-code nits once a toolchain owns them
([#172](https://github.com/fairagro/m4.2_middleware_devinfra/issues/172); contract from
[#140](https://github.com/fairagro/m4.2_middleware_devinfra/issues/140)).

## What Changes

- Add **vulture** to the shared quality toolchain targeting `middleware/`
- Wire **commit-stage pre-commit** and **reusable code-quality CI** with the same fail bar
- Fail policy (**explore lock-in D2**): `--min-confidence 100`, **no** fleet whitelist file
- Document parity (hooks + CI; **no IDE** gate — Bandit-style named exception) and FP handling (dynamic attrs /
  fixtures: fix code or `# noqa`, not a synced whitelist)
- Update `/code-review` anti-duplication: vulture is **toolchain-owned** once this lands
- **Not** in this change: import-linter (#173), IDE extension for vulture

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-python-quality-config`: document vulture as a shared gate (CLI policy; no whitelist fragment under D2)
- `shared-quality-tooling`: commit-stage + CI must run vulture; pre-commit skeleton lists it; Bandit-like IDE exception
- `synced-consumer-paths`: only if a new sync path is required (none expected under D2 — pre-commit already allowlisted)
- `code-review`: anti-duplication treats vulture as landed / owned (import-linter still “once landed”)

## Impact

- `.pre-commit-config.yaml`, `reusable-code-quality.yml`, root `pyproject.toml` / uv deps (vulture pin)
- `docs/quality.md`, `openspec/principles.global.md` (Code Quality examples)
- `.agents/skills/code-review/SKILL.md`, `docs/code-review.md`
- Product adopt via sync of pre-commit + dep pin; first runs may fail on real unused code at confidence 100
- Issue [#172](https://github.com/fairagro/m4.2_middleware_devinfra/issues/172); sibling
  [#173](https://github.com/fairagro/m4.2_middleware_devinfra/issues/173) unchanged
