## Context

See proposal.md — Why. Product `pyproject.toml` files now register `system_external` / `system_local`. Pytest does not
merge config files; fleet SoT for markers without product copies is
[#123](https://github.com/fairagro/m4.2_middleware_devinfra/issues/123) (out of scope here).

## Goals / Non-Goals

**Goals:**

- Fast default pre-push pytest via marker exclusion in synced pre-commit.
- Clear wait / `SKIP=pytest` UX and docs split vs CI.

**Non-Goals:**

- Pytest plugin / coverage fragment merge (#123).
- Changing reusable CI pytest invocation to inherit the pre-push `-m` filter.
- Making `SKIP=pytest` the normal developer path.

## Decisions

1. **Fixed `-m` in synced hook** — `not system_external and not system_local` (no `PRE_PUSH_PYTEST_ARGS` in this MVP).
2. **Banner in the pre-commit `entry`** — `bash -c` echoes before `uv run pytest …`.
3. **CI unchanged** — document that CI stays broad; products run `system_*` intentionally with explicit `-m` / path.

## Risks / Trade-offs

- [Products without the markers registered] → Mitigation: product issues landed markers on main; #123 for durable SoT.
- [Developers skip pytest habitually] → Docs: escape hatch only; not the supported cadence.

## Migration Plan

1. Merge this Devinfra change → sync `.pre-commit-config.yaml`.
2. Keep #123 for plugin/coverage follow-up; close product prep issues when verified.
