## ADDED Requirements

### Requirement: Kubeconform pinned in the shared Dev Container image

The shared product Dev Container image MUST install **kubeconform** at the version pinned by `KUBECONFORM_VERSION` in
`versions.env` (Compose build-arg / Dockerfile `ARG`, same pattern as gitleaks and actionlint). The binary MUST be on
`PATH` after rebuild so local and consumer CI scripts can use the shared runner without a separate host install.
Documentation (`docs/devcontainer.md` and/or `docs/quality.md`) MUST name kubeconform among shared CLI tools.

#### Scenario: kubeconform available after rebuild

- **WHEN** a contributor rebuilds the Dev Container from this repo’s compose/Dockerfile
- **THEN** `kubeconform` is on `PATH` at `KUBECONFORM_VERSION`
- **AND** Dev Container docs list kubeconform with the other shared lint CLIs
