# Dev Container

Open this repo with **Dev Containers: Reopen in Container** (VS Code or Cursor).

The image is a lean bootstrap for developing **this** shared Devinfra repo (`gh`, OpenSpec CLI, uv/Python,
Docker-in-Docker). [Issue #10](https://github.com/fairagro/m4.2_middleware_devinfra/issues/10) will expand it into the
full product-shared toolchain; product repos will then keep only thin `devcontainer.json` overlays.

OpenSpec **specs/changes** for product work stay in the product repos
([epic #1](https://github.com/fairagro/m4.2_middleware_devinfra/issues/1)); this image only provides the OpenSpec CLI.

## Layout

| Path                               | Purpose                                                      |
| ---------------------------------- | ------------------------------------------------------------ |
| `.devcontainer/devcontainer.json`  | Compose service, DinD, mounts, extensions, postCreate        |
| `.devcontainer/docker-compose.yml` | Build args from `versions.env` via `.env` symlink            |
| `.devcontainer/Dockerfile`         | Pinned tooling image                                         |
| `versions.env`                     | Single source of truth for tool versions                     |
| `.devcontainer/.env`               | Symlink → `../versions.env` (Compose build-arg substitution) |

## Tool versions

All toolchain pins live in repo-root [`versions.env`](../versions.env):

- base image, Python, uv, Node, OpenSpec, Starship, hadolint, yq, …

[`.python-version`](../.python-version) is kept aligned with `PYTHON_VERSION` (via `scripts/load-versions-env.sh`, also
run from postCreate).

**After changing pins:** edit `versions.env`, then **Dev Containers: Rebuild Container**.

```bash
gh --version
openspec --version
uv --version
node --version
```

## Tools in the image

| Tool          | Notes                                                                                                 |
| ------------- | ----------------------------------------------------------------------------------------------------- |
| `gh`          | GitHub CLI (APT); auth persists in volume `middleware-devinfra-gh-config`                             |
| `openspec`    | [@fission-ai/openspec](https://www.npmjs.com/package/@fission-ai/openspec) via Node `${NODE_VERSION}` |
| `uv` / Python | For upcoming quality scripts and the agent GitHub CLI (#7, #16)                                       |

## Markdown (format + lint)

| Tool                                                       | Role                                                                                     | VS Code / Cursor extension             |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------------------- | -------------------------------------- |
| [Prettier](https://prettier.io)                            | Format (`printWidth` 120, `proseWrap: always`)                                           | `esbenp.prettier-vscode` (first-party) |
| [markdownlint](https://github.com/DavidAnson/markdownlint) | Structure lint; Prettier-compatible disables in `.markdownlint.json` (no `extends` path) | `davidanson.vscode-markdownlint`       |

Node `${NODE_VERSION}` is required anyway (OpenSpec). Prettier and markdownlint-cli2 are installed **globally in the Dev
Container image** (same pattern as OpenSpec) — a workspace `npm install` would be hidden by the bind mount. Pins live in
`versions.env` (`PRETTIER_VERSION`, `MARKDOWNLINT_CLI2_VERSION`); `package.json` mirrors them for local clones.

```bash
# In the Dev Container (binaries on PATH after rebuild):
npm run format:md           # prettier --write (including .cursor opsx files)
npm run format:md:check
npm run lint:md             # markdownlint-cli2

# Outside the image only:
npm install
```

Format on save is enabled for Markdown in this Dev Container (`esbenp.prettier-vscode`). Do not also turn on
markdownlint fix-on-save — Prettier owns formatting.

After `openspec update`: run `format:md`, then `lint:md`; remaining lint findings must be fixed by hand (or by the
agent) — Prettier cannot clear every rule.

**uv alternative:** [mdformat](https://github.com/hukkin/mdformat) installs via `uv tool install mdformat` /
`uvx mdformat`, but the VS Code extension (`bittorala.mdformat`) is unofficial and there is no markdownlint-class Python
linter with the same ecosystem. Prefer Prettier + markdownlint here.

## Bash history

History is stored in Docker volume `middleware-devinfra-bashhistory` (`HISTFILE=/commandhistory/.bash_history`). The
image sets a large `HISTFILESIZE`, `histappend`, and `HISTIGNORE` so Cursor/VS Code agent bootstrap lines (`set +/-o …`)
do not flood the file and age out real commands.

One-time cleanup if an older volume is already polluted:

```bash
grep -vE '^(set |unset |shopt )' /commandhistory/.bash_history \
  > /tmp/bash_history.clean \
  && mv /tmp/bash_history.clean /commandhistory/.bash_history
```

## Host / credentials

Git credentials, SSH agent, and GPG agent are forwarded by the Dev Containers extension — no custom bind mounts
required.

Ensure on the **host**:

- `git config --global user.name` / `user.email` are set
- SSH agent running with keys loaded (`ssh-add`) if you use SSH remotes

### gh auth (HTTPS)

Prefer the personal-token helpers (see root README **Personal tokens**):

- Stored `GH_TOKEN` in `/commandhistory/tokens.env` (Linux Dev Container only)
- Empty prompt skips until `source ./scripts/set-dev-tokens.sh`
- `scripts/bin/gh` on `PATH` (after rebuild) loads tokens then runs real `gh`

Alternatively:

```bash
gh auth login
```

`gh` CLI login credentials (if used) live in Docker volume `middleware-devinfra-gh-config` and survive rebuilds.

## postCreateCommand

Runs `scripts/devcontainer-post-create.sh` once per create:

- fix `/commandhistory` and `~/.config/gh` permissions
- write `.python-version` from `versions.env` via `scripts/load-versions-env.sh`
- ensure `~/.bashrc` sources `scripts/dev-tokens.sh` (load stored tokens; TTY prompts only when interactive)
- load stored tokens into the postCreate environment (no hang without TTY)

`PATH` with `scripts/bin` first comes from `.devcontainer/devcontainer.json` (`remoteEnv`) after rebuild.

Re-run anytime:

```bash
bash scripts/devcontainer-post-create.sh
```
