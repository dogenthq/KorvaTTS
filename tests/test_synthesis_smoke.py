"""End-to-end smoke tests against real ONNX assets (skipped when assets/ is absent)."""

import numpy as np
import pytest

from korvatts import TTS


@pytest.fixture(scope="module")
def tts(assets_dir):
    return TTS(assets_dir=assets_dir, device="cpu", auto_download=False)


def test_lists_bundled_voices(tts):
    voices = tts.list_voices()
    assert len(voices) >= 1


def test_synthesize_vietnamese(tts):
    voice = tts.list_voices()[0]
    wav, duration = tts.synthesize("Xin chào, đây là bài kiểm tra.", voice=voice, lang="vi",
                                   total_steps=32, seed=0)
    assert wav.ndim == 1 and wav.dtype == np.float32
    assert 0.3 < duration < 10
    assert abs(len(wav) / tts.sample_rate - duration) < 0.05
    assert np.abs(wav).max() > 0.01  # not silence


def test_synthesize_is_reproducible_with_seed(tts):
    voice = tts.list_voices()[0]
    a, _ = tts.synthesize("Một hai ba.", voice=voice, total_steps=3, seed=42)
    b, _ = tts.synthesize("Một hai ba.", voice=voice, total_steps=3, seed=42)
    assert np.allclose(a, b, atol=1e-4)


def test_unknown_voice_raises(tts):
    with pytest.raises(FileNotFoundError):
        tts.get_voice("does-not-exist")


def test_invalid_params_raise(tts):
    voice = tts.list_voices()[0]
    with pytest.raises(ValueError):
        tts.synthesize("x.", voice=voice, total_steps=0)
    with pytest.raises(ValueError):
        tts.synthesize("x.", voice=voice, speed=5.0)
    with pytest.raises(ValueError):
        tts.synthesize("   ", voice=voice)


def test_voice_name_cannot_escape_voice_styles_dir(tts):
    with pytest.raises(FileNotFoundError):
        tts.get_voice("../onnx/tts")


def test_output_tail_is_cleaned(tts):
    voice = tts.list_voices()[0]
    wav, duration = tts.synthesize("Xin chào các bạn.", voice=voice, total_steps=4, seed=0)
    sr = tts.sample_rate
    assert wav[-1] == 0.0  # fade ends exactly at zero
    assert np.abs(wav[-int(0.002 * sr) :]).max() < 0.25  # no abrupt cut / burst at the end
    assert abs(len(wav) / sr - duration) < 1e-3  # duration reflects the cleaned audio


def test_long_text_is_chunked_and_joined(tts):
    voice = tts.list_voices()[0]
    text = "Đây là câu thứ nhất. " * 30  # > 300 chars → several chunks
    wav, duration = tts.synthesize(text, voice=voice, total_steps=2, seed=0)
    assert duration > 5
    assert abs(len(wav) / tts.sample_rate - duration) < 0.05
