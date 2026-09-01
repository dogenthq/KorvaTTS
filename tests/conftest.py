"""Shared fixtures. Asset-dependent tests are skipped when no local assets exist."""

from pathlib import Path

import pytest

from korvatts.assets import is_valid_assets_dir

REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = REPO_ROOT / "assets"


@pytest.fixture(scope="session")
def assets_dir() -> Path:
    if not is_valid_assets_dir(ASSETS_DIR):
        pytest.skip("local assets/ directory not found; skipping model-dependent tests")
    return ASSETS_DIR


@pytest.fixture(scope="session")
def indexer_path(assets_dir: Path) -> Path:
    return assets_dir / "onnx" / "unicode_indexer.json"
