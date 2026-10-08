## Why

Operators must pick `major` / `minor` / `patch` on Release workflows and often guess wrong since the last tag. Auto
detecting the bump from [Conventional Commits](https://www.conventionalcommits.org/) (via lightweight **git-cliff**)
removes that guesswork. Detection only works if commit messages stay Conventional — so generation (Cursor sparkle
**and** VS Code / Copilot auto-commit) and enforcement (commitlint) must land with the detector.

## What Changes

- **BREAKING (workflow default):** `version_bump` gains `auto` and becomes the **default** (explicit `major`/`minor`/
  `patch` remain overrides) on shared Docker build/release and Helm final (and Pre-Release base bump — lock-in S2).
- Pin and use **git-cliff** to compute the next base semver from commits since the surface’s last tag (R1: Docker
  `*-docker-v*` vs Helm chart tags separately); fail closed when detection fails (F1).
- Thin wrapper keeps existing `build/*` RC suffix / PEP 440 logic on top of the cliff base version.
- Shared `cliff.toml` (+ sync allowlist as needed).
- **G2:** commitlint (or equivalent) in commit-stage / CI for Conventional Commits.
- Editor instructions so Cursor sparkle **and** VS Code Copilot commit-message generation emit Conventional Commits
  (synced `.vscode/settings.json` and/or Copilot commit instructions — not Cursor-only).

## Capabilities

### New Capabilities

<!-- none -->

### Modified Capabilities

- `reusable-ci-workflows`: `version_bump=auto` default; git-cliff-based detection for Docker and Helm release paths.
- `shared-quality-tooling`: Conventional Commits enforcement (commitlint) + docs for mapping / editor generation.
- `shared-devcontainer-base`: `GIT_CLIFF_VERSION` (or equivalent) pin; IDE commit-message generation instructions for
  Cursor and VS Code.
- `synced-consumer-paths`: allowlist any new shared cliff/commitlint/editor instruction files products must receive.

## Impact

- Devinfra: workflows, `versions.env`, scripts, `cliff.toml`, commitlint config, `.vscode` / Copilot instructions, docs,
  OpenSpec.
- Products: sync picks up pins/config; Release `workflow_dispatch` choice lists need `auto`; historical non-Conventional
  history may fail `auto` until override or message hygiene.
- Agents writing commits MUST follow Conventional Commits (issue-fixer / apply / sparkle / VS Code).
