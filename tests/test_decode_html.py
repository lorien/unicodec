# coding: utf-8
from unicodec import decode_content


def test_basic_usage():
    # type: () -> None
    assert decode_content(b"asdf") == "asdf"


def test_input_bytess():
    # type: () -> None
    # fmt: off
    assert decode_content(u"крокодил".encode("utf-8")) == u"крокодил"
    # fmt: on


def test_input_str():
    # type: () -> None
    # fmt: off
    assert decode_content(u"крокодил") == u"крокодил"
    # fmt: on


def test_arg_decode_entities_default():
    # type: () -> None
    # fmt: off
    assert decode_content("&copy;") == u"©"
    # fmt: on


def test_arg_decode_entities_false():
    # type: () -> None
    assert decode_content("&copy;", decode_entities=False) == "&copy;"


def test_arg_remove_null_bytes_default():
    # type: () -> None
    assert decode_content("as\x00df") == "asdf"


def test_arg_remove_null_bytes_false():
    # type: () -> None
    assert decode_content("as\x00df", remove_null_bytes=False) == "as\x00df"


def test_arg_encoding_default():
    # type: () -> None
    # fmt: off
    assert decode_content(u"крокодил".encode("utf-8")) == u"крокодил"
    # fmt: on


def test_arg_encoding_explicit():
    # type: () -> None
    # fmt: off
    assert decode_content(u"крокодил".encode("cp1251"), encoding="cp1251") == (
        u"крокодил"
    )
    # fmt: on
