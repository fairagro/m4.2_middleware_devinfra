# m4.2_middleware_devinfra

Shared source of truth for agent skills, quality tooling, Dev Container base, and reusable GitHub Actions used by:

- [m4.2_advanced_middleware_api](https://github.com/fairagro/m4.2_advanced_middleware_api)
- [m4.2_sql_to_arc](https://github.com/fairagro/m4.2_sql_to_arc)
- [m4.2_middleware_harvester](https://github.com/fairagro/m4.2_middleware_harvester)

Canonical shared files live **here**. Product repos consume them via sync PRs. Do **not** hand-edit synced paths in
consumers — land shared changes in this repo first. That includes the AI review policy, Finder entries
(`.cursor/BUGBOT.md`, `.github/copilot-instructions.md`), `/review-fixer` (`.agents/skills/review-fixer/`, Cursor
command, Copilot prompt), personal-token helpers (`scripts/dev-tokens.sh`, `scripts/bin/gh`), and
`openspec/principles.global.md`. Roadmap: [epic #1](https://github.com/fairagro/m4.2_middleware_devinfra/issues/1).

**OpenSpec split:** product `openspec/specs/` and `openspec/changes/` stay local. The shared principles base is
`openspec/principles.global.md`; each repo extends it with a local `openspec/principles.md` (do not weaken Supported
environment or Type Safety in the local file).

## Personal tokens

Personal `GH_TOKEN` / `GITGUARDIAN_API_KEY` (see [path conventions](docs/conventions.md)):

- **Dev Container:** `/commandhistory/tokens.env` (volume-backed).
- **Host clone:** `~/.config/<git-repo-name>/tokens.env` — name from `origin` (e.g. `m4.2_middleware_devinfra`); no
  `PRODUCT_SLUG` required.
- **Kombi:** interactive shells source `scripts/dev-tokens.sh` after postCreate (loads stored values; prompts only on a
  TTY). `scripts/bin/gh` and `scripts/bin/git` stay on `PATH` for agents / Cursor SCM.
- **Empty prompt** = skip until you re-prompt: `source ./scripts/set-dev-tokens.sh`
- Do **not** put tokens in the git worktree.

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

| Path                               | Role                                                         |
| ---------------------------------- | ------------------------------------------------------------ |
| `docs/`                            | Feature documentation (grows over time)                      |
| `docs/ai_review_policy.md`         | Canonical AI review (Finder/Fixer) policy                    |
| `openspec/principles.global.md`    | Shared principles base (synced; do not diverge in consumers) |
| `openspec/principles.md`           | Repo-local principles extension (points at `.global`)        |
| `.agents/skills/review-fixer/`     | Shared `/review-fixer` Fixer skill                           |
| `.cursor/commands/review-fixer.md` | Cursor slash command for review-fixer                        |
| `.github/prompts/`                 | Copilot prompts (incl. review-fixer)                         |
| `.cursor/`                         | Shared Cursor config (incl. `BUGBOT.md`)                     |
| `.github/`                         | Shared workflows / prompts (incl. `copilot-instructions.md`) |
| `scripts/dev-tokens.sh`            | Personal token load / prompt                                 |
| `scripts/bin/`                     | `gh` / `git` PATH wrappers                                   |
| `scripts/`                         | Shared scripts                                               |
| `.devcontainer/`                   | Dev Container definition                                     |
| `versions.env`                     | Toolchain version pins                                       |
