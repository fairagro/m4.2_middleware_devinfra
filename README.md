# m4.2_middleware_devinfra

Shared source of truth for agent skills, quality tooling, Dev Container base, and reusable GitHub Actions used by:

- [m4.2_advanced_middleware_api](https://github.com/fairagro/m4.2_advanced_middleware_api)
- [m4.2_sql_to_arc](https://github.com/fairagro/m4.2_sql_to_arc)
- [m4.2_middleware_harvester](https://github.com/fairagro/m4.2_middleware_harvester)

Canonical shared files live **here**. Product repos consume them via sync PRs. Do **not** hand-edit synced paths in
consumers — land shared changes in this repo first. That includes the AI review policy, Finder entries
(`.cursor/BUGBOT.md`, `.github/copilot-instructions.md`), `/review-fixer`, `/create-issue`, and `/issue-fixer` (skills,
Cursor commands, Copilot prompts), the agent GitHub CLI (`scripts/ai/`, `m42-ai`), personal-token helpers
(`scripts/dev-tokens.sh`, `scripts/set-dev-tokens.sh`, `scripts/bin/gh`, `scripts/bin/git`), and
`openspec/principles.global.md`. Roadmap: [epic #1](https://github.com/fairagro/m4.2_middleware_devinfra/issues/1).

## Vendor agent skills

Committed vendor skills live under `.agents/skills/{gh,docker,hadolint,uv}/`. **Do not hand-edit** those trees —
reinstall or update via `gh skill`, then commit the result.

Install (project scope; Cursor / Copilot share `.agents/skills/`):

```bash
gh skill install cli/cli gh --scope project --agent cursor -f
gh skill install Mindrally/skills docker --scope project --agent cursor -f
gh skill install rshade/agent-skills hadolint --scope project --agent cursor -f
gh skill install balintdecsi/skills uv --scope project --agent cursor -f
```

Update to newer upstream releases when intentional:

```bash
gh skill update
```

Markdownlint and Prettier already exclude those paths. When a pre-commit skeleton lands later, apply the same excludes
there.

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
- [Review-fixer](docs/review-fixer.md) — open-work triage + no auto-commit for `/review-fixer`
- [Create-issue](docs/create-issue.md) — org issue types, triage labels, sub-of vs linked for `/create-issue`
- [Issue-fixer](docs/issue-fixer.md) — explore → draft PR → local implement for `/issue-fixer`
- [Shared principles](openspec/principles.global.md) — synced foundation; extend via
  [`openspec/principles.md`](openspec/principles.md)

## Layout

| Path                               | Role                                                                  |
| ---------------------------------- | --------------------------------------------------------------------- |
| `docs/`                            | Feature documentation (grows over time)                               |
| `docs/ai_review_policy.md`         | Canonical AI review (Finder/Fixer) policy                             |
| `docs/review-fixer.md`             | Thin index for `/review-fixer`                                        |
| `docs/create-issue.md`             | Org issue types + triage labels + relation for `/create-issue`        |
| `docs/issue-fixer.md`              | Thin index for `/issue-fixer`                                         |
| `scripts/ai/`                      | `m42-ai` CLI (auth, review, issue-view/branch/start, pr-strip-footer) |
| `openspec/principles.global.md`    | Shared principles base (synced; do not diverge in consumers)          |
| `openspec/principles.md`           | Repo-local principles extension (points at `.global`)                 |
| `.agents/skills/review-fixer/`     | Shared `/review-fixer` Fixer skill                                    |
| `.agents/skills/create-issue/`     | Shared `/create-issue` creator skill                                  |
| `.agents/skills/issue-fixer/`      | Shared `/issue-fixer` Fixer skill                                     |
| `.agents/skills/gh/`               | Vendor `gh` skill (committed; do not hand-edit)                       |
| `.agents/skills/docker/`           | Vendor Docker skill (committed; do not hand-edit)                     |
| `.agents/skills/hadolint/`         | Vendor hadolint skill (committed; do not hand-edit)                   |
| `.agents/skills/uv/`               | Vendor `uv` skill (committed; do not hand-edit)                       |
| `.cursor/commands/review-fixer.md` | Cursor slash command for review-fixer                                 |
| `.cursor/commands/create-issue.md` | Cursor slash command for create-issue                                 |
| `.cursor/commands/issue-fixer.md`  | Cursor slash command for issue-fixer                                  |
| `.github/prompts/`                 | Copilot prompts (review-fixer, create-issue, issue-fixer)             |
| `.cursor/`                         | Shared Cursor config (incl. `BUGBOT.md`)                              |
| `.github/`                         | Shared workflows / prompts (incl. `copilot-instructions.md`)          |
| `scripts/dev-tokens.sh`            | Personal token load / prompt                                          |
| `scripts/bin/`                     | `gh` / `git` PATH wrappers                                            |
| `scripts/`                         | Shared scripts                                                        |
| `.devcontainer/`                   | Dev Container definition                                              |
| `versions.env`                     | Toolchain version pins                                                |
