# Dev Container (Cursor / VS Code) — step 0

Open with **Dev Containers: Reopen in Container**.

This is the bootstrap image for developing **this** shared Devinfra repo
(`gh`, OpenSpec, uv/Python, DinD). Issue
[#10](https://github.com/fairagro/m4.2_middleware_devinfra/issues/10) will
expand it into the full product-shared toolchain; product repos will then keep
only thin `devcontainer.json` overlays.

## Layout

| Path | Purpose |
| ---- | ------- |
| `devcontainer.json` | Compose service, DinD, mounts, extensions, postCreate |
| `docker-compose.yml` | Build args from `versions.env` via `.env` symlink |
| `Dockerfile` | Pinned tooling image |
| `../versions.env` | Single source of truth for tool versions |
| `.env` | Symlink → `../versions.env` (Compose build-arg substitution) |

## Required tools

| Tool | Notes |
| ---- | ----- |
| `gh` | GitHub CLI (APT); auth persists in volume `middleware-devinfra-gh-config` |
| `openspec` | [@fission-ai/openspec](https://www.npmjs.com/package/@fission-ai/openspec) via Node `${NODE_VERSION}` |
| `uv` / Python | For upcoming quality scripts and the agent GitHub CLI (#7, #16) |

After changing pins in `versions.env`, rebuild (**Dev Containers: Rebuild Container**).

```bash
gh --version
openspec --version
uv --version
node --version
```

OpenSpec **specs/changes** stay in the product repos (see epic #1); this image
only provides the CLI.

## Bash history

History is stored in Docker volume `middleware-devinfra-bashhistory`
(`HISTFILE=/commandhistory/.bash_history`). The image sets a large
`HISTFILESIZE`, `histappend`, and `HISTIGNORE` so Cursor/VS Code agent
bootstrap lines (`set +/-o …`) do not flood the file and age out real
commands.

One-time cleanup if an older volume is already polluted:

```bash
grep -vE '^(set |unset |shopt )' /commandhistory/.bash_history \
  > /tmp/bash_history.clean \
  && mv /tmp/bash_history.clean /commandhistory/.bash_history
```

## Host / credentials

Git credentials, SSH agent, and GPG agent are forwarded by the Dev Containers
extension — no custom bind mounts required.

Ensure on the **host**:

- `git config --global user.name` / `user.email` are set
- SSH agent running with keys loaded (`ssh-add`) if you use SSH remotes

### gh auth (HTTPS)

```bash
gh auth login
```

Credentials live in Docker volume `middleware-devinfra-gh-config` and survive
rebuilds.

## postCreateCommand

Runs `scripts/devcontainer-post-create.sh` once per create:

- fix `/commandhistory` and `~/.config/gh` permissions
- write `.python-version` from `versions.env` via `scripts/load-versions-env.sh`

Re-run anytime:

```bash
bash scripts/devcontainer-post-create.sh
```
