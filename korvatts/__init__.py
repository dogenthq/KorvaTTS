"""KorvaTTS — Vietnamese-first, on-device text-to-speech built on ONNX Runtime."""

from korvatts.assets import resolve_assets_dir
from korvatts.text_processor import AVAILABLE_LANGS
from korvatts.tts import TTS
from korvatts.voice_style import VoiceStyle

__version__ = "0.1.1"

__all__ = ["AVAILABLE_LANGS", "TTS", "VoiceStyle", "__version__", "resolve_assets_dir"]
