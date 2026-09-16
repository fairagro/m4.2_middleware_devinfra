## 1. Registry retry orchestrator

- [x] 1.1 Add `reusable-registry-retry.yml` with validate, nested bake/push, body replace; fail-closed flags/secrets
- [x] 1.2 Docker path via nested bake + registry-push; no tag/Release create
- [x] 1.3 Helm path via Release `.tgz` artifact + nested helm-oci-push; no version bump/tag create
- [x] 1.4 Replace `## Registry status` only; other sections preserved

## 2. Shared nested reusables (no composites)

- [x] 2.1 Add `reusable-docker-bake.yml`, `reusable-docker-registry-push.yml`, `reusable-helm-oci-push.yml`
- [x] 2.2 Wire build, release, helm-release, helm-pre-release, registry-retry via `$/.github/workflows/…`
- [x] 2.3 Remove `.github/actions/*` composites if present

## 3. Documentation

- [x] 3.1 Update `docs/ci.md` (retry + nested `$/` bake/push); `format:md` / `lint:md`

## 4. OpenSpec validate

- [x] 4.1 `openspec validate registry-retry-publish --strict`
