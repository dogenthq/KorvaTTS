"""Synthesize one demo clip per bundled voice for the Hugging Face model card.

Usage:
    python scripts/generate_voice_samples.py [--assets-dir assets] [--out assets/samples]
                                             [--steps 32] [--seed 0] [--only stem ...]

Output: ``<out>/<voice>.wav`` (44.1 kHz mono), one distinct sentence per voice
(see scripts/voice_catalog.py).
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from voice_catalog import VOICES

from korvatts import TTS


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--assets-dir", default="assets")
    parser.add_argument("--out", default="assets/samples")
    parser.add_argument("--steps", type=int, default=32)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--only", nargs="*", default=None, help="Voice stems to (re)generate")
    args = parser.parse_args(argv)

    tts = TTS(assets_dir=args.assets_dir, device="cpu", auto_download=False)
    available = set(tts.list_voices())
    selected = [v for v in VOICES if not args.only or v.stem in args.only]
    missing = [v.stem for v in selected if v.stem not in available]
    if missing:
        print(f"error: voices in catalog but not in assets: {missing}", file=sys.stderr)
        return 1

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    for v in selected:
        start = time.perf_counter()
        wav, duration = tts.synthesize(
            v.sample_text, voice=v.stem, lang="vi", total_steps=args.steps, seed=args.seed
        )
        tts.save_audio(wav, out_dir / f"{v.stem}.wav")
        print(f"{v.stem:12s} {duration:5.2f}s audio  {time.perf_counter() - start:5.2f}s wall")
    return 0


if __name__ == "__main__":
    sys.exit(main())
