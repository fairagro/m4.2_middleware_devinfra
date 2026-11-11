## ADDED Requirements

### Requirement: Product Dev Container vs Infra GitOps image ownership

Documentation for the shared Dev Container (`docs/devcontainer.md` and cross-links from `docs/sync.md`) MUST state that
`.devcontainer/Dockerfile`, `devcontainer.json`, `docker-compose.yml`, `starship.toml`, and `versions.env` describe the
**python-product** toolchain synced to api / sql_to_arc / harvester. They MUST state that `m4.2_infrastructure` keeps
owning its fat GitOps Dev Container (argocd / kind / chart-testing / related tools) until a dedicated adoption issue
explicitly moves Infra onto a shared Devinfra target or overlay. Docs MUST publish pin-ownership buckets:

- **Shared / foundation-eligible:** Helm, minikube (current product local-cluster tool), git-lfs (shared-eligible; the
  existing shared-image rule that git-lfs is not a _required_ install on the product happy path remains until a separate
  change installs it), plus other shared CLIs already in `versions.env`
- **python-product:** Python/uv, CST, Trivy, Renovate, git-cliff, product-app image pins, and other product-only quality
  toolchain pins
- **Infra-owned until adoption:** argocd, kind, chart-testing (`ct`)

Docs MUST name the deferred product **minikube → kind** swap as a separate follow-up (not implied by this ownership
doc). This requirement MUST NOT by itself change the installed product image tool set.

#### Scenario: Docs separate product image from Infra GitOps image

- **WHEN** a contributor reads Dev Container or sync docs about Infra adoption
- **THEN** they learn product `.devcontainer/*` is python-product sync only
- **AND** they learn Infra keeps its fat GitOps image until an adoption issue says otherwise
- **AND** they find the shared / python-product / Infra-owned pin buckets
- **AND** they learn minikube→kind for products is a separate follow-up
