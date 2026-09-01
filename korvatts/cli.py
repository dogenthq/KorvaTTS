"""Command-line interface: ``korvatts synth`` and ``korvatts voices``."""

from __future__ import annotations

import argparse
import sys
import time

from korvatts import __version__
from korvatts.session import DEVICES
from korvatts.text_processor import AVAILABLE_LANGS
from korvatts.tts import DEFAULT_TOTAL_STEPS, MAX_TOTAL_STEPS, TTS


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="korvatts", description="KorvaTTS on-device TTS")
    parser.add_argument("--version", action="version", version=f"korvatts {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--assets-dir", help="Local assets directory (default: auto-resolve)")
    common.add_argument("--device", default="auto", choices=DEVICES)

    synth = sub.add_parser("synth", parents=[common], help="Synthesize text to a WAV file")
    synth.add_argument("text", help="Text to speak (wrap in quotes)")
    synth.add_argument(
        "-v", "--voice", default=None,
        help="Voice name (see `korvatts voices`); default: first available voice",
    )
    synth.add_argument("-l", "--lang", default="vi", choices=AVAILABLE_LANGS)
    synth.add_argument("-o", "--output", default="output.wav", help="Output WAV path")
    synth.add_argument(
        "--steps", type=int, default=DEFAULT_TOTAL_STEPS,
        help=f"Denoising steps, 1..{MAX_TOTAL_STEPS}; fewer = faster, {MAX_TOTAL_STEPS} = best",
    )
    synth.add_argument("--speed", type=float, default=1.0, help="0.5 (slow) .. 2.0 (fast)")
    synth.add_argument("--seed", type=int, default=None, help="Fix random seed for reproducibility")

    sub.add_parser("voices", parents=[common], help="List available voice styles")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        tts = TTS(assets_dir=args.assets_dir, device=args.device)
        if args.command == "voices":
            for name in tts.list_voices():
                print(name)
            return 0

        voice = args.voice or (tts.list_voices() or [None])[0]
        if voice is None:
            raise FileNotFoundError("no voice styles found in assets/voice_styles")
        start = time.perf_counter()
        wav, duration = tts.synthesize(
            args.text, voice=voice, lang=args.lang, total_steps=args.steps,
            speed=args.speed, seed=args.seed,
        )
        elapsed = time.perf_counter() - start
        tts.save_audio(wav, args.output)
        print(
            f"Saved {args.output} ({duration:.2f}s audio, {elapsed:.2f}s wall, "
            f"RTF {elapsed / max(duration, 1e-6):.3f}, provider {tts.sessions.active_provider})"
        )
        return 0
    except Exception as exc:  # noqa: BLE001 — CLI boundary: any failure becomes exit code 1
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
