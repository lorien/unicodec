from __future__ import annotations

from unicodec import decode_content


def test_basic_usage() -> None:
    assert decode_content(b"asdf") == "asdf"


def test_input_bytess() -> None:
    assert decode_content("крокодил".encode()) == "крокодил"


def test_input_str() -> None:
    assert decode_content("крокодил") == "крокодил"


def test_arg_decode_entities_default() -> None:
    assert decode_content("&copy;") == "©"


def test_arg_decode_entities_false() -> None:
    assert decode_content("&copy;", decode_entities=False) == "&copy;"


def test_arg_remove_null_bytes_default() -> None:
    assert decode_content("as\x00df") == "asdf"


def test_arg_remove_null_bytes_false() -> None:
    assert decode_content("as\x00df", remove_null_bytes=False) == "as\x00df"


def test_arg_encoding_default() -> None:
    assert decode_content("крокодил".encode()) == "крокодил"


def test_arg_encoding_explicit() -> None:
    assert decode_content("крокодил".encode("cp1251"), encoding="cp1251") == "крокодил"
