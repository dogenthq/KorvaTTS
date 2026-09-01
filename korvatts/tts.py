"""High-level synthesis API.

Pipeline per chunk of text:
  text -> TextProcessor -> duration_predictor -> text_encoder
       -> flow-matching loop over vector_estimator (``total_steps`` iterations)
       -> vocoder -> 44.1 kHz float32 waveform

The shipped ONNX graphs fix the batch dimension to 1, so the API is single-utterance only.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import soundfile as sf

from korvatts.assets import list_voices, resolve_assets_dir
from korvatts.session import ModelSessions
from korvatts.text_processor import TextProcessor, chunk_text, length_to_mask
from korvatts.voice_style import VoiceStyle

DEFAULT_TOTAL_STEPS = 32  # maximum supported; best quality
MAX_TOTAL_STEPS = 32
SPEED_RANGE = (0.5, 2.0)


class TTS:
    """Load ONNX assets once, then call :meth:`synthesize` repeatedly."""

    def __init__(
        self,
        assets_dir: str | Path | None = None,
        device: str = "auto",
        auto_download: bool = True,
        num_threads: int | None = None,
    ):
        self.assets_dir = resolve_assets_dir(assets_dir, auto_download=auto_download)
        onnx_dir = self.assets_dir / "onnx"
        with open(onnx_dir / "tts.json", "r", encoding="utf-8") as f:
            self.config = json.load(f)
        self.sessions = ModelSessions.load(onnx_dir, device=device, num_threads=num_threads)
        self.text_processor = TextProcessor(onnx_dir / "unicode_indexer.json")

        self.sample_rate: int = self.config["ae"]["sample_rate"]
        self._base_chunk_size: int = self.config["ae"]["base_chunk_size"]
        self._chunk_compress: int = self.config["ttl"]["chunk_compress_factor"]
        self._latent_dim: int = self.config["ttl"]["latent_dim"]

    # ---- voices -----------------------------------------------------------------------------

    def list_voices(self) -> list[str]:
        return list_voices(self.assets_dir)

    def get_voice(self, name: str) -> VoiceStyle:
        # Names are file stems only; reject anything that could escape voice_styles/.
        if name not in self.list_voices():
            raise FileNotFoundError(
                f"Voice '{name}' not found. Available: {', '.join(self.list_voices()) or 'none'}"
            )
        return VoiceStyle.from_file(self.assets_dir / "voice_styles" / f"{name}.json")

    # ---- synthesis --------------------------------------------------------------------------

    def synthesize(
        self,
        text: str,
        voice: VoiceStyle | str,
        lang: str = "vi",
        total_steps: int = DEFAULT_TOTAL_STEPS,
        speed: float = 1.0,
        silence_between_chunks: float = 0.3,
        seed: int | None = None,
    ) -> tuple[np.ndarray, float]:
        """Synthesize arbitrarily long text with one speaker.

        Returns ``(wav, duration_seconds)`` where ``wav`` has shape (num_samples,).
        """
        style = self.get_voice(voice) if isinstance(voice, str) else voice
        _validate_params(total_steps, speed, silence_between_chunks)
        if not text or not text.strip():
            raise ValueError("text is empty")

        max_len = 120 if lang in ("ko", "ja") else 300
        chunks = chunk_text(text, max_len=max_len)
        rng = np.random.default_rng(seed)
        pieces: list[np.ndarray] = []
        total = 0.0
        silence = np.zeros(int(silence_between_chunks * self.sample_rate), dtype=np.float32)
        for chunk in chunks:
            wav, dur = self._infer(chunk, lang, style, total_steps, speed, rng)
            trimmed = wav[0, : int(dur * self.sample_rate)]
            if pieces:
                pieces.append(silence)
                total += silence_between_chunks
            pieces.append(trimmed)
            total += dur
        return np.concatenate(pieces), total

    def save_audio(self, wav: np.ndarray, path: str | Path) -> None:
        sf.write(str(path), wav, self.sample_rate)

    # ---- internals --------------------------------------------------------------------------

    def _infer(self, text, lang, style: VoiceStyle, total_steps, speed, rng):
        s = self.sessions
        text_ids, text_mask = self.text_processor.encode([text], [lang])
        (duration,) = s.duration_predictor.run(
            None, {"text_ids": text_ids, "style_dp": style.dp, "text_mask": text_mask}
        )
        duration = duration / speed
        (text_emb,) = s.text_encoder.run(
            None, {"text_ids": text_ids, "style_ttl": style.ttl, "text_mask": text_mask}
        )
        latent, latent_mask = self._sample_noisy_latent(duration, rng)
        total_np = np.array([total_steps], dtype=np.float32)
        for step in range(total_steps):
            (latent,) = s.vector_estimator.run(
                None,
                {
                    "noisy_latent": latent,
                    "text_emb": text_emb,
                    "style_ttl": style.ttl,
                    "text_mask": text_mask,
                    "latent_mask": latent_mask,
                    "current_step": np.array([step], dtype=np.float32),
                    "total_step": total_np,
                },
            )
        (wav,) = s.vocoder.run(None, {"latent": latent})
        return wav, float(duration[0])

    def _sample_noisy_latent(self, duration: np.ndarray, rng: np.random.Generator):
        """Gaussian noise of the right latent length for the predicted duration, masked."""
        wav_lengths = (duration * self.sample_rate).astype(np.int64)
        chunk = self._base_chunk_size * self._chunk_compress
        latent_lengths = (wav_lengths + chunk - 1) // chunk
        latent_len = int(latent_lengths.max())
        latent_dim = self._latent_dim * self._chunk_compress
        noise = rng.standard_normal((1, latent_dim, latent_len), dtype=np.float32)
        latent_mask = length_to_mask(latent_lengths, latent_len)
        return noise * latent_mask, latent_mask


def _validate_params(total_steps: int, speed: float, silence: float) -> None:
    if not 1 <= total_steps <= MAX_TOTAL_STEPS:
        raise ValueError(f"total_steps must be between 1 and {MAX_TOTAL_STEPS}")
    if not SPEED_RANGE[0] <= speed <= SPEED_RANGE[1]:
        raise ValueError(f"speed must be between {SPEED_RANGE[0]} and {SPEED_RANGE[1]}")
    if silence < 0:
        raise ValueError("silence_between_chunks must be >= 0")
