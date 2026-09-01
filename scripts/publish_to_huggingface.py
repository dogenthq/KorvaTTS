"""Upload model assets and the model card to the Hugging Face Hub.

Usage:
    huggingface-cli login            # once
    python scripts/publish_to_huggingface.py [--repo dogenthq/KorvaTTS] [--dry-run]

Uploads from ./assets: onnx/, voice_styles/, raw_voices/, samples/ and the model card at
model_card/README.md. Run scripts/strip_voice_style_metadata.py and
scripts/generate_voice_samples.py first.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ASSETS_DIR = REPO_ROOT / "assets"
MODEL_CARD = REPO_ROOT / "model_card" / "README.md"
ALLOW_PATTERNS = ["onnx/*", "voice_styles/*.json", "raw_voices/*.wav", "samples/*.wav"]


def preflight() -> list[str]:
    problems = []
    for sub in ("onnx", "voice_styles", "raw_voices", "samples"):
        if not (ASSETS_DIR / sub).is_dir():
            problems.append(f"missing directory: assets/{sub}")
    if not MODEL_CARD.is_file():
        problems.append(f"missing model card: {MODEL_CARD.relative_to(REPO_ROOT)}")
    styles = {p.stem for p in (ASSETS_DIR / "voice_styles").glob("*.json")}
    for sub in ("raw_voices", "samples"):
        wavs = {p.stem for p in (ASSETS_DIR / sub).glob("*.wav")}
        if styles != wavs:
            problems.append(f"voice_styles/{sub} mismatch: {sorted(styles ^ wavs)}")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="dogenthq/KorvaTTS")
    parser.add_argument("--message", default="Upload KorvaTTS assets")
    parser.add_argument("--dry-run", action="store_true", help="Validate only, upload nothing")
    args = parser.parse_args(argv)

    problems = preflight()
    if problems:
        print("preflight failed:\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    print(f"assets OK; target repo: {args.repo}")
    if args.dry_run:
        return 0

    from huggingface_hub import HfApi

    api = HfApi()
    api.create_repo(args.repo, repo_type="model", exist_ok=True)
    api.upload_file(
        path_or_fileobj=str(MODEL_CARD), path_in_repo="README.md", repo_id=args.repo,
        commit_message=f"{args.message} (model card)",
    )
    api.upload_folder(
        folder_path=str(ASSETS_DIR), repo_id=args.repo, allow_patterns=ALLOW_PATTERNS,
        commit_message=args.message,
    )
    print(f"done: https://huggingface.co/{args.repo}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
