# KorvaTTS — Text-to-speech chạy on-device, ưu tiên tiếng Việt

[🇬🇧 English](README.md)

[![Models](https://img.shields.io/badge/🤗%20Hugging%20Face-dogenthq%2FKorvaTTS-blue)](https://huggingface.co/dogenthq/KorvaTTS)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/dogenthq/KorvaTTS?style=social)](https://github.com/dogenthq/KorvaTTS/stargazers)
[![Try it online](https://img.shields.io/badge/🌐%20Try%20it%20online-heykorva.com-2ea44f)](https://heykorva.com/)
[![Discord](https://img.shields.io/badge/Discord-tham%20gia%20cộng%20đồng-5865F2?logo=discord&logoColor=white)](https://discord.gg/cX5rmsRcsg)

KorvaTTS là hệ thống text-to-speech mã nguồn mở tập trung vào **tiếng Việt có code-switching** (câu tiếng Việt chứa từ tiếng Anh, tên thương hiệu, thuật ngữ kỹ thuật). Toàn bộ chạy on-device qua ONNX Runtime: không cần GPU, không gọi API, âm thanh 44.1 kHz.

Model là bản re-implement của chúng tôi theo kiến trúc [Supertonic 3](https://github.com/supertone-inc/supertonic) (99M tham số, flow-matching TTS), **train từ đầu** trên dữ liệu tiếng Việt, với vocoder dựa trên [BlueCodec](https://github.com/maxmelichov/BlueTTS). Nhóm tác giả Supertonic đang archive repo gốc; KorvaTTS tiếp nối hướng đi này với trọng tâm tiếng Việt và lộ trình mở hướng tới voice cloning và training.

**🌐 Dùng thử ngay trên trình duyệt — không cần cài đặt:** [heykorva.com](https://heykorva.com/)

## Điểm nổi bật

- 🇻🇳 **Ưu tiên tiếng Việt** — huấn luyện trên audiobook tiếng Việt cộng thêm bộ dữ liệu code-switching riêng
- 🔀 **Code-switching** — từ tiếng Anh nằm trong câu tiếng Việt được đọc tự nhiên
- ⚡ **Nhanh trên CPU** — real-time factor nhỏ hơn 1 trên CPU laptop; GPU là tuỳ chọn
- 🔊 Xuất **WAV 44.1 kHz**, không cần upsampler ngoài
- 🧩 **Tương thích trực tiếp** với các runtime Supertonic 3 (xem [Tương thích](#tương-thích-với-supertonic))
- 🪪 **Apache-2.0** cho cả code lẫn weight

## Giọng đọc

10 giọng có sẵn — 5 nữ, 5 nam. Nghe thử từng giọng trên [model card Hugging Face](https://huggingface.co/dogenthq/KorvaTTS#voices).

| Nữ | Nam |
|----|-----|
| `bao_kim` — Bảo Kim | `gia_bao` — Gia Bảo |
| `khanh_vy` — Khánh Vy | `hoang_nam` — Hoàng Nam |
| `ngoc_huyen` — Ngọc Huyền | `huu_dat` — Hữu Đạt |
| `phuong_linh` — Phương Linh | `quang_huy` — Quang Huy |
| `quynh_nhu` — Quỳnh Như | `thanh_phong` — Thanh Phong |

## Cài đặt

```bash
pip install korvatts
```

Yêu cầu Python ≥ 3.10. Muốn chạy GPU, cài `onnxruntime-gpu` (CUDA) thay cho `onnxruntime`.

## Bắt đầu nhanh

```python
from korvatts import TTS

tts = TTS()  # lần chạy đầu sẽ tải weight + voice từ Hugging Face
print(tts.list_voices())

wav, duration = tts.synthesize(
    "Hôm nay team mình sẽ demo tính năng text-to-speech mới.",
    voice="khanh_vy",
    lang="vi",
    total_steps=32,  # mặc định; chất lượng tốt nhất. Giảm (8-16) nếu cần nhanh hơn
    speed=1.05,      # mặc định; 0.5 (chậm) .. 2.0 (nhanh)
)
tts.save_audio(wav, "output.wav")
```

Dòng lệnh:

```bash
korvatts voices
korvatts synth "Xin chào, đây là KorvaTTS." -v khanh_vy -o hello.wav
```

Dùng asset cục bộ thay vì tải: truyền `TTS(assets_dir="duong/dan/assets")` hoặc đặt biến môi trường `KORVATTS_ASSETS_DIR`. Thư mục phải chứa `onnx/` và `voice_styles/`.

## Hỗ trợ ngôn ngữ

- **Chính:** tiếng Việt (`lang="vi"`), bao gồm từ tiếng Anh xen trong câu tiếng Việt.
- **Tiếng Anh (`lang="en"`):** một phần dữ liệu huấn luyện là tiếng Anh nên câu tiếng Anh thuần vẫn đọc được, nhưng **không đảm bảo** chất lượng bằng hoặc hơn giọng tiếng Anh gốc của Supertonic 3. Model này được xây cho tiếng Việt.
- **Ngôn ngữ khác:** text encoder vẫn nhận tag của 31 ngôn ngữ Supertonic 3, nhưng chúng không có trong dữ liệu huấn luyện; chất lượng chưa kiểm chứng.

## Tương thích với Supertonic

Weight giai đoạn 1 giữ nguyên chữ ký đồ thị ONNX và định dạng JSON voice style của Supertonic 3. Bạn có thể copy thư mục `onnx/` và `voice_styles/` của KorvaTTS sang bất kỳ runtime Supertonic 3 nào (Python, Node.js, trình duyệt/WebGPU, Rust, C++, Swift, Flutter, …) và dùng ngay không cần sửa.

Tương thích này là chủ đích cho giai đoạn 1–2. **Giai đoạn 3 sẽ thay đổi kiến trúc và không còn load được bằng runtime Supertonic.** Tag phiên bản trên Hugging Face sẽ ghi rõ checkpoint nào còn tương thích.

## Lộ trình

| Giai đoạn | Phạm vi | Trạng thái |
|-----------|---------|------------|
| **1. Inference ONNX** | Package Python, CLI, weight + voice style công bố trên Hugging Face | ✅ bản này |
| **2. Voice cloning + training** | Encoder từ audio tham chiếu → voice style, script train / fine-tune bằng PyTorch, công cụ chuẩn bị dữ liệu | 🔜 dự kiến |
| **3. Cải tiến kiến trúc** | Thay đổi kiến trúc TTS + cloning để prosody tiếng Việt và độ giống giọng tốt hơn. **Sẽ không còn tương thích với Supertonic.** | 🧭 sau này |

Giai đoạn 2 được ưu tiên dựa trên mức độ quan tâm của cộng đồng và nguồn lực hiện có. Theo dõi tiến độ trên [Discord](https://discord.gg/cX5rmsRcsg) và tab Issues — mọi phản hồi, báo lỗi hay đề xuất giọng mới đều góp phần định hình những gì được xây tiếp theo.

<a href="https://star-history.com/#dogenthq/KorvaTTS&Date"><img src="https://api.star-history.com/svg?repos=dogenthq/KorvaTTS&type=Date" alt="Biểu đồ số sao theo thời gian" width="600"></a>

## Dữ liệu huấn luyện

- [PhoAudiobook](https://huggingface.co/datasets/thivux/phoaudiobook) — 941 giờ audiobook tiếng Việt đã được lọc, giới thiệu trong bài [Zero-Shot Text-to-Speech for Vietnamese (ACL 2025)](https://aclanthology.org/2025.acl-short.81.pdf).
- Bộ dữ liệu code-switching Việt/Anh do tác giả tự thu thập để cải thiện khả năng đọc văn bản pha trộn ngôn ngữ. Bộ này không được công bố.

## Cộng đồng

Tham gia Discord của KorvaTTS để hỏi đáp, chia sẻ sản phẩm bạn làm, đề xuất giọng mới và theo dõi tiến độ giai đoạn 2: **[discord.gg/cX5rmsRcsg](https://discord.gg/cX5rmsRcsg)**. Báo lỗi và đề xuất tính năng gửi qua [GitHub Issues](https://github.com/dogenthq/KorvaTTS/issues).

## Ủng hộ dự án

KorvaTTS miễn phí và mã nguồn mở. Mỗi lần train và thu âm giọng đều tốn tiền thật — nếu dự án hữu ích với bạn, một khoản ủng hộ nhỏ sẽ đi thẳng vào phần voice cloning và training ở giai đoạn 2. Quét mã VietQR bên dưới bằng app ngân hàng bất kỳ.

<img src="https://img.vietqr.io/image/970407-19035566489014-compact.png?addInfo=Ung%20ho%20KorvaTTS&accountName=LE%20TAN%20NGHIA" alt="VietQR — Techcombank 19035566489014 — LE TAN NGHIA" width="320">

## Đóng góp

Hoan nghênh issue và pull request. Chạy kiểm tra cục bộ:

```bash
pip install -e ".[dev]"
ruff check .
pytest        # test cần model tự bỏ qua nếu chưa có ./assets
```

## License

| Thành phần | License |
|------------|---------|
| Mã nguồn trong repo | [Apache-2.0](LICENSE) |
| Weight & voice style | [Apache-2.0](MODEL_LICENSE.md) — train từ đầu, không phái sinh từ weight Supertonic |

Một phần code inference được chuyển thể từ Supertonic (MIT, © Supertone Inc.); vocoder dựa trên BlueCodec của BlueTTS (MIT). Xem [NOTICE](NOTICE). KorvaTTS không liên kết với Supertone Inc.

## Ghi nhận & trích dẫn

KorvaTTS đứng trên vai những dự án sau. Nếu bạn dùng KorvaTTS, vui lòng trích dẫn cả họ:

- **Supertonic / SupertonicTTS** — kiến trúc và bản tham chiếu. [github.com/supertone-inc/supertonic](https://github.com/supertone-inc/supertonic)
- **BlueTTS / BlueCodec** — thiết kế vocoder. [github.com/maxmelichov/BlueTTS](https://github.com/maxmelichov/BlueTTS)
- **PhoAudiobook** — kho ngữ liệu tiếng Việt. [huggingface.co/datasets/thivux/phoaudiobook](https://huggingface.co/datasets/thivux/phoaudiobook)

Mục BibTeX đầy đủ xem ở [README tiếng Anh](README.md#acknowledgements--citation).
