"""Prepare voice style JSON files for publishing.

- Drops private metadata (local file paths, etc.). Only ``style_ttl`` and ``style_dp`` are
  required by the runtime; ``metadata`` keys listed via ``--keep`` are preserved.
- Canonicalises tensor ``data`` to the nested ``[1][rows][cols]`` layout. Upstream Supertonic
  Rust/C++ runtimes parse the nested form only, so a flat list would break byte-compatibility.

Usage:
    python scripts/strip_voice_style_metadata.py assets/voice_styles
    python scripts/strip_voice_style_metadata.py "assets/voice_styles/*.json" --dry-run
"""

from __future__ import annotations

import argparse
import glob
import json
import sys
from pathlib import Path

import numpy as np

REQUIRED_KEYS = ("style_ttl", "style_dp")


def canonical_entry(entry: dict) -> dict:
    """Return ``{"data": nested list, "dims": [...]}`` regardless of the input nesting."""
    dims = [int(d) for d in entry["dims"]]
    arr = np.asarray(entry["data"], dtype=np.float32).reshape(dims)
    return {"data": arr.tolist(), "dims": dims}


def clean_style(data: dict, keep: set[str]) -> dict:
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        raise ValueError(f"missing required keys {missing}")
    cleaned = {k: canonical_entry(data[k]) for k in REQUIRED_KEYS}
    kept_meta = {k: v for k, v in data.get("metadata", {}).items() if k in keep}
    if kept_meta:
        cleaned["metadata"] = kept_meta
    return cleaned


def process_file(path: Path, keep: set[str], dry_run: bool) -> bool:
    """Rewrite ``path`` in canonical form. Returns True if the content changed."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cleaned = clean_style(data, keep)
    changed = cleaned != data
    if changed and not dry_run:
        tmp = path.with_suffix(".json.tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(cleaned, f, separators=(",", ":"))
        tmp.replace(path)  # atomic on the same filesystem
    return changed


def expand_paths(inputs: list[str]) -> list[Path]:
    """Accept files, directories, or glob patterns (shells on Windows do not expand ``*``)."""
    paths: list[Path] = []
    for item in inputs:
        p = Path(item)
        if p.is_dir():
            paths.extend(sorted(p.glob("*.json")))
        elif any(ch in item for ch in "*?["):
            paths.extend(Path(m) for m in sorted(glob.glob(item)))
        else:
            paths.append(p)
    return paths


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("paths", nargs="+", help="Voice style JSON files, directories, or globs")
    parser.add_argument("--keep", nargs="*", default=[], help="metadata keys to keep")
    parser.add_argument("--dry-run", action="store_true", help="Report without writing")
    args = parser.parse_args(argv)

    status = 0
    for path in expand_paths(args.paths):
        try:
            changed = process_file(path, set(args.keep), args.dry_run)
            verb = "would rewrite" if args.dry_run else "rewrote"
            print(f"{verb}: {path}" if changed else f"clean: {path}")
        except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
            print(f"error: {path}: {exc}", file=sys.stderr)
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
