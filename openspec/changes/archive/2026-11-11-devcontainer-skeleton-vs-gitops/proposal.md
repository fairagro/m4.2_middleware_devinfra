## Why

Verbatim product `.devcontainer/*` sync would overwrite Infra’s GitOps Dev Container (argocd / kind / ct / …). After the
profile split (#350 / #351), product Dev Container files already sit on `python-product` only — #352 locks the
**model**, **pin ownership**, and **sync invariants** so that stays intentional and documented, without adopting Infra
onto a shared image yet.

## What Changes

- Document the Dev Container overlay model: **python-product** verbatim blob vs **gitops** tools owned by Infra until a
  dedicated adoption issue
- Document pin ownership (shared / python-product / Infra-owned): Helm + minikube (today) + git-lfs as shared-eligible;
  argocd / kind / ct Infra-owned; note planned product **minikube → kind** as follow-up (#364 / API #670), not this
  change
- Strengthen sync/docs/spec invariants: `.devcontainer/**` MUST stay off `foundation` / `gitops` / `infra-consumer`;
  Infra target MUST NOT receive product Dev Container files; Infra keeps its fat GitOps image until adoption says
  otherwise
- Add/extend sync profile tests that assert Infra effective allow excludes `.devcontainer/`
- **No** Dockerfile multi-stage rewrite, **no** new synced gitops Dockerfile, **no** Infra image adoption in this change

## Capabilities

### New Capabilities

<!-- none — extend existing sync + Dev Container contracts -->

### Modified Capabilities

- `synced-consumer-paths`: Explicit Dev Container / pin-ownership documentation requirements; Infra allow MUST exclude
  `.devcontainer/**`; product blob remains on `python-product` only
- `shared-devcontainer-base`: Clarify that the shared image/docs describe the **python-product** toolchain; Infra’s fat
  GitOps image is out of scope until adoption; document pin-ownership buckets and the deferred minikube→kind follow-up
- `product-repo-sync`: Tighten documented non-goals for Infra sync (no product Dev Container overwrite; Infra owns fat
  image until adoption)

## Impact

- Docs: `docs/sync.md`, `docs/devcontainer.md` (and brief cross-links in `docs/quality.md` if needed)
- Specs: deltas under the three capabilities above; archive syncs into main specs later
- Tests: `scripts/tests/test_sync_products_profiles.py` (Infra ∌ `.devcontainer/`)
- Out of scope: `#364` (kind swap), API `#670` (smoke docs), `#354` (Renovate/`versions.env` on Infra), Infra Dockerfile
  rewrite
