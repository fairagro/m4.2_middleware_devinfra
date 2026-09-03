# Project principles (Devinfra)

This repository extends the shared foundation in [`principles.global.md`](principles.global.md). Read that file first
for Values, Supported development environment, Type Safety, Configuration, Code Quality, Testing, Security, Spec/Code
naming, and Branch strategy.

Do **not** redefine or weaken Supported development environment or Type Safety here — those sections are owned by
`principles.global.md`.

## Devinfra-only notes

- This repo has **no** product `middleware/` packages. Quality gates that target `middleware/` apply in product
  consumers, not as runtime packages here.
- Shared docs and agent extracts live under `docs/`, `.agents/`, `.cursor/`, and `.github/` as described in the root
  README.
