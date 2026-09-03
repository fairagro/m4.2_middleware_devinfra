# m4.2_middleware_devinfra

Shared source of truth for agent skills, quality tooling, Dev Container base, and reusable GitHub Actions used by:

- [m4.2_advanced_middleware_api](https://github.com/fairagro/m4.2_advanced_middleware_api)
- [m4.2_sql_to_arc](https://github.com/fairagro/m4.2_sql_to_arc)
- [m4.2_middleware_harvester](https://github.com/fairagro/m4.2_middleware_harvester)

Canonical shared files live **here**. Product repos consume them via sync PRs. Do **not** hand-edit synced paths in
consumers — land shared changes in this repo first. That includes the AI review policy, Finder entries
(`.cursor/BUGBOT.md`, `.github/copilot-instructions.md`), and `openspec/principles.global.md`. Roadmap:
[epic #1](https://github.com/fairagro/m4.2_middleware_devinfra/issues/1).

**OpenSpec split:** product `openspec/specs/` and `openspec/changes/` stay local. The shared principles base is
`openspec/principles.global.md`; each repo extends it with a local `openspec/principles.md` (do not weaken Supported
environment or Type Safety in the local file).

## Tool versions

Toolchain pins live in [`versions.env`](versions.env) (single source of truth). [`.python-version`](.python-version)
stays aligned with `PYTHON_VERSION` from that file. See [Dev Container](docs/devcontainer.md) for edit and rebuild
steps.

## Docs

- [Dev Container](docs/devcontainer.md) — open, rebuild, tools, auth, postCreate
- [Path conventions](docs/conventions.md) — tokens, volumes, package root
- [AI review policy](docs/ai_review_policy.md) — Finder/Fixer policy (Copilot, Bugbot, `/review-fixer`)
- [Shared principles](openspec/principles.global.md) — synced foundation; extend via
  [`openspec/principles.md`](openspec/principles.md)

## Layout

| Path                            | Role                                                         |
| ------------------------------- | ------------------------------------------------------------ |
| `docs/`                         | Feature documentation (grows over time)                      |
| `docs/ai_review_policy.md`      | Canonical AI review (Finder/Fixer) policy                    |
| `openspec/principles.global.md` | Shared principles base (synced; do not diverge in consumers) |
| `openspec/principles.md`        | Repo-local principles extension (points at `.global`)        |
| `.agents/skills/`               | Shared agent skills (later extracts)                         |
| `.cursor/`                      | Shared Cursor config (incl. `BUGBOT.md`)                     |
| `.github/`                      | Shared workflows / prompts (incl. `copilot-instructions.md`) |
| `scripts/`                      | Shared scripts                                               |
| `.devcontainer/`                | Dev Container definition                                     |
| `versions.env`                  | Toolchain version pins                                       |
