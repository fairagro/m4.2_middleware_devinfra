# Add canonical arctrl agent skill

## Why

Product repos each ship `.agents/skills/arctrl/SKILL.md` at different fidelity; harvester has the fullest arctrl ≥ 3.2.1
reference. Devinfra has no canonical copy, so sync (#13) cannot converge products on one skill.

## What Changes

- Add first-party `.agents/skills/arctrl/SKILL.md` equal to (or superseding) the harvester full feature set for arctrl ≥
  3.2.1
- Document the skill in the root README (intro / layout) as a shared first-party skill — not a vendor `gh skill` pin
- Keep it out of vendor lint-exclude trees (`gh` / `docker` / `hadolint` / `uv`); format and lint like other shared
  skills
- Out of scope: flipping callers in product repos (sync #13); Cursor command / Copilot prompt entrypoints (reference
  skill only)

## Capabilities

### New Capabilities

- `shared-arctrl-skill`: Canonical first-party arctrl agent skill under `.agents/skills/arctrl/`, README discovery, and
  first-party (not vendor-exclude) treatment

### Modified Capabilities

- (none — vendor exclude lists stay unchanged; arctrl is simply not added to them)

## Impact

- New path `.agents/skills/arctrl/` (sync consumers of this tree later via #13)
- README layout / skills section
- Markdown format/lint will cover the new skill (may need Prettier/markdownlint passes on import)
