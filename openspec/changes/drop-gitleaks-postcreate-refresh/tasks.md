## 1. Script

- [ ] 1.1 Remove the gitleaks `install-pinned-tool.sh` block from `scripts/devcontainer-post-create.sh` — verify the
      script no longer mentions `gitleaks` or `install-pinned-tool`

## 2. Docs

- [ ] 2.1 Update `docs/devcontainer.md` / `docs/quality.md`: drop legacy postCreate gitleaks refresh wording; state
      image rebuild for gitleaks like other CLI hooks — verify no “soft-refresh gitleaks” / “legacy exception” remains

## 3. Validate

- [ ] 3.1 Run `openspec validate drop-gitleaks-postcreate-refresh --strict` and Prettier on touched Markdown — verify
      clean
- [ ] 3.2 Confirm `gitleaks version` works in this Dev Container (image pin) without re-running the removed refresh —
      verify binary still on PATH after the script change (image already has it)
