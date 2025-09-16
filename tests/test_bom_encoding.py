# coding: utf-8
import codecs

from unicodec.bom_encoding import find_bom_encoding


def test_bom_preservation_while_decoding():
    # type: () -> None
    # fmt: off
    msg = codecs.BOM_UTF8 + u"привет".encode("utf-8")
    assert msg.decode("utf-8") == codecs.BOM_UTF8.decode("utf-8") + u"привет"
    # fmt: on


def test_find_bom_encoding_empty_data():
    # type: () -> None
    assert find_bom_encoding(b"") is None


def test_find_bom_encoding_nonbom_data():
    # type: () -> None
    assert find_bom_encoding(b"asdf") is None


def test_find_bom_encoding_utf8_bom():
    # type: () -> None
    assert find_bom_encoding(codecs.BOM_UTF8 + b"asdf") == "utf-8"


def test_find_bom_encoding_utf16_be_bom():
    # type: () -> None
    assert find_bom_encoding(codecs.BOM_UTF16_BE + b"asdf") == "utf-16-be"


def test_find_bom_encoding_utf32_le_bom():
    # type: () -> None
    assert find_bom_encoding(codecs.BOM_UTF32_LE + b"asdf") == "utf-32-le"
