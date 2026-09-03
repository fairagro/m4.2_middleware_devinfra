# Extract AI review policy and global principles — Tasks

## 1. Global principles

- [ ] 1.1 Add `openspec/principles.global.md` from the API principles (shared sections only per design.md decision 4)
- [ ] 1.2 Add thin Devinfra `openspec/principles.md` that points at `openspec/principles.global.md`

## 2. AI review policy and Finder entries

- [ ] 2.1 Add `docs/ai_review_policy.md` from the API policy; strip product-only examples; cite
      `openspec/principles.global.md` directly for Supported environment and Type Safety
- [ ] 2.2 Add `.cursor/BUGBOT.md` pointing at `docs/ai_review_policy.md` (Finder; `.cursor/rules/` do not apply)
- [ ] 2.3 Add `.github/copilot-instructions.md` as shared Finder entry → policy (optional direct cite of
      `principles.global.md`; no product `AGENTS.md` requirement)

## 3. README

- [ ] 3.1 Index `docs/ai_review_policy.md` and document `principles.global.md` (shared) vs `principles.md` (local
      extension); reinforce that consumers must not diverge on synced AI review / global principles paths

## 4. Verify

- [ ] 4.1 Human review once: policy + both Finder entries + principles split match issue #4 done-when and design
      decisions
- [ ] 4.2 Run `npm run format:md` and `npm run lint:md`; fix any remaining markdownlint findings by hand
