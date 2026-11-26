"""Regression: run-helm-lint.sh HELM_VALUES_FILE auto-default (#419)."""

from __future__ import annotations

import os
import shutil
import stat
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = REPO_ROOT / "scripts" / "run-helm-lint.sh"


def _write_fake_helm(bin_dir: Path, log_path: Path) -> None:
    helm = bin_dir / "helm"
    helm.write_text(
        f"""#!/usr/bin/env bash
set -euo pipefail
printf '%s\\n' "$*" >> {str(log_path)!r}
case "${{1:-}}" in
  version) echo "v0.0.0-test" ;;
  lint|template) ;;
  *) echo "unexpected helm args: $*" >&2; exit 1 ;;
esac
""",
        encoding="utf-8",
    )
    helm.chmod(helm.stat().st_mode | stat.S_IEXEC)


def _fixture_repo(tmp_path: Path, *, with_overrides: bool) -> Path:
    repo = tmp_path / "repo"
    (repo / "scripts").mkdir(parents=True)
    (repo / "charts" / "demo").mkdir(parents=True)
    shutil.copy2(SCRIPT, repo / "scripts" / "run-helm-lint.sh")
    (repo / "charts" / "demo" / "Chart.yaml").write_text(
        "apiVersion: v2\nname: demo\nversion: 0.1.0\n",
        encoding="utf-8",
    )
    if with_overrides:
        (repo / "ci").mkdir(parents=True)
        (repo / "ci" / "helm-ci-overrides.yaml").write_text(
            "tls:\n  enabled: false\n",
            encoding="utf-8",
        )
    return repo


def _run(
    repo: Path,
    bin_dir: Path,
    *,
    env_extra: dict[str, str] | None = None,
    unset_values: bool = True,
) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, "PATH": f"{bin_dir}:{os.environ.get('PATH', '')}"}
    if unset_values:
        env.pop("HELM_VALUES_FILE", None)
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        ["bash", str(repo / "scripts" / "run-helm-lint.sh")],
        cwd=repo,
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def test_auto_applies_ci_overrides_when_unset(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path, with_overrides=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "helm.log"
    _write_fake_helm(bin_dir, log)

    proc = _run(repo, bin_dir)
    assert proc.returncode == 0, proc.stderr
    assert "values overlay ci/helm-ci-overrides.yaml" in proc.stderr
    lines = log.read_text(encoding="utf-8").splitlines()
    assert any(line.startswith("lint ./charts/demo -f ci/helm-ci-overrides.yaml") for line in lines)
    assert any(line.startswith("template ci-smoke ./charts/demo -f ci/helm-ci-overrides.yaml") for line in lines)


def test_bare_chart_when_overrides_absent(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path, with_overrides=False)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "helm.log"
    _write_fake_helm(bin_dir, log)

    proc = _run(repo, bin_dir)
    assert proc.returncode == 0, proc.stderr
    assert "values overlay" not in proc.stderr
    lines = log.read_text(encoding="utf-8").splitlines()
    assert "lint ./charts/demo" in lines
    assert "template ci-smoke ./charts/demo" in lines


def test_explicit_helm_values_file_wins(tmp_path: Path) -> None:
    repo = _fixture_repo(tmp_path, with_overrides=True)
    custom = repo / "custom-values.yaml"
    custom.write_text("replicaCount: 1\n", encoding="utf-8")
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "helm.log"
    _write_fake_helm(bin_dir, log)

    proc = _run(
        repo,
        bin_dir,
        env_extra={"HELM_VALUES_FILE": "custom-values.yaml"},
        unset_values=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "values overlay custom-values.yaml" in proc.stderr
    assert "ci/helm-ci-overrides.yaml" not in proc.stderr
    lines = log.read_text(encoding="utf-8").splitlines()
    assert any(line.startswith("lint ./charts/demo -f custom-values.yaml") for line in lines)


def test_empty_helm_values_file_forces_bare(tmp_path: Path) -> None:
    """Explicit empty export must not auto-apply the CI overlay."""
    repo = _fixture_repo(tmp_path, with_overrides=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    log = tmp_path / "helm.log"
    _write_fake_helm(bin_dir, log)

    proc = _run(
        repo,
        bin_dir,
        env_extra={"HELM_VALUES_FILE": ""},
        unset_values=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert "values overlay" not in proc.stderr
    lines = log.read_text(encoding="utf-8").splitlines()
    assert "lint ./charts/demo" in lines
