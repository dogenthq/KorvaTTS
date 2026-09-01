# KorvaTTS — Vietnamese-first, on-device text-to-speech

[🇻🇳 Tiếng Việt](README.vi.md)

[![Models](https://img.shields.io/badge/🤗%20Hugging%20Face-dogenthq%2FKorvaTTS-blue)](https://huggingface.co/dogenthq/KorvaTTS)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/dogenthq/KorvaTTS?style=social)](https://github.com/dogenthq/KorvaTTS/stargazers)
[![Discord](https://img.shields.io/badge/Discord-join%20the%20community-5865F2?logo=discord&logoColor=white)](https://discord.gg/cX5rmsRcsg)

KorvaTTS is an open-source text-to-speech system focused on **Vietnamese with natural code-switching** (Vietnamese sentences that contain English words, brand names, tech terms). It runs entirely on-device through ONNX Runtime: no GPU required, no API calls, 44.1 kHz output.

The model is our own re-implementation of the 99M-parameter [Supertonic 3](https://github.com/supertone-inc/supertonic) architecture (flow-matching TTS), **trained from scratch** on Vietnamese data, with a vocoder based on [BlueCodec](https://github.com/maxmelichov/BlueTTS). Upstream Supertonic is being archived by its authors; KorvaTTS continues the line with a Vietnamese focus and an open roadmap toward voice cloning and training.

## Highlights

- 🇻🇳 **Vietnamese-first** — trained on Vietnamese audiobook speech plus a private code-switching set
- 🔀 **Code-switching** — English words inside Vietnamese sentences are read naturally
- ⚡ **Fast on CPU** — real-time factor well below 1 on a laptop CPU; GPU optional
- 🔊 **44.1 kHz WAV** output, no external upsampler
- 🧩 **Drop-in compatible** with Supertonic 3 runtimes (see [Compatibility](#compatibility-with-supertonic))
- 🪪 **Apache-2.0** for both code and weights

## Voices

10 bundled voices — 5 female, 5 male. Listen to every voice on the [Hugging Face model card](https://huggingface.co/dogenthq/KorvaTTS#voices).

| Female | Male |
|--------|------|
| `bao_kim` — Bảo Kim | `gia_bao` — Gia Bảo |
| `khanh_vy` — Khánh Vy | `hoang_nam` — Hoàng Nam |
| `ngoc_huyen` — Ngọc Huyền | `huu_dat` — Hữu Đạt |
| `phuong_linh` — Phương Linh | `quang_huy` — Quang Huy |
| `quynh_nhu` — Quỳnh Như | `thanh_phong` — Thanh Phong |

## Installation

```bash
pip install korvatts
```

Requires Python ≥ 3.10. For GPU inference install `onnxruntime-gpu` (CUDA) instead of `onnxruntime`.

## Quick start

```python
from korvatts import TTS

tts = TTS()  # first run downloads weights + voices from Hugging Face
print(tts.list_voices())

wav, duration = tts.synthesize(
    "Hôm nay team mình sẽ demo tính năng text-to-speech mới.",
    voice="khanh_vy",
    lang="vi",
    total_steps=32,  # default; best quality. Lower (8-16) for faster synthesis
    speed=1.0,       # 0.5 .. 2.0
)
tts.save_audio(wav, "output.wav")
```

Command line:

```bash
korvatts voices
korvatts synth "Xin chào, đây là KorvaTTS." -v khanh_vy -o hello.wav
```

Use local assets instead of downloading: pass `TTS(assets_dir="path/to/assets")` or set `KORVATTS_ASSETS_DIR`. The directory must contain `onnx/` and `voice_styles/`.

## Language support

- **Primary:** Vietnamese (`lang="vi"`), including English words embedded in Vietnamese text.
- **English (`lang="en"`):** part of the training data is English, so plain English works, but we do **not** guarantee English quality matches — or exceeds — the original Supertonic 3 English voices. Vietnamese is what this model is built for.
- **Other languages:** the Supertonic 3 tag set (31 languages) is still accepted by the text encoder, but those languages were not in the training data; quality is untested.

## Compatibility with Supertonic

The phase-1 weights keep the exact ONNX graph signatures and voice-style JSON format of Supertonic 3. You can copy the KorvaTTS `onnx/` and `voice_styles/` folders into any Supertonic 3 runtime (Python, Node.js, browser/WebGPU, Rust, C++, Swift, Flutter, …) and they will work unchanged.

This compatibility is intentional for phases 1–2. **Phase 3 will change the architecture and will not be loadable by Supertonic runtimes.** Version tags on Hugging Face will make it clear which checkpoints are compatible.

## Roadmap

| Phase | Scope | Status |
|-------|-------|--------|
| **1. ONNX inference** | Python package, CLI, published weights + voice styles on Hugging Face | ✅ this release |
| **2. Voice cloning + training** | Reference-audio → voice style encoder, PyTorch training / fine-tuning recipes, dataset tooling | 🔜 planned |
| **3. Architecture improvements** | Original changes to the TTS + cloning architecture for better Vietnamese prosody and cloning fidelity. **Breaks Supertonic compatibility.** | 🧭 later |

Phase 2 starts once the phase-1 release has a healthy community around it — **our goal is 1,000 GitHub stars** ⭐ [![GitHub stars](https://img.shields.io/github/stars/dogenthq/KorvaTTS?label=current&color=yellow)](https://github.com/dogenthq/KorvaTTS/stargazers). Star the repo to move the roadmap forward, and join our [Discord](https://discord.gg/cX5rmsRcsg) or watch the issues tab for progress.

<a href="https://star-history.com/#dogenthq/KorvaTTS&Date"><img src="https://api.star-history.com/svg?repos=dogenthq/KorvaTTS&type=Date" alt="Star History Chart" width="600"></a>

## Training data

- [PhoAudiobook](https://huggingface.co/datasets/thivux/phoaudiobook) — 941 hours of curated Vietnamese audiobook speech, introduced in [Zero-Shot Text-to-Speech for Vietnamese (ACL 2025)](https://aclanthology.org/2025.acl-short.81.pdf).
- A private, author-collected Vietnamese/English code-switching set used to improve mixed-language reading. This set is not released.

## Community

Join the KorvaTTS Discord to ask questions, share what you build, request voices, and follow phase-2 development: **[discord.gg/cX5rmsRcsg](https://discord.gg/cX5rmsRcsg)**. Bug reports and feature requests are welcome on [GitHub Issues](https://github.com/dogenthq/KorvaTTS/issues).

## Support the project

KorvaTTS is free and open source. Training runs and voice recordings cost real money — if this project is useful to you, a small donation goes directly into the voice cloning and training work in phase 2. Scan the VietQR code below with any Vietnamese banking app (international options coming later).

<img src="https://img.vietqr.io/image/970407-19035566489014-compact.png?addInfo=Ung%20ho%20KorvaTTS&accountName=LE%20TAN%20NGHIA" alt="VietQR — Techcombank 19035566489014 — LE TAN NGHIA" width="320">

## Contributing

Issues and pull requests are welcome. Run the checks locally:

```bash
pip install -e ".[dev]"
ruff check .
pytest        # model tests auto-skip unless ./assets exists
```

## Licenses

| Component | License |
|-----------|---------|
| Source code in this repository | [Apache-2.0](LICENSE) |
| Model weights & voice styles | [Apache-2.0](MODEL_LICENSE.md) — trained from scratch, not derived from Supertonic weights |

Portions of the inference code are adapted from Supertonic (MIT, © Supertone Inc.); the vocoder follows BlueCodec from BlueTTS (MIT). See [NOTICE](NOTICE). KorvaTTS is not affiliated with Supertone Inc.

## Acknowledgements & citation

KorvaTTS builds on the work of others. If you use it, please also cite them:

- **Supertonic / SupertonicTTS** — architecture and reference implementation. [github.com/supertone-inc/supertonic](https://github.com/supertone-inc/supertonic)
- **BlueTTS / BlueCodec** — vocoder design. [github.com/maxmelichov/BlueTTS](https://github.com/maxmelichov/BlueTTS)
- **PhoAudiobook** — Vietnamese training corpus. [huggingface.co/datasets/thivux/phoaudiobook](https://huggingface.co/datasets/thivux/phoaudiobook)

```bibtex
@misc{korvatts2026,
  title        = {KorvaTTS: Vietnamese-first on-device text-to-speech},
  author       = {dogenthq},
  year         = {2026},
  howpublished = {\url{https://github.com/dogenthq/KorvaTTS}}
}

@article{kim2025supertonictts,
  title   = {SupertonicTTS: Towards Highly Efficient and Streamlined Text-to-Speech System},
  author  = {Kim, Hyeongju and Yang, Jinhyeok and Yu, Yechan and Ji, Seunghun and Morton, Jacob and Bous, Frederik and Byun, Joon and Lee, Juheon},
  journal = {arXiv preprint arXiv:2503.23108},
  year    = {2025}
}

@misc{melichov2025bluetts,
  title        = {BlueTTS},
  author       = {Melichov, Max},
  year         = {2025},
  howpublished = {\url{https://github.com/maxmelichov/BlueTTS}}
}

@inproceedings{vu2025phoaudiobook,
  title     = {Zero-Shot Text-to-Speech for Vietnamese},
  author    = {Vu, Thi and Nguyen, Linh The and Nguyen, Dat Quoc},
  booktitle = {Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Short Papers)},
  year      = {2025}
}
```
