## 1. Documentation

- [ ] 1.1 Add a `docs/ci.md` section (near Feature PR / Release) with the thin post-merge main Docker check caller:
      `on.push.branches: [main]`, concurrency, `permissions.security-events: write`, jobs `build` → `check` only using
      existing reusables; verify the snippet has no code-quality or release/publish jobs
- [ ] 1.2 Document why (Default-Branch Code Scanning alert close), that Release keeps its own check gate / does not
      consume this SARIF, and that path-filters are optional later; verify those sentences appear in the section

## 2. Verification

- [ ] 2.1 Run `openspec validate post-merge-trivy-main-sarif --strict` and confirm it passes; run `npm run format:md`
      and `npm run lint:md` for the edited docs
