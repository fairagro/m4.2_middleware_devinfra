## ADDED Requirements

### Requirement: Product Dockerfile apk pins use ARG defaults

Product-local Dockerfiles that pin Alpine `apk` packages (typically last-stage / component Dockerfiles under
`docker/Dockerfile.*`, excluding `docker/Dockerfile.product-app.base`) MUST declare each pin as a Dockerfile `ARG`
default whose value is an Alpine package version (`X.Y.Z-rN`), and MUST reference that ARG in `apk add` (e.g.
`"pkg=${PKG_VERSION}"`). They MUST NOT embed Alpine-style inline literals `pkg=X.Y.Z-rN` as the pin source of truth.

The repository MUST provide `scripts/update-dockerfile-pins.sh` that, for each candidate Dockerfile:

1. Detects `ARG <NAME>_VERSION=<apk-ver>` defaults whose value matches Alpine `*-rN` form
2. Maps `<NAME>_VERSION` to apk package `<name>` by stripping `_VERSION`, lower-casing, and replacing `_` with `-`
3. Refreshes those ARG defaults from Alpine APKINDEX (main + community) for the detected Alpine minor
4. Continues to refresh inline pip-style `name==` pins from PyPI when present
5. Exits non-zero (fail loud) when an ARG apk pin’s package is missing from APKINDEX, or when forbidden inline
   `pkg=…-rN` apk literals are present in the file

The script MUST NOT write `*.bak` sidecars. Documentation (`docs/renovate.md` and the script header) MUST state style B
as the fleet convention.

#### Scenario: ARG apk pin is refreshed from APKINDEX

- **WHEN** a product Dockerfile contains `ARG CA_CERTIFICATES_VERSION=20260611-r0` and APKINDEX has a newer
  `ca-certificates` version
- **THEN** running `scripts/update-dockerfile-pins.sh` on that file updates the ARG default to the newer version

#### Scenario: Inline apk version literals fail the updater

- **WHEN** a product Dockerfile contains an Alpine-style inline pin `ca-certificates=20260611-r0`
- **THEN** the updater exits non-zero and reports that inline apk version literals are not supported

#### Scenario: Unknown ARG apk package fails loud

- **WHEN** a Dockerfile declares `ARG SOME_OBSCURE_VERSION=1.0.0-r0` mapping to a package absent from APKINDEX
- **THEN** the updater exits non-zero after reporting the miss (it does not print a successful Done for that file)
