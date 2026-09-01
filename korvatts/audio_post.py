"""Post-processing for synthesized audio tails.

Trimming the waveform at the predicted duration can leave either an abrupt cut in the middle of
speech energy or a detached vocoder noise burst after the final pause. Both are audible as a
click or crackle at the end of the file. :func:`clean_tail` removes the detached burst (if any)
and fades the remaining tail to zero.
"""

from __future__ import annotations

import numpy as np

_FRAME_S = 0.02  # RMS analysis frame
_SEARCH_S = 0.6  # how far from the end to look for a trailing pause
_GAP_RMS = 0.01  # below this RMS a frame counts as silence
_MIN_GAP_S = 0.05  # a pause must be at least this long to separate speech from a burst
_MAX_BURST_S = 0.35  # audio after the pause longer than this is treated as real speech
_BURST_PEAK = 0.4  # bursts run near clipping; trailing real speech stays below this after a pause
_KEEP_PAUSE_S = 0.05  # how much of the pause to keep after cutting
_FADE_S = 0.03


def clean_tail(wav: np.ndarray, sample_rate: int) -> np.ndarray:
    """Return ``wav`` with any trailing vocoder burst removed and the tail faded to zero."""
    cut = _detached_burst_start(wav, sample_rate)
    if cut is not None:
        wav = wav[: cut + int(_KEEP_PAUSE_S * sample_rate)]
    _fade_out(wav, sample_rate)
    return wav


def _detached_burst_start(wav: np.ndarray, sample_rate: int) -> int | None:
    """Start index of the trailing pause separating speech from a short burst, if present."""
    frame = int(_FRAME_S * sample_rate)
    start = max(0, len(wav) - int(_SEARCH_S * sample_rate))
    gap_start = None
    run = 0
    best = None
    for i in range(start, len(wav) - frame, frame):
        rms = float(np.sqrt(np.mean(wav[i : i + frame] ** 2)))
        if rms < _GAP_RMS:
            if run == 0:
                gap_start = i
            run += frame
        else:
            if run >= _MIN_GAP_S * sample_rate:
                best = gap_start
            run = 0
    if run >= _MIN_GAP_S * sample_rate:
        best = gap_start
    if best is None:
        return None
    after = wav[best + int(_MIN_GAP_S * sample_rate) :]
    peak = float(np.abs(after).max()) if len(after) else 0.0
    if peak < 0.05:
        return best  # only silence remains: trim it
    # A burst is short AND abnormally loud; anything long or moderate is real speech.
    if len(after) <= int(_MAX_BURST_S * sample_rate) and peak >= _BURST_PEAK:
        return best
    return None


def _fade_out(wav: np.ndarray, sample_rate: int, duration: float = _FADE_S) -> None:
    """Linear fade to zero over the last ``duration`` seconds, in place."""
    n = min(len(wav), int(duration * sample_rate))
    if n > 0:
        wav[-n:] *= np.linspace(1.0, 0.0, n, dtype=wav.dtype)
