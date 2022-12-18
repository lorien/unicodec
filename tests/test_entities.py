from unicodec.entities import decode_entities


def test_decode_numeric_entities() -> None:
    assert decode_entities("asdf &#1046;") == "asdf Ж"


def test_decode_invalid_numeric_entities() -> None:
    assert decode_entities("asdf &#99999999;") == "asdf �"


def test_decode_multiple_named_entities() -> None:
    assert decode_entities("&copy; asdf &copy;") == "© asdf ©"


def test_decode_mixed_valid_invalid_named_entities() -> None:
    assert decode_entities("&zz; asdf &copy;") == "&zz; asdf ©"
