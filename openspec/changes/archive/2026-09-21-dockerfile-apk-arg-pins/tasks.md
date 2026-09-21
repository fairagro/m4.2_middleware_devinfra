## 1. Script

- [x] 1.1 Rewrite apk update path in `scripts/update-dockerfile-pins.sh` for ARG `*_VERSION=*-rN` defaults (map name →
      package; bump from APKINDEX) and verify with a temp Dockerfile fixture that ARG bumps
- [x] 1.2 Fail loud on inline `pkg=…-rN` apk literals and on ARG packages missing from APKINDEX; verify non-zero exit
- [x] 1.3 Keep pip `name==` updates; update script header comments for style B

## 2. Docs

- [x] 2.1 Document style B + updater behaviour in `docs/renovate.md` (Manual Dockerfile pins) and verify `docs/ci.md`
      pointer still accurate
- [x] 2.2 Run `openspec validate dockerfile-apk-arg-pins --strict` and confirm pass
