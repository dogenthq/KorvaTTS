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
[![Discord](https://img.shields.io/badge/Discord-join%20the%20community-5865F2?logo=discord&logoColor=white)](https://discord.gg/cX5rmsRcsg)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green)](https://github.com/dogenthq/KorvaTTS/blob/main/MODEL_LICENSE.md)

KorvaTTS is an open-source text-to-speech model focused on **Vietnamese with natural code-switching** (Vietnamese sentences containing English words, brand names and tech terms). It runs entirely on-device through ONNX Runtime — no GPU, no API calls — and outputs 44.1 kHz audio.

The model is a from-scratch re-implementation of the 99M-parameter [Supertonic 3](https://github.com/supertone-inc/supertonic) architecture (flow-matching TTS) with a vocoder based on [BlueCodec](https://github.com/maxmelichov/BlueTTS), trained on Vietnamese speech. **No Supertonic checkpoint was used.**

## Voices

10 bundled voices (5 female, 5 male). **Sample** = synthesized by KorvaTTS from a different Vietnamese sentence per voice, each with natural English code-switching. **Reference** = the original recording the voice style was built from (`raw_voices/`).

| Voice | Name | Gender | Sample (synthesized) | Reference recording |
|-------|------|--------|----------------------|---------------------|
| `bao_kim` | Bảo Kim | female | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/samples/bao_kim.wav"></audio> | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/bao_kim.wav"></audio> |
| `khanh_vy` | Khánh Vy | female | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/samples/khanh_vy.wav"></audio> | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/khanh_vy.wav"></audio> |
| `ngoc_huyen` | Ngọc Huyền | female | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/samples/ngoc_huyen.wav"></audio> | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/ngoc_huyen.wav"></audio> |
| `phuong_linh` | Phương Linh | female | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/samples/phuong_linh.wav"></audio> | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/phuong_linh.wav"></audio> |
| `quynh_nhu` | Quỳnh Như | female | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/samples/quynh_nhu.wav"></audio> | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/quynh_nhu.wav"></audio> |
| `gia_bao` | Gia Bảo | male | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/samples/gia_bao.wav"></audio> | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/gia_bao.wav"></audio> |
| `hoang_nam` | Hoàng Nam | male | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/samples/hoang_nam.wav"></audio> | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/hoang_nam.wav"></audio> |
| `huu_dat` | Hữu Đạt | male | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/samples/huu_dat.wav"></audio> | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/huu_dat.wav"></audio> |
| `quang_huy` | Quang Huy | male | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/samples/quang_huy.wav"></audio> | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/quang_huy.wav"></audio> |
| `thanh_phong` | Thanh Phong | male | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/samples/thanh_phong.wav"></audio> | <audio controls preload="none" src="https://huggingface.co/dogenthq/KorvaTTS/resolve/main/raw_voices/thanh_phong.wav"></audio> |

<details>
<summary>Sample sentences</summary>

- **Bảo Kim** (`bao_kim`): "Chào mừng bạn đến với podcast Công nghệ mỗi ngày. Hôm nay chúng ta sẽ nói về cách AI đang thay đổi ngành marketing và những skill mà người làm content cần có."
- **Khánh Vy** (`khanh_vy`): "Dạ, đơn hàng của anh đã được xác nhận và sẽ ship trong vòng hai ngày. Anh có thể track đơn hàng qua app hoặc website của bên em bất cứ lúc nào ạ."
- **Ngọc Huyền** (`ngoc_huyen`): "Trong bài học hôm nay, các em sẽ học cách dùng hàm filter và map trong JavaScript để xử lý dữ liệu. Mở file bài tập lên và chúng ta bắt đầu nhé."
- **Phương Linh** (`phuong_linh`): "Tin nhanh buổi sáng: chỉ số VN-Index tăng nhẹ, trong khi nhóm cổ phiếu công nghệ tiếp tục thu hút dòng tiền từ các quỹ đầu tư nước ngoài."
- **Quỳnh Như** (`quynh_nhu`): "Bạn có mười phút không? Mình muốn demo tính năng voice cloning mới, feedback của bạn rất quan trọng với team trước khi release."
- **Gia Bảo** (`gia_bao`): "Chào cả nhà, hôm nay mình review chiếc laptop mới: màn hình OLED, pin trâu, và hiệu năng thì khỏi bàn. Bấm subscribe để không bỏ lỡ video tiếp theo nhé."
- **Hoàng Nam** (`hoang_nam`): "Thưa quý khách, chuyến bay VN một hai ba đi Đà Nẵng sẽ bắt đầu boarding tại cửa số bảy trong vài phút nữa. Xin vui lòng chuẩn bị sẵn thẻ lên máy bay."
- **Hữu Đạt** (`huu_dat`): "Sprint này team cần hoàn thành phần login bằng OAuth, còn phần dashboard sẽ dời sang sprint sau. Ai có blocker thì báo trong daily standup nhé."
- **Quang Huy** (`quang_huy`): "Nhớ backup dữ liệu trước khi update hệ điều hành, nếu không lỡ mất file thì khó khôi phục lắm đấy. Tốt nhất là sync lên cloud rồi hãy bấm cài đặt."
- **Thanh Phong** (`thanh_phong`): "Trận đấu tối nay giữa Việt Nam và Thái Lan sẽ được livestream lúc bảy giờ rưỡi trên kênh chính thức. Anh em nhớ đặt lịch để không bỏ lỡ highlight nhé."

</details>

## Community

Questions, voice requests, show-and-tell: **[Discord](https://discord.gg/cX5rmsRcsg)** · bugs: [GitHub Issues](https://github.com/dogenthq/KorvaTTS/issues).

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
| `samples/<voice>.wav` | Synthesized demo clips, one distinct sentence per voice (table above) |
| `raw_voices/<voice>.wav` | Reference recordings (44.1 kHz mono, 8–12 s) the styles were built from |

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
