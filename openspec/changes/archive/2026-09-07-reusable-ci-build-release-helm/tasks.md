# Tasks: reusable CI build, release, and Helm

## 1. Docker build reusable

- [x] 1.1 Add `.github/workflows/reusable-build.yml` adapted from the API: `workflow_call` inputs for `version_bump`,
      `components`, `image_base_name`, and `skip`; shared `*-docker-v*` version job; outputs `version` and
      `pep440_version`
- [x] 1.2 Implement per-component Docker build + SBOM so uploaded artifacts match the #11 check contract
      (`docker-image-…`, `sbom-…`, local tag `local/<image_base_name>-<component>:<version>`)
- [x] 1.3 Wire toolchain pins via caller `versions.env` / `scripts/load-versions-env.sh` like other reusables

## 2. Docker release reusable (B1)

- [x] 2.1 Add `.github/workflows/reusable-release.yml` with inputs for version, pep440 (unused for PyPI), components,
      `image_base_name`, registry namespaces, `release_type`, `tag_prefix` (default `docker-v`),
      `create_github_release`, and secrets for DockerHub (+ `GITHUB_TOKEN` for GHCR)
- [x] 2.2 Implement DockerHub + GHCR push from build artifacts; optional GitHub release/tag; **omit** all PyPI/TestPyPI
      jobs

## 3. Helm publish reusables (H1)

- [x] 3.1 Add `reusable-helm-release.yml` and `reusable-helm-pre-release.yml` (or one parameterized file if clearer)
      with `workflow_call` inputs for `chart_dir`, `chart_name`, version bump / chart version path, and registry naming
- [x] 3.2 Port package + OCI push to DockerHub/GHCR, `*-chart-v*` tagging, and fail-clearly when no Docker tag exists
      for `appVersion`; no ns-pages steps

## 4. Documentation and issue alignment

- [x] 4.1 Extend `docs/ci.md`: build/release/Helm tables, inputs, build→check contract reminder, concrete feature-PR /
      release / Helm caller snippets; note PyPI + ns-pages stay API-local
- [x] 4.2 Update README CI pointer if needed; align issue #12 task wording with H1 (Helm shared) via issue comment or
      body edit when opening the draft PR

## 5. Verify

- [x] 5.1 `openspec validate reusable-ci-build-release-helm --strict` (or current validate invocation)
- [x] 5.2 `npm run format:md` and `npm run lint:md` on touched Markdown
