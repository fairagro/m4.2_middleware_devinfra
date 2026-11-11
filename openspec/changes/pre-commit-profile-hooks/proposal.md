## Why

A single root `.pre-commit-config.yaml` mixes foundation hygiene with python-product gates (`middleware/`, pytest, CST).
Syncing that full blob to `m4.2_infrastructure` would force no-op noise or the wrong contract (#347 / #351). Profiles
already exist (#350); hooks must compose the same way. Legacy “Wave A” wording in live docs/specs is obsolete and should
go.

## What Changes

- Split the shared pre-commit SoT into **composable fragments** (`foundation`, `python-product`, `gitops`) owned in
  Devinfra, with a documented merge/generate step that produces each consumer’s root `.pre-commit-config.yaml`
- Map hooks per locked explore: foundation = core hooks + gitleaks + md tooling + commitlint/commit-path-check;
  python-product = middleware quality + uv-audit + pre-push pytest/CST; gitops = helm-lint (actionlint/kubeconform
  later)
- **Ship for products** and **wire Infra**: python-product targets compose foundation ∪ python-product ∪ gitops
  (preserve today’s helm-lint); `infrastructure` receives foundation (± gitops) — never python-product hooks
- Update sync allowlists/docs so fragments and generated root configs follow profiles; keep “no full product hook blob
  on Infra”
- Remove obsolete “Wave A” / “Wave-A” wording from live SoT (`README.md`, main OpenSpec specs this change touches)

## Capabilities

### New Capabilities

- (none)

### Modified Capabilities

- `shared-quality-tooling`: pre-commit skeleton becomes profile fragments + compose; consumer root config is generated
- `synced-consumer-paths`: allowlist which hook fragments / generated configs sync per profile (foundation vs
  python-product vs gitops surfaces)
- `product-repo-sync`: drop Wave-A wording; document Infra hook compose (foundation ± gitops) vs product union
- `shared-git-hooks`: pre-push still invokes the consumer root `.pre-commit-config.yaml` (composed), not a fragment path

## Impact

- `.pre-commit-config.yaml`, new fragment paths under Devinfra, sync YAML/docs (`docs/quality.md`, `docs/sync.md`,
  README), possibly a small compose script + tests
- Three python-product consumers: migration to composed root (behavior should match today’s hook set)
- Infra: can adopt foundation (± gitops) hooks without python-product gates; depends on sync target already present
  (#350)
- Follow-ups stay separate: actionlint (#353), kubeconform (#348), Renovate (#354)
