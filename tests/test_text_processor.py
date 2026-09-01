from unicodedata import normalize

import numpy as np
import pytest

from korvatts.text_processor import TextProcessor, chunk_text, length_to_mask, normalize_text


def test_normalize_wraps_lang_tags_and_adds_period():
    out = normalize_text("Xin chào", "vi")
    assert out == normalize("NFKD", "<vi>Xin chào.</vi>")
    assert out != "<vi>Xin chào.</vi>"  # diacritics are decomposed for the indexer


def test_normalize_keeps_existing_punctuation():
    assert normalize_text("Hello!", "en") == "<en>Hello!</en>"


def test_normalize_strips_emoji_and_collapses_spaces():
    out = normalize_text("Hi  😀  there ,ok", "en")
    assert out == "<en>Hi there,ok.</en>"


def test_normalize_rejects_unknown_lang():
    with pytest.raises(ValueError):
        normalize_text("x", "xx")


def test_chunk_text_respects_max_len():
    text = "Câu một. Câu hai. Câu ba. " * 20
    chunks = chunk_text(text, max_len=60)
    assert len(chunks) > 1
    assert all(len(c) <= 60 for c in chunks)
    assert " ".join(chunks) == text.strip()


def test_chunk_text_keeps_abbreviations_together():
    assert chunk_text("Dr. Smith arrived. He left.", max_len=100) == ["Dr. Smith arrived. He left."]


def test_length_to_mask_shape_and_values():
    mask = length_to_mask(np.array([2, 4]))
    assert mask.shape == (2, 1, 4)
    assert mask[0, 0].tolist() == [1, 1, 0, 0]
    assert mask[1, 0].tolist() == [1, 1, 1, 1]


def test_text_processor_encodes_batch(indexer_path):
    proc = TextProcessor(indexer_path)
    ids, mask = proc.encode(["Xin chào", "Hello world"], ["vi", "en"])
    assert ids.shape[0] == 2 and ids.dtype == np.int64
    assert mask.shape == (2, 1, ids.shape[1])
    assert (ids[mask[:, 0] == 0] == 0).all()  # padded positions are zero


def test_text_processor_drops_unknown_codepoints(indexer_path):
    proc = TextProcessor(indexer_path)
    plain, _ = proc.encode(["ab"], ["en"])
    # U+20000 is an astral CJK ideograph (outside the 65536-entry table, not an emoji).
    with_unknown, _ = proc.encode(["a\U00020000b"], ["en"])
    assert with_unknown.shape == plain.shape
    assert (with_unknown == plain).all()
    assert (with_unknown >= 0).all()


def test_chunk_text_splits_overlong_sentence_on_whitespace():
    sentence = " ".join(["từ"] * 200)  # ~800 chars, no terminal punctuation
    chunks = chunk_text(sentence, max_len=100)
    assert len(chunks) >= len(sentence) // 100
    assert all(len(c) <= 100 for c in chunks)
    assert " ".join(chunks) == sentence


def test_chunk_text_hard_cuts_single_overlong_token():
    token = "x" * 250
    chunks = chunk_text(token, max_len=100)
    assert [len(c) for c in chunks] == [100, 100, 50]
