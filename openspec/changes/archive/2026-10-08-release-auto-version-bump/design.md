## Context

See proposal.md — Why. Lock-in: **D2** git-cliff, **F1** fail closed, **S2** Final + Pre-Release base, **R1**
per-surface tags, **G2** commitlint + Conventional generation for **Cursor sparkle and VS Code Copilot** commit
messages.

Today `reusable-build.yml` / Helm final take `version_bump` ∈ {major,minor,patch} (default patch) and bump the latest
matching tag in shell. Pre-release adds `-rc.<branch>.<run>` on `build/*`.

## Goals / Non-Goals

**Goals:**

- `auto` default; explicit overrides remain.
- git-cliff computes next **base** semver from Conventional Commits since the relevant last tag.
- Same auto path for Final and Pre-Release (S2): cliff → base; existing RC/PEP440 suffix unchanged.
- Fail closed with a clear error when cliff cannot determine a bump (F1).
- commitlint on commit-stage (and CI parity as already patterned for other gates).
- Synced editor instructions for Cursor **and** VS Code Copilot generate-commit-message.

**Non-Goals:**

- Full GitVersion.
- Replacing GitHub Releases/changelog UX with git-cliff changelog as primary product surface (cliff may be used only for
  bump; changelog generation optional later).
- Rewriting historical commit messages.
- Cursor-only guidance.

## Decisions

1. **Tool:** git-cliff pinned in `versions.env` (`GIT_CLIFF_VERSION`), on Dev Container `PATH`, installed in Release
   jobs (setup action or binary download — match existing Helm/Trivy pin patterns).
2. **Config:** shared `cliff.toml` with `tag_pattern` appropriate per invocation (Docker vs Helm via CLI override / env
   / thin wrapper args — R1).
3. **Wrapper:** `scripts/detect-version-bump.sh` (or similar) wraps `git cliff --bumped-version` (and/or compares to
   latest tag to emit `major|minor|patch` if workflows still want the case statement). Prefer emitting the **base
   version string** and letting workflows attach RC suffix — fewer dual parsers.
4. **Fail closed:** non-zero exit + message if no tag match, empty history edge cases that cliff cannot bump, or cliff
   missing; operators use explicit `version_bump`.
5. **commitlint:** `@commitlint/cli` + conventional config in root npm SoT; pre-commit hook; reusable-code-quality check
   when Node already present.
6. **Editor generation:** synced `.vscode/settings.json` key(s) for Copilot commit message instructions (VS Code)
   **and** Cursor-compatible guidance (same file and/or `.github/copilot-instructions.md` / small rule) stating
   Conventional Commits shape. Do not require a Cursor-only private format.
7. **Sync:** allowlist `cliff.toml`, commitlint config, detect script, any new instruction fragments.

## Risks / Trade-offs

- **[Risk]** Noisy history without Conventional Commits → `auto` fails often → Mitigation: F1 + docs + commitlint +
  editor instructions; explicit override.
- **[Risk]** Docker/Helm tag skew (R1) → Mitigation: document; operators release each surface knowingly.
- **[Trade-off]** Installing git-cliff in GHA vs only DC → both needed for local dry-run and CI.
- **[Trade-off]** commitlint friction on Renovate `deps:` commits → configure commitlint to accept Renovate’s prefix /
  types (align with existing `commitMessagePrefix: "deps:"`).

## Migration Plan

1. Land pin, cliff.toml, wrapper, workflow `auto` default, commitlint, editor settings, docs.
2. Sync to products; update thin Release `workflow_dispatch` choice lists.
3. Operators: first `auto` runs may need overrides until recent commits are Conventional.
