## 1. Runner, hook, CI

- [x] 1.1 Add `scripts/run-uv-audit.sh` (`uv audit --frozen`, optional `.uv-audit-ignore` → `--ignore`, fail on
      findings)
- [x] 1.2 Add commit-stage pre-commit hook calling the runner; document `SKIP` / network need in `docs/quality.md`
- [x] 1.3 Add matching step in `reusable-code-quality.yml` after `uv sync`; set `UV_MALWARE_CHECK=1` on the sync step

## 2. Malware check + sync paths + docs

- [x] 2.1 Enable `UV_MALWARE_CHECK=1` for `uv sync` in `scripts/devcontainer-post-create.sh`
- [x] 2.2 List `.uv-audit-ignore` under `docs/synced-paths.yaml` `overlays`; note in `docs/sync.md`
- [x] 2.3 Document uv audit vs Trivy vs malware check in `docs/quality.md` / `docs/ci.md` (+ principles Code Quality
      example if needed); parity table IDE exception for uv audit

## 3. Validate

- [x] 3.1 Run runner locally on Devinfra lockfile (expect clean or only ignored)
- [x] 3.2 `openspec validate fleet-uv-audit-lockfile --strict`
