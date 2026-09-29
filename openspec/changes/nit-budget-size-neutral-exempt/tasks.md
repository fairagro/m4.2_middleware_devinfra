## 1. Specs

- [ ] 1.1 Confirm `ai-review-policy` delta matches lock-in (size-neutral/size-reducing Low always `fix`, no budget;
      Fixed non-nit excludes those; abort still on 0)

## 2. Policy + skill

- [ ] 2.1 Update `docs/ai_review_policy.md` Nit-budget section and Fixed non-nit / cycle-abort wording for the exemption
- [ ] 2.2 Update `.agents/skills/review-fixer/SKILL.md` nit-budget paragraph and step-6 checklist accordingly

## 3. Verify

- [ ] 3.1 Run Prettier on the change tree and `openspec validate nit-budget-size-neutral-exempt --strict`
