"""Text normalization and character-to-id encoding.

The model consumes raw Unicode code points mapped through ``unicode_indexer.json``.
The indexer was built on NFKD-decomposed text, so Vietnamese diacritics are split into
base letter + combining marks before lookup. Do not change the normalization form
without retraining the text encoder.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from unicodedata import normalize

import numpy as np

# Language tags accepted by the text encoder. "na" = language-agnostic.
AVAILABLE_LANGS = [
    "en", "ko", "ja", "ar", "bg", "cs", "da", "de", "el", "es", "et", "fi", "fr", "hi",
    "hr", "hu", "id", "it", "lt", "lv", "nl", "pl", "pt", "ro", "ru", "sk", "sl", "sv",
    "tr", "uk", "vi", "na",
]

_EMOJI_RE = re.compile(
    "[\U0001f600-\U0001f64f\U0001f300-\U0001f5ff\U0001f680-\U0001f6ff\U0001f700-\U0001f77f"
    "\U0001f780-\U0001f7ff\U0001f800-\U0001f8ff\U0001f900-\U0001f9ff\U0001fa00-\U0001fa6f"
    "\U0001fa70-\U0001faff☀-⛿✀-➿\U0001f1e6-\U0001f1ff]+",
    flags=re.UNICODE,
)

_CHAR_REPLACEMENTS = {
    "–": "-", "‑": "-", "—": "-", "_": " ",
    "“": '"', "”": '"', "‘": "'", "’": "'", "´": "'", "`": "'",
    "[": " ", "]": " ", "|": " ", "/": " ", "#": " ", "→": " ", "←": " ",
}

_EXPR_REPLACEMENTS = {"@": " at ", "e.g.,": "for example, ", "i.e.,": "that is, "}

_TRAILING_PUNCT_RE = re.compile(r"[.!?;:,'\"')\]}…。」』】〉》›»]$")

# Sentence boundary: punctuation + whitespace, excluding common abbreviations / initials.
_SENTENCE_SPLIT_RE = re.compile(
    r"(?<!Mr\.)(?<!Mrs\.)(?<!Ms\.)(?<!Dr\.)(?<!Prof\.)(?<!Sr\.)(?<!Jr\.)(?<!Ph\.D\.)"
    r"(?<!etc\.)(?<!e\.g\.)(?<!i\.e\.)(?<!vs\.)(?<!Inc\.)(?<!Ltd\.)(?<!Co\.)(?<!Corp\.)"
    r"(?<!St\.)(?<!Ave\.)(?<!Blvd\.)(?<!\b[A-Z]\.)(?<=[.!?])\s+"
)


def normalize_text(text: str, lang: str) -> str:
    """Clean raw text and wrap it in language tags expected by the text encoder."""
    if lang not in AVAILABLE_LANGS:
        raise ValueError(f"Unsupported language '{lang}'. Choose one of {AVAILABLE_LANGS}")

    text = normalize("NFKD", text)
    text = _EMOJI_RE.sub("", text)
    for src, dst in _CHAR_REPLACEMENTS.items():
        text = text.replace(src, dst)
    text = re.sub(r"[♥☆♡©\\]", "", text)
    for src, dst in _EXPR_REPLACEMENTS.items():
        text = text.replace(src, dst)

    # Tighten spacing before punctuation and collapse repeated quotes.
    text = re.sub(r" ([,.!?;:'])", r"\1", text)
    for dup in ('""', "''", "``"):
        while dup in text:
            text = text.replace(dup, dup[0])
    text = re.sub(r"\s+", " ", text).strip()

    if text and not _TRAILING_PUNCT_RE.search(text):
        text += "."
    return f"<{lang}>{text}</{lang}>"


def chunk_text(text: str, max_len: int = 300) -> list[str]:
    """Split long text into sentence-aligned chunks no longer than ``max_len`` chars.

    Sentences longer than ``max_len`` are split further on whitespace so the model never sees
    an out-of-distribution input length.
    """
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n+", text.strip()) if p.strip()]
    chunks: list[str] = []
    for paragraph in paragraphs:
        current = ""
        for sentence in _SENTENCE_SPLIT_RE.split(paragraph):
            for piece in _split_long_sentence(sentence, max_len):
                if len(current) + len(piece) + 1 <= max_len:
                    current += (" " if current else "") + piece
                else:
                    if current:
                        chunks.append(current.strip())
                    current = piece
        if current:
            chunks.append(current.strip())
    return chunks


def _split_long_sentence(sentence: str, max_len: int) -> list[str]:
    if len(sentence) <= max_len:
        return [sentence]
    pieces, current = [], ""
    for word in sentence.split():
        if current and len(current) + len(word) + 1 > max_len:
            pieces.append(current)
            current = word
        else:
            current += (" " if current else "") + word
    if current:
        pieces.append(current)
    # A single "word" longer than max_len (e.g. a URL) is hard-cut.
    return [p[i : i + max_len] for p in pieces for i in range(0, len(p), max_len)]


def length_to_mask(lengths: np.ndarray, max_len: int | None = None) -> np.ndarray:
    """Convert (B,) lengths to a float mask of shape (B, 1, max_len)."""
    max_len = max_len or int(lengths.max())
    ids = np.arange(max_len)
    mask = (ids < np.expand_dims(lengths, axis=1)).astype(np.float32)
    return mask.reshape(-1, 1, max_len)


class TextProcessor:
    """Turns a batch of (text, lang) pairs into padded ``text_ids`` + ``text_mask``."""

    def __init__(self, unicode_indexer_path: str | Path):
        with open(unicode_indexer_path, "r", encoding="utf-8") as f:
            self.indexer: list[int] = json.load(f)

    def encode(self, texts: list[str], langs: list[str]) -> tuple[np.ndarray, np.ndarray]:
        if len(texts) != len(langs):
            raise ValueError("texts and langs must have the same length")
        id_lists = [self._ids_for(normalize_text(t, lang)) for t, lang in zip(texts, langs)]
        lengths = np.array([len(ids) for ids in id_lists], dtype=np.int64)
        text_ids = np.zeros((len(id_lists), int(lengths.max())), dtype=np.int64)
        for i, ids in enumerate(id_lists):
            text_ids[i, : len(ids)] = ids
        return text_ids, length_to_mask(lengths)

    def _ids_for(self, text: str) -> list[int]:
        """Map characters to ids, silently dropping any the vocabulary does not cover.

        The table marks unknown code points with -1 and only spans the BMP (65536 entries);
        feeding -1 into the ONNX embedding gather would wrap to the last vocabulary row.
        """
        ids = []
        for ch in text:
            code = ord(ch)
            if code < len(self.indexer) and self.indexer[code] >= 0:
                ids.append(int(self.indexer[code]))
        return ids
