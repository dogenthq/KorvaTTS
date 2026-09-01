"""Tests for the release-hygiene script that canonicalises voice style JSON."""

import importlib.util
import json
import sys
from pathlib import Path

from tests.test_voice_style import TTL_DIMS, write_style

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "strip_voice_style_metadata.py"
_spec = importlib.util.spec_from_file_location("strip_voice_style_metadata", _SCRIPT)
strip = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = strip
_spec.loader.exec_module(strip)


def _nesting_depth(value) -> int:
    depth = 0
    while isinstance(value, list):
        depth += 1
        value = value[0]
    return depth


def test_flat_data_becomes_nested_and_metadata_dropped(tmp_path):
    path = write_style(tmp_path / "v.json", nested=False, metadata={"ref_wav": "/secret/x.mp3", "sr": 44100})
    assert strip.process_file(path, keep={"sr"}, dry_run=False) is True

    out = json.loads(path.read_text(encoding="utf-8"))
    assert set(out) == {"style_ttl", "style_dp", "metadata"}
    assert out["metadata"] == {"sr": 44100}
    assert _nesting_depth(out["style_ttl"]["data"]) == len(TTL_DIMS)
    assert out["style_ttl"]["dims"] == list(TTL_DIMS)


def test_canonical_file_is_reported_clean(tmp_path):
    path = write_style(tmp_path / "v.json", nested=True)
    assert strip.process_file(path, keep=set(), dry_run=True) is False


def test_dry_run_does_not_write(tmp_path):
    path = write_style(tmp_path / "v.json", nested=False)
    before = path.read_text(encoding="utf-8")
    assert strip.process_file(path, keep=set(), dry_run=True) is True
    assert path.read_text(encoding="utf-8") == before


def test_expand_paths_handles_dirs_and_globs(tmp_path):
    write_style(tmp_path / "a.json")
    write_style(tmp_path / "b.json")
    assert [p.name for p in strip.expand_paths([str(tmp_path)])] == ["a.json", "b.json"]
    assert [p.name for p in strip.expand_paths([str(tmp_path / "*.json")])] == ["a.json", "b.json"]
