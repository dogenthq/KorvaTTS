"""Locate model assets: explicit path -> env var -> ./assets -> HuggingFace download.

Expected layout inside the assets directory::

    assets/
    ├── onnx/
    │   ├── duration_predictor.onnx
    │   ├── text_encoder.onnx
    │   ├── vector_estimator.onnx
    │   ├── vocoder.onnx
    │   ├── tts.json
    │   └── unicode_indexer.json
    └── voice_styles/
        └── <voice_name>.json
"""

from __future__ import annotations

import os
from pathlib import Path

ENV_ASSETS_DIR = "KORVATTS_ASSETS_DIR"
ENV_HF_REPO = "KORVATTS_HF_REPO"
DEFAULT_HF_REPO = "dogenthq/KorvaTTS"

ONNX_FILES = [
    "duration_predictor.onnx",
    "text_encoder.onnx",
    "vector_estimator.onnx",
    "vocoder.onnx",
    "tts.json",
    "unicode_indexer.json",
]


def is_valid_assets_dir(path: Path) -> bool:
    onnx_dir = path / "onnx"
    return all((onnx_dir / name).is_file() for name in ONNX_FILES)


def resolve_assets_dir(assets_dir: str | Path | None = None, auto_download: bool = True) -> Path:
    """Return a directory containing ``onnx/`` and ``voice_styles/``.

    Resolution order: ``assets_dir`` argument, ``$KORVATTS_ASSETS_DIR``, ``./assets``,
    then (if ``auto_download``) a HuggingFace snapshot of ``$KORVATTS_HF_REPO``.
    An explicitly given location (argument or env var) must be valid; it never falls through.
    """
    explicit = assets_dir if assets_dir is not None else os.environ.get(ENV_ASSETS_DIR) or None
    if explicit is not None:
        path = Path(explicit).resolve()
        if not is_valid_assets_dir(path):
            raise FileNotFoundError(f"Assets dir '{path}' is missing required ONNX files")
        return path

    local = (Path.cwd() / "assets").resolve()
    if is_valid_assets_dir(local):
        return local
    if not auto_download:
        raise FileNotFoundError(
            "No local assets found. Pass assets_dir=..., set "
            f"${ENV_ASSETS_DIR}, or enable auto_download."
        )
    return download_assets()


def download_assets(repo_id: str | None = None) -> Path:
    """Download (or reuse cached) assets from HuggingFace Hub and return the local path."""
    from huggingface_hub import snapshot_download

    repo_id = repo_id or os.environ.get(ENV_HF_REPO, DEFAULT_HF_REPO)
    try:
        local = Path(snapshot_download(repo_id=repo_id, allow_patterns=["onnx/*", "voice_styles/*"]))
    except Exception as exc:  # hub raises a mix of HTTP/OS errors; surface one clear message
        raise RuntimeError(f"Failed to download assets from Hugging Face repo '{repo_id}': {exc}") from exc
    if not is_valid_assets_dir(local):
        raise FileNotFoundError(f"Downloaded repo '{repo_id}' does not contain the expected files")
    return local


def list_voices(assets_dir: Path) -> list[str]:
    """Names of bundled voice styles (file stems under ``voice_styles/``)."""
    styles_dir = assets_dir / "voice_styles"
    if not styles_dir.is_dir():
        return []
    return sorted(p.stem for p in styles_dir.glob("*.json"))
