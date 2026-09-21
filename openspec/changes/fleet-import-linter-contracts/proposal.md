## Why

Import-graph / layer health is a `/code-review` goal, but mechanical contracts are missing. The skill stays judgment-only
until **import-linter** lands ([#173](https://github.com/fairagro/m4.2_middleware_devinfra/issues/173); [#140](https://github.com/fairagro/m4.2_middleware_devinfra/issues/140)).
Fleet Import policy already requires an acyclic DAG; products need local layer contracts without a single synced layout
for all three repos.

## What Changes

- Add **import-linter** to the shared quality toolchain (hooks + CI; no IDE — Bandit/vulture-style)
- Ship a **synced baseline** encoding what Import policy can express mechanically: acyclic `middleware/` +
  `exclude_type_checking_imports = True` (TYPE_CHECKING edges out of the runtime graph)
- Document **product-owned overlays** for `layers` / `forbidden` / `independence` (sync must not wipe them) — C3
- **pydeps** docs-only / optional local — not a fail gate (D1)
- Update `/code-review` anti-duplication: import-linter mechanical hits are toolchain-owned once landed
- **Not** in this change: inventing shared fleet layer names; pydeps CI; encoding module-level / relative-import /
  `sys.path` rules (those stay principles / other tools)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-python-quality-config`: baseline import-linter config + overlay contract
- `shared-quality-tooling`: pre-commit + reusable CI run import-linter; IDE exception; pydeps non-gate
- `synced-consumer-paths`: allowlist baseline path; document overlay as non-synced / excluded
- `code-review`: import-linter owned; judgment remains for what contracts cannot express
- `global-principles` (optional note only if Code Quality examples need the CLI) — prefer docs/quality + principles
  Code Quality example without inventing a new requirement unless needed

## Impact

- `.pre-commit-config.yaml`, `reusable-code-quality.yml`, uv dep pin, synced baseline config, `docs/synced-paths.yaml`
- `docs/quality.md`, `openspec/principles.global.md` (example invocation)
- `.agents/skills/code-review/SKILL.md`, `docs/code-review.md`
- Product follow-up Tasks for overlays (API / harvester / sql-to-arc)
- Issue [#173](https://github.com/fairagro/m4.2_middleware_devinfra/issues/173)
