from __future__ import annotations

import codecs

from unicodec.encoding import detect_bom_encoding


def test_bom_preservation_while_decoding() -> None:
    assert (codecs.BOM_UTF8 + "привет".encode("utf-8")).decode(
        "utf-8"
    ) == codecs.BOM_UTF8.decode("utf-8") + "привет"


def test_detect_bom_encoding_empty_data() -> None:
    assert detect_bom_encoding(b"") is None


def test_detect_bom_encoding_nonbom_data() -> None:
    assert detect_bom_encoding(b"asdf") is None


def test_detect_bom_encoding_utf8_bom() -> None:
    assert detect_bom_encoding(codecs.BOM_UTF8 + b"asdf") == "utf-8"


def test_detect_bom_encoding_utf16_be_bom() -> None:
    assert detect_bom_encoding(codecs.BOM_UTF16_BE + b"asdf") == "utf-16-be"


def test_detect_bom_encoding_utf32_le_bom() -> None:
    assert detect_bom_encoding(codecs.BOM_UTF32_LE + b"asdf") == "utf-32-le"
