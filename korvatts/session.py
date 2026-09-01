"""ONNX Runtime session creation and execution-provider selection."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import onnxruntime as ort

# Providers usable with default session options. DirectML is intentionally excluded: it needs
# special session options (no mem pattern, sequential execution) and is not validated yet.
_GPU_PROVIDERS = ["CUDAExecutionProvider", "CoreMLExecutionProvider"]
DEVICES = ("auto", "cpu", "gpu")


def select_providers(device: str = "auto") -> list[str]:
    """Map a device string ("auto" | "cpu" | "gpu") to an ORT provider list."""
    if device not in DEVICES:
        raise ValueError(f"device must be one of {DEVICES}, got '{device}'")
    if device == "cpu":
        return ["CPUExecutionProvider"]
    available = ort.get_available_providers()
    gpu = [p for p in _GPU_PROVIDERS if p in available]
    if device == "gpu" and not gpu:
        raise RuntimeError(
            "No supported GPU execution provider found. Install onnxruntime-gpu (CUDA) "
            "or use device='cpu'."
        )
    return gpu + ["CPUExecutionProvider"]


@dataclass
class ModelSessions:
    duration_predictor: ort.InferenceSession
    text_encoder: ort.InferenceSession
    vector_estimator: ort.InferenceSession
    vocoder: ort.InferenceSession

    @classmethod
    def load(cls, onnx_dir: Path, device: str = "auto", num_threads: int | None = None):
        opts = ort.SessionOptions()
        if num_threads:
            opts.intra_op_num_threads = num_threads
        providers = select_providers(device)

        def _open(name: str) -> ort.InferenceSession:
            return ort.InferenceSession(str(onnx_dir / name), sess_options=opts, providers=providers)

        return cls(
            duration_predictor=_open("duration_predictor.onnx"),
            text_encoder=_open("text_encoder.onnx"),
            vector_estimator=_open("vector_estimator.onnx"),
            vocoder=_open("vocoder.onnx"),
        )

    @property
    def active_provider(self) -> str:
        return self.vector_estimator.get_providers()[0]
