# coding: utf-8
from unicodec.entities import decode_entities


def test_decode_numeric_entities():  # type: () -> None
    # fmt: off
    assert decode_entities("asdf &#1046;") == u"asdf Ж"
    # fmt: on


# def test_decode_invalid_numeric_entities(): # type: () -> None
#    # fmt: off
#    assert decode_entities("asdf &#99999999;") == u"asdf �"
#    # fmt: on


def test_decode_multiple_named_entities():  # type: () -> None
    # fmt: off
    assert decode_entities("&copy; asdf &copy;") == u"© asdf ©"
    # fmt: on


def test_decode_mixed_valid_invalid_named_entities():  # type: () -> None
    # fmt: off
    assert decode_entities("&zz; asdf &copy;") == u"&zz; asdf ©"
    # fmt: on


def test_control_entity_decimal():  # type: () -> None
    # fmt: off
    assert decode_entities("&#128;") == u"€"
    # fmt: on


def test_control_entity_hex():  # type: () -> None
    # fmt: off
    assert decode_entities("&#x80;") == u"€"
    # fmt: on


def test_control_entity_not_mapped_decimal():  # type: () -> None
    # fmt: off
    assert decode_entities("&#129;") == u"\x81"
    # fmt: on


def test_control_entity_not_mapped_hex():  # type: () -> None
    # fmt: off
    assert decode_entities("&#x81;") == u"\x81"
    # fmt: on
