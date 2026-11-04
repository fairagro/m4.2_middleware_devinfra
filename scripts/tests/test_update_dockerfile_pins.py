"""Unit tests for update-dockerfile-pins.sh ARG→apk resolution (#333)."""

from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "update-dockerfile-pins.sh"


def _bash_resolve(dockerfile: Path, arg_name: str, *, index_pkgs: dict[str, str]) -> tuple[int, str]:
    """Source the script with a mocked APKINDEX and print resolve_apk_pkg result."""
    pkg_assignments = "\n".join(
        f'PKG_VERSIONS[{pkg!r}]="{ver}"$\'\\n\'' for pkg, ver in index_pkgs.items()
    )
    script = textwrap.dedent(
        f"""\
        set -euo pipefail
        # shellcheck source=/dev/null
        source {SCRIPT.as_posix()!r}
        {pkg_assignments}
        set +e
        out="$(resolve_apk_pkg {dockerfile.as_posix()!r} {arg_name!r})"
        code=$?
        set -e
        printf '%s\\n' "$out"
        exit "$code"
        """
    )
    result = subprocess.run(
        ["bash", "-c", script],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout.strip()


def test_resolve_libstdcxx_from_dockerfile_usage(tmp_path: Path) -> None:
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text(
        textwrap.dedent(
            """\
            FROM alpine:3.24
            ARG LIBSTDCXX_VERSION=14.2.0-r4
            RUN apk add --no-cache "libstdc++=${LIBSTDCXX_VERSION}"
            """
        ),
        encoding="utf-8",
    )
    code, pkg = _bash_resolve(
        dockerfile,
        "LIBSTDCXX_VERSION",
        index_pkgs={"libstdc++": "15.2.0-r5"},
    )
    assert code == 0
    assert pkg == "libstdc++"


def test_resolve_libstdcxx_from_override_without_usage(tmp_path: Path) -> None:
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text(
        "FROM alpine:3.24\nARG LIBSTDCXX_VERSION=14.2.0-r4\n",
        encoding="utf-8",
    )
    code, pkg = _bash_resolve(
        dockerfile,
        "LIBSTDCXX_VERSION",
        index_pkgs={"libstdc++": "15.2.0-r5"},
    )
    assert code == 0
    assert pkg == "libstdc++"


def test_resolve_derived_name_when_in_index(tmp_path: Path) -> None:
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text(
        textwrap.dedent(
            """\
            FROM alpine:3.24
            ARG CA_CERTIFICATES_VERSION=20241121-r1
            RUN apk add --no-cache "ca-certificates=${CA_CERTIFICATES_VERSION}"
            """
        ),
        encoding="utf-8",
    )
    code, pkg = _bash_resolve(
        dockerfile,
        "CA_CERTIFICATES_VERSION",
        index_pkgs={"ca-certificates": "20261020-r0"},
    )
    assert code == 0
    assert pkg == "ca-certificates"


def test_resolve_fails_when_derived_wrong_and_no_fallback(tmp_path: Path) -> None:
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text(
        "FROM alpine:3.24\nARG LIBSTDCXX_VERSION=14.2.0-r4\n",
        encoding="utf-8",
    )
    code, pkg = _bash_resolve(
        dockerfile,
        "LIBSTDCXX_VERSION",
        index_pkgs={"ca-certificates": "20261020-r0"},
    )
    assert code != 0
    assert pkg == "libstdc++"  # override name reported even when missing from index
