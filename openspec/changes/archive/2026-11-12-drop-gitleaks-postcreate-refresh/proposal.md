# Proposal

## Why

postCreate soft-refreshes **gitleaks** while other commit-stage CLIs (**actionlint**, **kubeconform**) require a Dev
Container **image rebuild**. That split confuses operators after sync
([#384](https://github.com/fairagro/m4.2_middleware_devinfra/issues/384); lock-in from
[#383](https://github.com/fairagro/m4.2_middleware_devinfra/issues/383)). Align gitleaks with the image-only story.

## What Changes

- Remove the gitleaks `install-pinned-tool.sh` block from `scripts/devcontainer-post-create.sh`
- Spec: gitleaks on PATH after **image rebuild** (same bar as actionlint); CI keeps `install-pinned-tool.sh gitleaks`
- Spec: shared postCreate MUST NOT refresh pinned CLI tools via the installer
- Docs: drop “legacy postCreate gitleaks refresh” wording introduced for #383

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `shared-quality-tooling`: gitleaks availability after Dev Container **rebuild**, not postCreate refresh
- `shared-devcontainer-base`: generic postCreate MUST NOT soft-refresh pinned CLIs via `install-pinned-tool.sh`

## Impact

- `scripts/devcontainer-post-create.sh` (synced via `python-product`)
- `docs/devcontainer.md`, `docs/quality.md`
- OpenSpec main specs after archive; CI install path unchanged
