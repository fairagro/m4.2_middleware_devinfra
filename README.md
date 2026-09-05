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

Markdownlint and Prettier already exclude those paths. The shared [`.pre-commit-config.yaml`](.pre-commit-config.yaml)
applies the same vendor excludes.

## Quality (pre-commit)

Shared commit-stage / pre-push skeleton and helpers — see [`docs/quality.md`](docs/quality.md). Needs `uv` (and, for the
markdownlint hook, Node/`npm`: Dev Container has them global; on a host clone run `npm install` once). Prefer
`uv run pre-commit …` so the tool need not be on `PATH`:

```bash
uv sync
npm install   # host clones; optional in Dev Container (global markdownlint/prettier)
./scripts/quality-check.sh          # commit-stage, non-mutating
./scripts/quality-fix.sh            # autofix hooks
uv run pre-commit install --hook-type pre-commit   # usually postCreate / #10
./scripts/setup-git-lfs.sh          # LFS + pre-push git hooks (after clone / postCreate)
```

Pre-push **git** hook (`scripts/git-hooks/pre-push`: Git LFS then pre-commit pre-push stage) is installed by
`./scripts/setup-git-lfs.sh` — see [`docs/quality.md`](docs/quality.md). CST runner params (`CST_DOCKERFILE`,
`CST_IMAGE_TAG`, `CST_CONFIG`) are documented there.

**OpenSpec split:** product `openspec/specs/` and `openspec/changes/` stay local. The shared principles base is
`openspec/principles.global.md`; each repo extends it with a local `openspec/principles.md` (do not weaken Supported
environment or Type Safety in the local file).

## Personal tokens

Personal `GH_TOKEN` / `GITGUARDIAN_API_KEY` (see [path conventions](docs/conventions.md)):

- **Dev Container only:** `/commandhistory/tokens.env` (volume-backed). No host `~/.config/…` store.
- **Load path:** `scripts/bin/gh` and `scripts/bin/git` are first on `PATH` (`remoteEnv`) and source
  `scripts/dev-tokens.sh` (loads stored values; prompts only on a TTY). No `~/.bashrc` patch.
- **Empty prompt** = skip until you re-prompt: `source ./scripts/set-dev-tokens.sh`
- Do **not** put tokens in the git worktree.

Quality / CST / `load-versions-env` / `m42-ai` also run on a **host** checkout; token helpers and `scripts/bin` wrappers
do not — on the host, keep using your own env (e.g. `~/.bashrc`) or `gh auth`. See
[Script environments](docs/quality.md#script-environments).

## Tool versions

Toolchain pins live in [`versions.env`](versions.env) (single source of truth). [`.python-version`](.python-version)
stays aligned with `PYTHON_VERSION` from that file. See [Dev Container](docs/devcontainer.md) for edit and rebuild
steps.

## Docs

- [Dev Container](docs/devcontainer.md) — open, rebuild, tools, auth, postCreate
- [Path conventions](docs/conventions.md) — tokens, volumes, package root
- [Quality / pre-commit](docs/quality.md) — commit-stage scripts, CST runner, git-hooks / LFS install (#10 wires
  postCreate)
- [AI review policy](docs/ai_review_policy.md) — Finder/Fixer policy (Copilot, Bugbot, `/review-fixer`)
- [Review-fixer](docs/review-fixer.md) — open-work triage + no auto-commit for `/review-fixer`
- [Create-issue](docs/create-issue.md) — org issue types, triage labels, sub-of vs linked for `/create-issue`
- [Issue-fixer](docs/issue-fixer.md) — explore → draft PR → local implement for `/issue-fixer`
- [Shared principles](openspec/principles.global.md) — synced foundation; extend via
  [`openspec/principles.md`](openspec/principles.md)

## Layout

| Path                                      | Role                                                                  |
| ----------------------------------------- | --------------------------------------------------------------------- |
| `docs/`                                   | Feature documentation (grows over time)                               |
| `docs/ai_review_policy.md`                | Canonical AI review (Finder/Fixer) policy                             |
| `docs/review-fixer.md`                    | Thin index for `/review-fixer`                                        |
| `docs/create-issue.md`                    | Org issue types + triage labels + relation for `/create-issue`        |
| `docs/issue-fixer.md`                     | Thin index for `/issue-fixer`                                         |
| `docs/quality.md`                         | Pre-commit skeleton, quality scripts, CST params                      |
| `scripts/quality-check.sh`                | Commit-stage quality check                                            |
| `scripts/quality-fix.sh`                  | Commit-stage autofix hooks                                            |
| `scripts/run-container-structure-test.sh` | Templated Docker + container-structure-test runner                    |
| `scripts/setup-git-lfs.sh`                | Local Git LFS init + install `scripts/git-hooks/`                     |
| `scripts/git-hooks/`                      | pre-push (LFS + pre-commit) + LFS post-* hooks                        |
| `.pre-commit-config.yaml`                 | Shared pre-commit skeleton (commit + pre-push stages)                 |
| `.bandit`                                 | Bandit config for `middleware/` consumers                             |
| `scripts/ai/`                             | `m42-ai` CLI (auth, review, issue-view/branch/start, pr-strip-footer) |
| `openspec/principles.global.md`           | Shared principles base (synced; do not diverge in consumers)          |
| `openspec/principles.md`                  | Repo-local principles extension (points at `.global`)                 |
| `.agents/skills/review-fixer/`            | Shared `/review-fixer` Fixer skill                                    |
| `.agents/skills/create-issue/`            | Shared `/create-issue` creator skill                                  |
| `.agents/skills/issue-fixer/`             | Shared `/issue-fixer` Fixer skill                                     |
| `.agents/skills/gh/`                      | Vendor `gh` skill (committed; do not hand-edit)                       |
| `.agents/skills/docker/`                  | Vendor Docker skill (committed; do not hand-edit)                     |
| `.agents/skills/hadolint/`                | Vendor hadolint skill (committed; do not hand-edit)                   |
| `.agents/skills/uv/`                      | Vendor `uv` skill (committed; do not hand-edit)                       |
| `.cursor/commands/review-fixer.md`        | Cursor slash command for review-fixer                                 |
| `.cursor/commands/create-issue.md`        | Cursor slash command for create-issue                                 |
| `.cursor/commands/issue-fixer.md`         | Cursor slash command for issue-fixer                                  |
| `.github/prompts/`                        | Copilot prompts (review-fixer, create-issue, issue-fixer)             |
| `.cursor/`                                | Shared Cursor config (incl. `BUGBOT.md`)                              |
| `.github/`                                | Shared workflows / prompts (incl. `copilot-instructions.md`)          |
| `scripts/dev-tokens.sh`                   | Personal token load / prompt                                          |
| `scripts/bin/`                            | `gh` / `git` PATH wrappers                                            |
| `scripts/`                                | Shared scripts                                                        |
| `.devcontainer/`                          | Dev Container definition                                              |
| `versions.env`                            | Toolchain version pins                                                |
