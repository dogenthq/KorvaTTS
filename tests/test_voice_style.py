import json

import numpy as np
import pytest

from korvatts.voice_style import VoiceStyle

TTL_DIMS = (1, 50, 256)
DP_DIMS = (1, 8, 16)


def _entry(dims, fill, nested):
    arr = np.full(dims, fill, dtype=np.float32)
    return {"data": arr.tolist() if nested else arr.ravel().tolist(), "dims": list(dims)}


def write_style(path, fill=1.0, nested=True, metadata=None):
    data = {
        "style_ttl": _entry(TTL_DIMS, fill, nested),
        "style_dp": _entry(DP_DIMS, fill, nested),
    }
    if metadata is not None:
        data["metadata"] = metadata
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


@pytest.mark.parametrize("nested", [True, False])
def test_from_file_accepts_nested_and_flat_layouts(tmp_path, nested):
    style = VoiceStyle.from_file(write_style(tmp_path / "v1.json", fill=2.0, nested=nested))
    assert style.ttl.shape == TTL_DIMS and style.dp.shape == DP_DIMS
    assert style.ttl.dtype == np.float32
    assert float(style.ttl.mean()) == 2.0
    assert style.name == "v1"


def test_batch_dim_must_be_one(tmp_path):
    path = tmp_path / "b.json"
    data = {
        "style_ttl": _entry((2, 50, 256), 1.0, True),
        "style_dp": _entry((2, 8, 16), 1.0, True),
    }
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError):
        VoiceStyle.from_file(path)


def test_invalid_file_raises(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError):
        VoiceStyle.from_file(bad)


def test_missing_file_raises(tmp_path):
    with pytest.raises(ValueError):
        VoiceStyle.from_file(tmp_path / "nope.json")
