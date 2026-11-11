"""Unit tests for profile-based synced-paths loading in sync-products."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync-products.py"


def _load_sync_module():

    spec = importlib.util.spec_from_file_location("sync_products", SYNC_SCRIPT)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    # dataclasses needs the module registered before class bodies run
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def sync():
    return _load_sync_module()


def test_load_repo_yaml_has_foundation_and_infra(sync) -> None:
    config = sync.load_sync_config(REPO_ROOT / "docs" / "synced-paths.yaml")
    assert "foundation" in config.profiles
    assert "python-product" in config.profiles
    assert "gitops" in config.profiles
    assert "infrastructure" in config.targets
    assert config.targets["infrastructure"][0] == "fairagro/m4.2_infrastructure"
    assert config.targets["infrastructure"][1] == ("foundation", "gitops", "infra-consumer")
    assert config.targets["api"][1] == ("foundation", "python-product", "gitops")
    assert "infra-consumer" in config.profiles


def test_foundation_excludes_renovate_and_devcontainer(sync) -> None:
    config = sync.load_sync_config(REPO_ROOT / "docs" / "synced-paths.yaml")
    foundation = set(sync.effective_allow(config, ("foundation",)))
    assert "scripts/ai/**" in foundation
    assert ".agents/skills/uv/**" in foundation
    assert "scripts/bin/m42-ai" in foundation
    assert "scripts/install-gitleaks.sh" in foundation
    assert "scripts/install-actionlint.sh" in foundation
    assert ".pre-commit-config.infrastructure.yaml" not in foundation
    assert "renovate.json" not in foundation
    assert "versions.env" not in foundation
    assert ".devcontainer/Dockerfile" not in foundation
    assert ".pre-commit-config.yaml" not in foundation


def test_product_union_includes_shared_surfaces(sync) -> None:
    config = sync.load_sync_config(REPO_ROOT / "docs" / "synced-paths.yaml")
    union = set(sync.effective_allow(config, sync.product_union_profiles(config)))
    assert "renovate.json" in union
    assert ".devcontainer/Dockerfile" in union
    assert "scripts/ai/**" in union
    assert ".pre-commit-config.yaml" in union
    assert "scripts/run-helm-lint.sh" in union
    assert ".pre-commit-config.infrastructure.yaml" not in union


def test_infra_allow_omits_product_pre_commit_root(sync) -> None:
    config = sync.load_sync_config(REPO_ROOT / "docs" / "synced-paths.yaml")
    infra = set(sync.effective_allow(config, config.targets["infrastructure"][1]))
    assert ".pre-commit-config.infrastructure.yaml" in infra
    assert ".pre-commit-config.yaml" not in infra
    assert "scripts/run-helm-lint.sh" in infra
    assert "ruff.toml" not in infra
    # #352: product Dev Container never on Infra profiles
    assert ".devcontainer/Dockerfile" not in infra
    assert ".devcontainer/devcontainer.json" not in infra
    assert not any(p.startswith(".devcontainer/") for p in infra)
    for profile in ("foundation", "gitops", "infra-consumer"):
        allow = set(sync.effective_allow(config, (profile,)))
        assert not any(p.startswith(".devcontainer/") for p in allow)


def test_legacy_flat_allow_still_loads(sync) -> None:
    text = """
allow:
  - scripts/ai/**
exclude:
  - middleware/**
overlays: []
"""
    config = sync.load_sync_config_text(text, source="test-legacy")
    assert sync._LEGACY_PROFILE in config.profiles
    assert set(config.targets) == {"api", "sql_to_arc", "harvester"}
    patterns, excludes = sync.load_allow_exclude_text(text, source="test-legacy")
    assert patterns == ["scripts/ai/**"]
    assert "middleware/**" in excludes


def test_profiles_reject_top_level_allow(sync) -> None:
    text = """
profiles:
  foundation:
    allow: [a]
targets:
  infrastructure:
    repo: fairagro/m4.2_infrastructure
    profiles: [foundation]
allow:
  - b
exclude: []
overlays: []
"""
    with pytest.raises(SystemExit, match="top-level `allow`"):
        sync.load_sync_config_text(text, source="test-dup")


def test_resolve_head_infra_smaller_than_product_union(sync) -> None:
    config = sync.load_sync_config(REPO_ROOT / "docs" / "synced-paths.yaml")
    product = sync.resolve_files(
        sync.effective_allow(config, sync.product_union_profiles(config)),
        REPO_ROOT,
        config.excludes,
    )
    infra = sync.resolve_files(
        sync.effective_allow(config, config.targets["infrastructure"][1]),
        REPO_ROOT,
        config.excludes,
    )
    assert infra
    assert len(infra) < len(product)
    infra_set = {p.as_posix() for p in infra}
    product_set = {p.as_posix() for p in product}
    # Infra-only pre-commit root is not on the product union.
    assert ".pre-commit-config.infrastructure.yaml" in infra_set
    assert ".pre-commit-config.infrastructure.yaml" not in product_set
    assert infra_set - {".pre-commit-config.infrastructure.yaml"} <= product_set
    assert not any(p.startswith(".devcontainer/") for p in infra_set)
    assert any("scripts/ai/" in p or p.startswith("scripts/ai/") for p in infra_set)


def test_missing_target_at_legacy_ref_is_empty(sync, monkeypatch: pytest.MonkeyPatch) -> None:
    """Pre-profile YAML has no infrastructure key — orphan base must not abort."""
    legacy = """
allow:
  - scripts/ai/**
exclude: []
overlays: []
"""
    monkeypatch.setattr(sync, "git_show_text", lambda *_a, **_k: legacy)
    monkeypatch.setattr(sync, "git_ls_tree_files", lambda *_a, **_k: ["scripts/ai/x.py"])
    assert sync.resolve_files_at_ref("fake-legacy", target="infrastructure") == []
    api_files = sync.resolve_files_at_ref("fake-legacy", target="api")
    assert [p.as_posix() for p in api_files] == ["scripts/ai/x.py"]
    orphans = sync.orphan_paths(
        sync.resolve_files_at_ref("fake-legacy", target="infrastructure"),
        [Path("scripts/ai/x.py")],
    )
    assert orphans == []
