## Context

See proposal.md — Why. Lock-in #200: style **B** (ARG defaults). Channel `ci/issue-200-…`.

## Goals / Non-Goals

**Goals:** One documented apk pin style; script updates ARG defaults from APKINDEX; fail closed on stale/unknown/forbidden
inline apk version literals; pip `name==` still updated.

**Non-Goals:** Migrating every product Dockerfile in this PR; Renovate apk datasource; changing `versions.env` toolchain
ARGs; reviving `.bak` sidecars (#167 done).

## Decisions

1. **ARG ↔ package map:** `ARG FOO_BAR_VERSION=…` maps to apk package `foo-bar` (strip `_VERSION`, lower-case, `_` → `-`).
2. **Update target:** rewrite only the default on `^ARG <NAME>_VERSION=<apk-ver>` lines; do not rewrite `${…}` references.
3. **Forbidden:** Alpine-style inline `name=X.Y.Z-rN` in product Dockerfiles the script updates → ERROR (exit non-zero)
   after reporting, so style A cannot silently remain.
4. **Loud misses:** ARG apk pin whose package is missing from APKINDEX → ERROR (not “skip” + Done).
5. **Pip:** unchanged `name==` PyPI bumps; PyPI lookup failure may skip with message (existing) unless we want fail —
   keep skip for pip to avoid blocking apk-only refresh networks; apk failures are hard errors.

## Risks / Trade-offs

- [Toolchain ARGs like `PYTHON_VERSION`] → Only match `ARG …_VERSION=` values that look like `*-rN` apk versions.
- [Products still on style A] → Loud failure nudges migration; document in renovate.md.

## Migration Plan

1. Land script + docs in Devinfra; sync.
2. Product PRs convert last-stage apk pins to ARG style, then re-run the helper.

## Open Questions

None.
