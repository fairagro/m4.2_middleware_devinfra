## Why

A single root `.pre-commit-config.yaml` mixes foundation hygiene with python-product gates (`middleware/`, pytest, CST).
Syncing that full blob to `m4.2_infrastructure` would force no-op noise or the wrong contract (#347 / #351). Profiles
already exist (#350). Legacy lettered “wave” adopt wording in live docs/specs is obsolete and should go.

## What Changes

- Keep **two hand-maintained** pre-commit roots (no fragment merge script): `.pre-commit-config.yaml` (product =
  foundation + python-product + gitops hooks) and `.pre-commit-config.infrastructure.yaml` (foundation + gitops only)
- Map hooks per locked explore: foundation = core + gitleaks + md + commitlint/commit-path-check; python-product =
  middleware quality + uv-audit + pre-push pytest/CST; gitops = helm-lint (actionlint/kubeconform later) — shared hooks
  are duplicated across the two files when needed
- **Ship for products** and **wire Infra**: sync product root to python-product targets; sync Infra root (+ helpers /
  helm runner) to `infrastructure` — never the product pre-commit blob
- Update sync allowlists/docs; remove obsolete lettered “wave” adopt labels from live SoT

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-quality-tooling`: dual full pre-commit configs by consumer matrix (not fragment compose)
- `synced-consumer-paths`: allowlist product vs Infra pre-commit roots and related helpers by profile
- `product-repo-sync`: drop obsolete wave labels; document Infra vs product hook files
- `shared-git-hooks`: pre-push still uses consumer root `.pre-commit-config.yaml` (Infra installs/copies the Infra file)

## Impact

- `.pre-commit-config.yaml`, `.pre-commit-config.infrastructure.yaml`, sync YAML/docs (`docs/quality.md`,
  `docs/sync.md`, README)
- Three python-product consumers: unchanged install path (product root)
- Infra: adopts Infra-specific config without python-product gates (#350 target already exists)
- Follow-ups: actionlint (#353), kubeconform (#348), Renovate (#354)
