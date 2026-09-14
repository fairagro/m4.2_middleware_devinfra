## ADDED Requirements

### Requirement: Bashrc-free PATH for venv and scripts/bin

This repository’s Dev Container `remoteEnv` MUST prepend `${workspaceFolder}/.venv/bin` and
`${workspaceFolder}/scripts/bin` on `PATH` (scripts/bin before or after `.venv/bin` is allowed as long as both appear
before the inherited container `PATH`). Shared postCreate and personal-token helpers MUST NOT patch `~/.bashrc` (or
other user shell profiles) to inject that PATH or to source a load-env script. Documentation MUST state that product
`devcontainer.json` overlays MUST carry the same `remoteEnv.PATH` contract so every integrated terminal and remote
process sees uv tool binaries and `scripts/bin` wrappers without home-profile mutation.

#### Scenario: Devinfra remoteEnv includes venv and scripts/bin

- **WHEN** a contributor inspects this repository’s `.devcontainer/devcontainer.json` `remoteEnv.PATH`
- **THEN** both `${workspaceFolder}/.venv/bin` and `${workspaceFolder}/scripts/bin` appear on that PATH value
- **AND** postCreate does not append a `source …/load-env.sh` (or equivalent) line to `~/.bashrc`

#### Scenario: Docs require the same PATH contract for products

- **WHEN** a contributor reads Dev Container adoption docs for product overlays
- **THEN** they learn product `devcontainer.json` MUST set the same `remoteEnv.PATH` prepend for `.venv/bin` and
  `scripts/bin`
- **AND** they learn the fleet MUST NOT rely on patching `~/.bashrc` for that PATH

### Requirement: kubectl and docker shortcut wrappers on scripts/bin

The repository MUST provide executable wrappers under `scripts/bin/` that invoke the shared Dev Container’s kubectl and
docker installs (`/usr/local/bin/kubectl` from the shared Dockerfile pin; `/usr/bin/docker` from the Docker-in-Docker
feature) under the short names formerly used as product bash aliases (`k`, `d`). Those wrappers MUST be listed on the
product sync allowlist with other `scripts/bin` helpers. The wrappers MUST NOT search `PATH` for alternate binaries,
MUST NOT load personal tokens, and MUST NOT patch shell profiles.

#### Scenario: Short names resolve via scripts/bin

- **WHEN** `scripts/bin` is on `PATH` and a contributor runs `k` or `d` in the shared Linux Dev Container
- **THEN** `k` execs `/usr/local/bin/kubectl` and `d` execs `/usr/bin/docker`
- **AND** the wrappers do not source `dev-tokens.sh` or modify `~/.bashrc`

### Requirement: Image bash-completion for kubectl and docker short names

The shared Dev Container image MUST install bash-completion entries under `/usr/share/bash-completion/completions/` for
the short names `k` and `d` that register the same completion functions as `kubectl` and `docker` (respectively),
without patching `~/.bashrc`. The `k` entry MUST reuse the image’s kubectl completion (already generated at image
build). The `d` entry MUST bind to docker’s completion function when the docker completion file is available in the
running container (e.g. after the Docker-in-Docker feature installs the client). Documentation MUST state that
short-name completion comes from the shared image, not from product `load-env.sh`.

#### Scenario: k completion registered in the image

- **WHEN** a contributor inspects `/usr/share/bash-completion/completions/k` in the shared image
- **THEN** that file registers programmable completion for `k` using `__start_kubectl`
- **AND** it does not instruct products to patch `~/.bashrc` for that binding

#### Scenario: d completion registered for docker short name

- **WHEN** bash-completion loads the `d` completion entry and docker’s completion function is available
- **THEN** `d` is registered with `__start_docker` (or equivalent docker completion entrypoint)
- **AND** no `~/.bashrc` mutation is required for that registration

### Requirement: Optional postCreate decrypt of integration env ciphertext

When postCreate runs in a Linux Dev Container and the repository root contains a SOPS-encrypted `.env.integration.enc`,
postCreate MUST attempt to decrypt it to repo-root `.env` using `sops` when available. If `.env` already exists and is
non-empty, postCreate MUST skip decryption. If the ciphertext file is absent, or `sops` / keys are unavailable,
postCreate MUST skip cleanly without failing the whole create. PostCreate MUST NOT patch `~/.bashrc` to auto-`source`
`.env` into interactive shells; leaving the plaintext `.env` file for `dev_environment` / tests that read it is
sufficient.

#### Scenario: Ciphertext present and decrypt succeeds

- **WHEN** postCreate runs and `.env.integration.enc` exists as SOPS ciphertext and decrypt succeeds
- **THEN** repo-root `.env` is written (or left unchanged if already non-empty)
- **AND** postCreate does not append bashrc lines that `source` `.env`

#### Scenario: Ciphertext absent

- **WHEN** postCreate runs and `.env.integration.enc` is missing
- **THEN** postCreate completes successfully without requiring SOPS decrypt

## MODIFIED Requirements

### Requirement: Consumer overlay documentation

Documentation (`docs/devcontainer.md` and/or README) MUST state that product repos keep a thin `devcontainer.json`
overlay owning at least `name`, `workspaceFolder`, and distinct Docker volume `source=` names (and MAY trim or add
extensions), while shared Dockerfile, compose build definition, `versions.env`, and scripts are consumed from this
Devinfra repo (via sync). Shared fragments MUST NOT hardcode another product’s `workspaceFolder` or volume source names.
Docs MUST state that product **ciphertext** and recipient config (`.sops.yaml`, encrypted secret files) and
`public_gpg_keys` **content** stay in each product repo, while the shared image provides sops/age/gpg/JRE/graphviz and
postCreate performs key import when keys are present. Docs MUST state that **Git LFS** is not part of the shared image;
products that need LFS (e.g. sql-to-arc) MUST install it in a product-owned path that sync of the shared Dockerfile does
not overwrite (e.g. product postCreate or a non-synced local fragment). Docs MUST state the bashrc-free shell contract:
product overlays MUST set `remoteEnv.PATH` to prepend `.venv/bin` and `scripts/bin`; fleet shell init MUST NOT patch
`~/.bashrc` for PATH, aliases, tokens, completions, or sourcing `load-env.sh`; kubectl/docker short-name bash completion
is provided by the shared image; optional `.env.integration.enc` decrypt runs in shared postCreate and does not
auto-export into every shell; product-local `load-env.sh` / bashrc wiring is deprecated in favor of this contract
(product migration tracked in follow-up issues, not required inside the Devinfra MVP PR).

#### Scenario: Contributor reads overlay guidance

- **WHEN** a contributor opens the Dev Container docs for product adoption
- **THEN** they learn which fields stay product-local in `devcontainer.json`
- **AND** they learn the shared image/`versions.env`/scripts live in Devinfra and must not encode another product’s
  folder or volume names
- **AND** they learn secret file **content** stays product-local while tooling and key-import behavior are shared
- **AND** they learn Prettier + markdownlint-cli2 (and their extensions) are the shared markdown format/lint stack that
  replaces or supplements prior product-local markdown tooling on sync
- **AND** they learn Git LFS is product-local when needed, not a shared base requirement
- **AND** they learn `remoteEnv.PATH` must prepend `.venv/bin` and `scripts/bin` without patching `~/.bashrc`
- **AND** they learn `k`/`d` bash completion comes from the shared image completion files
- **AND** they learn product `load-env.sh` / bashrc sourcing is not the shared pattern after sync adopt
