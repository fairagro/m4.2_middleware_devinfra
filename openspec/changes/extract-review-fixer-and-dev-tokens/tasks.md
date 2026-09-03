# Extract review-fixer and personal-token helpers — Tasks

## 1. Token helpers (#8)

- [ ] 1.1 Add `scripts/dev-tokens.sh`: `/commandhistory` or `~/.config/$PRODUCT_SLUG/` (fail if host path needed and
      slug missing); empty-skip; TTY prompts for `GH_TOKEN` and `GITGUARDIAN_API_KEY`; safe non-TTY load of stored
      values only
- [ ] 1.2 Add `scripts/set-dev-tokens.sh` (`DEV_TOKENS_FORCE=1`)

## 2. Wrappers (#8)

- [ ] 2.1 Add `scripts/bin/gh` (source tokens, require token, exec real `gh`)
- [ ] 2.2 Add `scripts/cursor-git.sh` and `scripts/bin/git` (strip null `core.hooksPath`, source tokens, exec real
      `git`)
- [ ] 2.3 Ensure wrapper scripts are executable

## 3. Dev Container and token docs (#8)

- [ ] 3.1 `remoteEnv.PATH` → `scripts/bin` first; set `PRODUCT_SLUG=middleware-devinfra`; wire postCreate and/or shell
      profile to non-prompting source of `dev-tokens.sh` (Kombi)
- [ ] 3.2 Document empty-skip, `set-dev-tokens.sh`, Kombi (shell load + wrappers), and `PRODUCT_SLUG` in README / Dev
      Container doc; link conventions token paths

## 4. Review-fixer (#5)

- [ ] 4.1 Add `.agents/skills/review-fixer/SKILL.md` from API: Variante A GraphQL; Auth → shared `gh` + conventions;
      cite `principles.global.md`; inline follow-up Markdown (no create-issue dependency)
- [ ] 4.2 Add `.cursor/commands/review-fixer.md` and `.github/prompts/review-fixer.prompt.md` pointing at the skill and
      `docs/ai_review_policy.md`
- [ ] 4.3 Index review-fixer in root README among synced agent paths

## 5. Verify

- [ ] 5.1 Sanity-check: `PRODUCT_SLUG` set in Dev Container; wrappers find real `gh`/`git`; no worktree tokens; skill
      content matches policy / decisions
- [ ] 5.2 Run `npm run format:md` and `npm run lint:md`; fix remaining findings by hand
