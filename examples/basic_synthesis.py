"""Minimal example: synthesize a Vietnamese sentence with code-switched English."""

from korvatts import TTS

tts = TTS()  # resolves ./assets or downloads from HuggingFace on first run
print("Available voices:", tts.list_voices())

text = "Hôm nay team mình sẽ demo tính năng text-to-speech mới cho khách hàng."
wav, duration = tts.synthesize(text, voice="khanh_vy", lang="vi", speed=1.0)  # total_steps=32
tts.save_audio(wav, "output.wav")
print(f"Wrote output.wav ({duration:.2f}s @ {tts.sample_rate} Hz)")
