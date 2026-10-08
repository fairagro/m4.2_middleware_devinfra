## Context

See proposal.md — Why. Lock-ins from explore (#300): **C1=A** disable GitHub `generate_release_notes`; **C2=soft** empty
changelog; **C3=R1** surface tag ranges; **C4** Final Docker + Final Helm only (pre-releases do not persist GitHub
Releases); **C5** thin helper script; **C6** keep operational sections + `## Changelog` + optional compare link. Extra
MVP slice: editor guidance prefers optional Conventional Commits scopes without `scope-enum`.

Today Final releases build `release-body.md` then call `softprops/action-gh-release` with
`generate_release_notes: true`. `cliff.toml` already has tight commit parsers for auto-bump but an empty changelog
`body`.

## Goals / Non-Goals

**Goals:**

- Readable Conventional Commits changelog on Final GitHub Releases via git-cliff
- One shared helper + pin; soft empty path; clear cliff error logging
- Prefer optional component scopes in sparkle/Copilot/agent commit instructions

**Non-Goals:**

- Pre-release / RC GitHub Release changelogs
- commitlint `scope-enum` / mandatory scopes
- Rewriting registry-retry body replace logic beyond leaving `## Registry status` intact
- Pinning cliff checksums into `versions.env` (installer already verifies published `.sha512`)

## Decisions

1. **Disable GitHub auto-notes (C1=A)** — cliff owns the human changelog; avoid duplicate “What’s Changed”. Recreate the
   useful **Full Changelog** compare URL ourselves when `RANGE_FROM` exists.
2. **Soft empty (C2)** — placeholder under `## Changelog`; do not fail the release. Distinguish cliff non-zero exit
   (log + soft placeholder or fail soft with warning — prefer soft with stderr in logs so operators still get tags).
3. **Helper `scripts/generate-release-changelog.sh`** — `--surface docker|helm`, prints markdown (changelog + optional
   compare line using `GITHUB_REPOSITORY` / explicit repo args). Reuses tag-glob logic aligned with
   `detect-version-bump.sh` (same R1). Workflows `sudo` install cliff then call the helper when building the body.
4. **`cliff.toml` body template** — standard grouped sections (Features, Bug Fixes, etc.); keep existing parsers for
   bump + changelog consistency.
5. **Body insertion point** — after registry / meta, before or after licenses (Docker: after Build from Source / before
   licenses is fine); stable `## Changelog` heading for readers.
6. **Optional scopes in editor guidance** — update `.cursorrules`, Copilot commit instructions, `copilot-instructions`,
   `docs/quality.md`; no commitlint rule change.

## Risks / Trade-offs

- **[Risk]** Historical non-CC history → thin or “Other”-heavy changelogs → Mitigation: commitlint + optional scopes;
  soft empty
- **[Risk]** Soft-fail masks cliff crashes → Mitigation: log exit code + stderr; distinct placeholder wording when cliff
  failed vs empty
- **[Trade-off]** Same-channel `.sha512` already on installer; unchanged here

## Migration Plan

1. Land helper + cliff body + workflow wiring + editor guidance on Devinfra; sync to products.
2. Next Final releases pick up new body shape automatically (no caller API change beyond observing notes).
