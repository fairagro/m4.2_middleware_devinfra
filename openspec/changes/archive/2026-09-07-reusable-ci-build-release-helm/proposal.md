# Reusable CI: build, release, and Helm

## Why

Issue #11 landed shared code-quality and check reusables; product repos still copy `reusable-build.yml`,
`reusable-release.yml`, and Helm chart publish workflows. Issue #12 (explore lock-in **H1**) moves the Docker
build/release **and** Helm publish paths into Devinfra so all three m4.2 products share one contract. PyPI and ns-pages
stay API-local.

## What Changes

- Add `.github/workflows/reusable-build.yml` adapted from the API: version calculation (`*-docker-v*` scheme, binding
  for all three products), Docker/SBOM build, artifacts matching the existing check contract from #11.
- Add `.github/workflows/reusable-release.yml` (MVP **B1**): push images to DockerHub + GHCR, optional GitHub
  release/tag with `tag_prefix` (default `docker-v`); **no** PyPI jobs.
- Add reusable Helm publish workflow(s) adapted from API `helm-release` / `helm-pre-release` (chart package + OCI push
  to DockerHub/GHCR, `*-chart-v*` tags), parameterized via `workflow_call` inputs (`chart_dir`, `chart_name`,
  namespaces, bump, …).
- Prefer **`workflow_call` inputs** for product-distinguishing names (**A1**); do not rely on silent
  `vars.IMAGE_BASE_NAME` defaults for correct product identity.
- Extend `docs/ci.md` with concrete caller snippets for feature-PR / release (Docker) and Helm dispatch callers
  (**D2**); update issue #12 narrative (Helm no longer “product-only”).
- **Out of scope:** flipping product `uses:` (#13); ns-pages; PyPI; a Devinfra-repo smoke job that itself builds/pushes
  product images; changing the #11 check artifact contract incompatibly.

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `reusable-ci-workflows`: Add requirements for reusable build, Docker release (B1), and Helm publish; replace the #11
  doc requirement that deferred build/release; document caller patterns including Helm.

## Impact

- New workflow YAML under `.github/workflows/`; `docs/ci.md`; main spec `openspec/specs/reusable-ci-workflows/spec.md`
  (via archive/sync later).
- Product repos keep thin callers until #13; API retains local PyPI + ns-pages workflows.
- Explore lock-ins: A1, B1, C.1 (shared Docker tag scheme), H1 (Helm in this change), D2, E as clarified (registry push
  happens when **products** call release — not a Devinfra-only smoke push).
