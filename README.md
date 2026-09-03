# m4.2_middleware_devinfra

Shared source of truth for agent skills, quality tooling, Dev Container base, and
reusable GitHub Actions used by:

- [m4.2_advanced_middleware_api](https://github.com/fairagro/m4.2_advanced_middleware_api)
- [m4.2_sql_to_arc](https://github.com/fairagro/m4.2_sql_to_arc)
- [m4.2_middleware_harvester](https://github.com/fairagro/m4.2_middleware_harvester)

Canonical shared files live **here**. Product repos consume them via sync PRs.
Do **not** hand-edit synced paths in consumers — land shared changes in this
repo first. Roadmap: [epic #1](https://github.com/fairagro/m4.2_middleware_devinfra/issues/1).

## Tool versions

Toolchain pins live in [`versions.env`](versions.env) (single source of truth).
[`.python-version`](.python-version) stays aligned with `PYTHON_VERSION` from
that file. See [Dev Container](docs/devcontainer.md) for edit and rebuild steps.

## Docs

- [Dev Container](docs/devcontainer.md) — open, rebuild, tools, auth, postCreate

## Layout

| Path | Role |
| ---- | ---- |
| `docs/` | Feature documentation (grows over time) |
| `.agents/skills/` | Shared agent skills (later extracts) |
| `.cursor/` | Shared Cursor commands / config (later extracts) |
| `.github/` | Shared workflows and prompts (later extracts) |
| `scripts/` | Shared scripts |
| `.devcontainer/` | Dev Container definition |
| `versions.env` | Toolchain version pins |
