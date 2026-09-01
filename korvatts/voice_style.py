"""Voice style embeddings (speaker identity) loaded from JSON files.

A voice style file holds two precomputed tensors, each as ``{"data": [...], "dims": [1, R, C]}``:
- ``style_ttl``: (1, 50, 256) style tokens consumed by the text encoder and vector estimator.
- ``style_dp``:  (1, 8, 16)  style tokens consumed by the duration predictor.

``data`` may be nested ``[1][R][C]`` (the canonical Supertonic layout) or flat; both are accepted
here, but only the nested form is written by the release tooling because upstream Rust/C++
runtimes require it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass
class VoiceStyle:
    """Single-speaker style tensors with a leading batch axis of size 1."""

    ttl: np.ndarray
    dp: np.ndarray
    name: str

    @classmethod
    def from_file(cls, path: str | Path) -> VoiceStyle:
        path = Path(path)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            ttl = tensor_from_entry(data["style_ttl"])
            dp = tensor_from_entry(data["style_dp"])
        except (OSError, KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
            raise ValueError(f"Invalid voice style file: {path}") from exc
        if ttl.shape[0] != 1 or dp.shape[0] != 1:
            raise ValueError(f"Voice style batch dim must be 1: {path}")
        return cls(ttl=ttl, dp=dp, name=path.stem)


def tensor_from_entry(entry: dict) -> np.ndarray:
    """Return a float32 array shaped by ``entry['dims']`` from nested or flat ``data``."""
    dims = [int(d) for d in entry["dims"]]
    arr = np.asarray(entry["data"], dtype=np.float32).reshape(dims)
    return arr
