---
license: apache-2.0
language:
  - vi
  - en
pipeline_tag: text-to-speech
library_name: onnx
tags:
  - text-to-speech
  - tts
  - vietnamese
  - code-switching
  - onnx
  - onnxruntime
  - on-device
  - flow-matching
  - supertonic
datasets:
  - thivux/phoaudiobook
---

# KorvaTTS — Vietnamese-first, on-device text-to-speech

[![GitHub](https://img.shields.io/badge/GitHub-dogenthq%2FKorvaTTS-black?logo=github)](https://github.com/dogenthq/KorvaTTS)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green)](https://github.com/dogenthq/KorvaTTS/blob/main/MODEL_LICENSE.md)

KorvaTTS is an open-source text-to-speech model focused on **Vietnamese with natural code-switching** (Vietnamese sentences containing English words, brand names and tech terms). It runs entirely on-device through ONNX Runtime — no GPU, no API calls — and outputs 44.1 kHz audio.

The model is a from-scratch re-implementation of the 99M-parameter [Supertonic 3](https://github.com/supertone-inc/supertonic) architecture (flow-matching TTS) with a vocoder based on [BlueCodec](https://github.com/maxmelichov/BlueTTS), trained on Vietnamese speech. **No Supertonic checkpoint was used.**

## Voices

10 bundled voices (5 female, 5 male). Each clip below is the reference recording the voice style was built from (`raw_voices/`), so you hear the real speaker the model reproduces.

| Voice | Name | Gender | Reference recording |
|-------|------|--------|--------|
| `bao_kim` | Bảo Kim | female | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/bao_kim.wav"></audio> |
| `khanh_vy` | Khánh Vy | female | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/khanh_vy.wav"></audio> |
| `ngoc_huyen` | Ngọc Huyền | female | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/ngoc_huyen.wav"></audio> |
| `phuong_linh` | Phương Linh | female | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/phuong_linh.wav"></audio> |
| `quynh_nhu` | Quỳnh Như | female | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/quynh_nhu.wav"></audio> |
| `gia_bao` | Gia Bảo | male | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/gia_bao.wav"></audio> |
| `hoang_nam` | Hoàng Nam | male | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/hoang_nam.wav"></audio> |
| `huu_dat` | Hữu Đạt | male | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/huu_dat.wav"></audio> |
| `quang_huy` | Quang Huy | male | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/quang_huy.wav"></audio> |
| `thanh_phong` | Thanh Phong | male | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/thanh_phong.wav"></audio> |

## Usage

```bash
pip install korvatts
```

```python
from korvatts import TTS

tts = TTS()  # downloads this repo on first run
wav, duration = tts.synthesize(
    "Hôm nay team mình sẽ demo tính năng text-to-speech mới.",
    voice="khanh_vy",
    lang="vi",
    total_steps=32,  # default, best quality; 8-16 for faster synthesis
)
tts.save_audio(wav, "output.wav")
```

```bash
korvatts synth "Xin chào, đây là KorvaTTS." -v khanh_vy -o hello.wav
```

Full documentation, CLI reference and roadmap: [github.com/dogenthq/KorvaTTS](https://github.com/dogenthq/KorvaTTS).

## Files

| Path | Description |
|------|-------------|
| `onnx/duration_predictor.onnx` | Predicts utterance length from text + duration style |
| `onnx/text_encoder.onnx` | Character-level text encoder conditioned on voice style |
| `onnx/vector_estimator.onnx` | Flow-matching latent denoiser (256 MB fp32) |
| `onnx/vocoder.onnx` | BlueCodec-based latent → 44.1 kHz waveform decoder |
| `onnx/tts.json`, `onnx/unicode_indexer.json` | Architecture hyper-parameters and character table |
| `voice_styles/<voice>.json` | Precomputed style tokens (`style_ttl` 1×50×256, `style_dp` 1×8×16) |
| `raw_voices/<voice>.wav` | Reference recordings (44.1 kHz mono, 8–12 s) the styles were built from (table above) |

## Compatibility with Supertonic runtimes

The ONNX graph signatures and the voice-style JSON format are identical to Supertonic 3, so `onnx/` and `voice_styles/` can be dropped into any Supertonic 3 runtime (Python, Node.js, WebGPU, Rust, C++, Swift, Flutter, …). This holds for roadmap phases 1–2; phase 3 will change the architecture and break compatibility. Compatible checkpoints are tagged as such.

## Language support

- **Vietnamese** (`vi`) — primary target, including embedded English words.
- **English** (`en`) — part of the training data; works, but English quality is not guaranteed to match the original Supertonic 3 English voices.
- Other Supertonic 3 language tags are accepted by the encoder but were not trained on.

## Training data

- [PhoAudiobook](https://huggingface.co/datasets/thivux/phoaudiobook) — 941 h of curated Vietnamese audiobook speech ([ACL 2025](https://aclanthology.org/2025.acl-short.81.pdf)).
- A private Vietnamese/English code-switching corpus collected by the authors (not released).

## License

Weights, voice styles and audio in this repository: **Apache-2.0** (see [MODEL_LICENSE.md](https://github.com/dogenthq/KorvaTTS/blob/main/MODEL_LICENSE.md)). Trained from scratch; not derived from Supertonic weights. Inference code: Apache-2.0, with portions adapted from Supertonic (MIT) — see [NOTICE](https://github.com/dogenthq/KorvaTTS/blob/main/NOTICE).

**Responsible use:** only clone or imitate voices you own or have permission to use; do not use generated speech to deceive, harass or impersonate.

## Citation

```bibtex
@misc{korvatts2026,
  title        = {KorvaTTS: Vietnamese-first on-device text-to-speech},
  author       = {dogenthq},
  year         = {2026},
  howpublished = {\url{https://github.com/dogenthq/KorvaTTS}}
}
```

Please also cite [SupertonicTTS](https://arxiv.org/abs/2503.23108), [BlueTTS](https://github.com/maxmelichov/BlueTTS) and [PhoAudiobook](https://aclanthology.org/2025.acl-short.81.pdf) — BibTeX entries in the [GitHub README](https://github.com/dogenthq/KorvaTTS#acknowledgements--citation).
