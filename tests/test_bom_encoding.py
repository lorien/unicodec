# coding: utf-8
import codecs

from unicodec.bom_encoding import BOM_ENCODINGS, find_bom_encoding
from unicodec.main import decode_content


def test_decode_utf8_preserves_bom():  # type: () -> None
    # fmt: off
    msg = codecs.BOM_UTF8 + u"привет".encode("utf-8")
    assert msg.decode("utf-8") == codecs.BOM_UTF8.decode("utf-8") + u"привет"
    # fmt: on


def test_find_bom_encoding_empty_data():  # type: () -> None
    assert find_bom_encoding(b"") == (None, None)


def test_find_bom_encoding_nonbom_data():  # type: () -> None
    assert find_bom_encoding(b"asdf") == (None, None)


def test_find_bom_encoding_utf8_bom():  # type: () -> None
    assert find_bom_encoding(codecs.BOM_UTF8 + b"asdf") == (codecs.BOM_UTF8, "utf-8")


def test_find_bom_encoding_utf16_be_bom():  # type: () -> None
    assert find_bom_encoding(codecs.BOM_UTF16_BE + b"asdf") == (
        codecs.BOM_UTF16_BE,
        "utf-16-be",
    )


def test_find_bom_encoding_utf32_le_bom():  # type: () -> None
    assert find_bom_encoding(codecs.BOM_UTF32_LE + b"asdf") == (
        codecs.BOM_UTF32_LE,
        "utf-32-le",
    )


def test_bom_is_stripped():  # type: () -> None
    # fmt: off
    msg = u"жук"
    # fmt: on
    for bom, enc in BOM_ENCODINGS:
        msg_enc = bom + msg.encode(enc)
        msg_dec = decode_content(msg_enc)
        assert msg_dec == msg
