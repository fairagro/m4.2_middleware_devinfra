## 1. Pin and install gitleaks

- [ ] 1.1 Add `GITLEAKS_VERSION` to `versions.env` (current stable release) and a Renovate regex custom manager + CLI
      group membership; verify `renovate.json` validates / dry extract lists the pin
- [ ] 1.2 Add `scripts/install-gitleaks.sh` (CST-like) and wire Dev Container post-create; verify `gitleaks version`
      matches the pin after install
- [ ] 1.3 Add `scripts/install-gitleaks.sh` to `docs/synced-paths.yaml` allowlist; verify sync inventory lists it

## 2. Replace commit-stage ggshield

- [ ] 2.1 Swap `.pre-commit-config.yaml` ggshield hook for gitleaks (no API key); verify
      `pre-commit run gitleaks --all-files` (or hook id) exits 0 on a clean tree
- [ ] 2.2 Remove ggshield from `scripts/quality-tools-pins.txt` and `pyproject.toml`; refresh lock; verify `rg ggshield`
      is gone from those pin surfaces
- [ ] 2.3 Add `.gitleaksignore` (or config) if needed and document allowlist in `docs/quality.md`; verify docs no longer
      require `GITGUARDIAN_API_KEY` for the secret-scan gate

## 3. CI gate

- [ ] 3.1 Install + run gitleaks in `.github/workflows/reusable-code-quality.yml` when `skip` is false (fail closed);
      verify workflow YAML references install helper / pin and fails conceptually on findings (comment or dry logic
      review)
- [ ] 3.2 Update `docs/ci.md` (and sync notes) for the new secret-scan step; verify docs mention gitleaks not ggshield
      for code-quality

## 4. Docs and anti-duplication surfaces

- [ ] 4.1 Update `docs/devcontainer.md`, `docs/code-review.md`, `.agents/skills/code-review/SKILL.md`, and token helper
      docs/prompts to drop ggshield / GitGuardian happy-path; verify `rg ggshield` / `GITGUARDIAN` only remain in
      archive or intentional historical notes
- [ ] 4.2 Add a short product migration blurb (sync → drop ggshield → no GG key) in `docs/quality.md` or `docs/sync.md`;
      verify infra follow-up #74 can point at it

## 5. Validate

- [ ] 5.1 Run `openspec validate replace-ggshield-with-gitleaks --strict` and Prettier/markdownlint on touched docs;
      verify both pass
