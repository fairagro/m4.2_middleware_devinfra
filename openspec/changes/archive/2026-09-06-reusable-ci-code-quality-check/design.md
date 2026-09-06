# Design: reusable-ci-code-quality-check

## Context

See `proposal.md` for motivation. Product API already has modern `reusable-code-quality.yml` / `reusable-check.yml`
(versions.env, `skip`, current action majors). Harvester copies are older. Devinfra has no workflows yet; epic #1 places
canonical CI here after the Dev Container base (#10, done). Explore lock-ins for issue #11: **A1** (workflows + docs
only), **B3** (ship check with explicit artifact contract; build stays product-local until later), **C1** (package-root
input; Python from `versions.env`), **D1** (keep job name `Code Quality Check (3.12)`), **E3** (document `@main` and
recommend tag/SHA pins).

## Goals / Non-Goals

**Goals:**

- One canonical pair of callable workflows in this repo that API/harvester/sql_to_arc can eventually `uses:` without
  forking quality/check logic.
- Clear, parameterized contracts for package root and check artifacts/image naming.
- Docs sufficient for “done when”: a product _can_ call these from a branch/tag of this repo.

**Non-Goals:**

- Shipping `reusable-build.yml` / release / Helm publish (#12 / “Next”).
- Opening or merging product-side PRs that flip `uses:` (sync #13 or separate product PR).
- A Devinfra-only smoke caller workflow.
- Multi-arch CI runners or changing the amd64 Dev Container story.
- Checksum-pinning every Actions download (orthogonal hardening).

## Decisions

### 1. Seed from API workflows, not Harvester

- **Choice:** Adapt `m4.2_advanced_middleware_api` reusable CQ/check YAML as the baseline.
- **Why:** Already aligned with `versions.env`, `skip`, Bandit JSON gate, modern checkout/uv/Trivy action pins.
- **Alternative:** Start from Harvester — rejected (older actions, weaker skip/ruleset story).

### 2. Package root input; Python only from versions.env

- **Choice:** `workflow_call` input e.g. `python_package_root` (default `middleware`); optionally mirror for pytest if
  needed as same root. No `python_version` input in MVP.
- **Why:** Matches issue wording and one-pin-source principle; products already ship `versions.env`.
- **Alternative:** Optional version override — deferred unless a caller lacks `versions.env`.

### 3. Check ships with artifact contract; build remains local

- **Choice:** Keep licence / Trivy / CST jobs; document expected artifact names (`docker-image-<component>-<version>`,
  `sbom-<component>-<version>`) and local tag pattern `local/<image_base_name>-<component>:<version>`. Add inputs for
  `components`, `version`, `image_base_name` (replace hard-coded API base), `skip`.
- **Why:** Done-when needs check callable; without shared build, products keep their build reusable until #12.
- **Alternative:** Defer entire check file — rejected (issue lists both workflows).

### 4. Preserve Code Quality job display name

- **Choice:** Job `name: Code Quality Check (3.12)` even without a Python matrix.
- **Why:** API branch ruleset requires that exact check name (D1).
- **Alternative:** Generic name + migrate rulesets — deferred; breaking for consumers.

### 5. CST config path

- **Choice:** Keep `docker/container-structure-tests/<component>.yaml` relative to caller checkout (API layout),
  document it; optional input only if a second layout appears.
- **Why:** All current middleware products share that path convention from shared quality work; avoid premature
  abstraction.

### 6. Docs location and ref guidance

- **Choice:** New `docs/ci.md` + short README pointer. Document
  `uses: fairagro/m4.2_middleware_devinfra/.github/workflows/<file>@<ref>` with `@main` for early adoption and recommend
  tag or commit SHA for stability (E3).
- **Why:** Issue asks for call documentation; no release train yet for required tags.

### 7. Permissions and secrets

- **Choice:** Mirror API: contents read; security-events write on security job for SARIF; callers use `secrets: inherit`
  when needed.
- **Why:** Least surprise for existing product callers.

## Risks / Trade-offs

- **[Risk] Check fails without matching build artifacts** → Mitigation: docs + `skip` path; keep artifact naming
  identical to API build until shared build exists.
- **[Risk] Hard-coded `(3.12)` job name drifts from actual Python pin** → Mitigation: accept cosmetic mismatch; change
  only with coordinated ruleset update.
- **[Risk] Product path filters / pylint targets differ (Harvester)** → Mitigation: package-root input covers
  ruff/mypy/pytest/bandit scope; product-specific pylint packages stay caller-side or follow-up input if needed — MVP
  uses root-wide checks like API (`middleware/`).
- **[Risk] Action pin drift vs products** → Mitigation: pin to API’s current majors; Renovate later (#12 era).

## Migration Plan

1. Land workflows + docs on a Devinfra branch/tag.
2. Product adopts by changing `uses: ./.github/workflows/...` to
   `uses: fairagro/m4.2_middleware_devinfra/.github/workflows/...@<ref>` and passing inputs (`image_base_name`,
   `components`, `python_package_root`).
3. Remove duplicated YAML from products in a sync/#13 follow-up once stable.
4. Rollback: point `uses:` back to local workflow copies.

## Open Questions

None for MVP (explore lock-ins closed A1/B3/C1/D1/E3).
