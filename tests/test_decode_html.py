from unicodec import decode_html


def test_basic_usage() -> None:
    assert decode_html(b"asdf") == "asdf"


def test_input_bytess() -> None:
    assert decode_html("крокодил".encode()) == "крокодил"


def test_input_str() -> None:
    assert decode_html("крокодил") == "крокодил"


def test_arg_decode_entities_default() -> None:
    assert decode_html("&copy;") == "©"


def test_arg_decode_entities_false() -> None:
    assert decode_html("&copy;", decode_entities=False) == "&copy;"


def test_arg_remove_null_bytes_default() -> None:
    assert decode_html("as\x00df") == "asdf"


def test_arg_remove_null_bytes_false() -> None:
    assert decode_html("as\x00df", remove_null_bytes=False) == "as\x00df"
