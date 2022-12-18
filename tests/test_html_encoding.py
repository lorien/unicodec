import pytest

from unicodec.html_encoding import detect_html_encoding


def extend_with_bytes(items: list[str]) -> list[str | bytes]:
    return items + [x.encode() for x in items]


def test_detect_html_encoding_empty_bytes() -> None:
    assert detect_html_encoding(b"") is None


def test_detect_html_encoding_empty_str() -> None:
    assert detect_html_encoding("") is None


@pytest.mark.parametrize(
    "data",
    extend_with_bytes(
        [
            '<meta charset="cp1251">',
            "<meta charset='cp1251'>",
            "<meta charset=cp1251>",
        ]
    ),
)
def test_detect_html_encoding_meta_charset(data: str | bytes) -> None:
    assert detect_html_encoding(data) == "cp1251"


@pytest.mark.parametrize(
    "data",
    extend_with_bytes(
        [
            '<meta http-equiv="content-type" content="text/html; charset=cp1251">',
            "<meta http-equiv='content-type' content='text/html; charset=cp1251'>",
            "<meta http-equiv=content-type content=text/html; charset=cp1251>",
        ]
    ),
)
def test_detect_html_encoding_http_equiv(data: str | bytes) -> None:
    assert detect_html_encoding(data) == "cp1251"


@pytest.mark.parametrize(
    "data",
    extend_with_bytes(
        [
            '<meta content="text/html; charset=cp1251" http-equiv="content-type">',
            "<meta content='text/html; charset=cp1251' http-equiv='content-type'>",
            "<meta content=text/html; charset=cp1251 http-equiv=content-type>",
        ]
    ),
)
def test_detect_html_encoding_http_equiv_reversed(data: bytes | str) -> None:
    assert detect_html_encoding(data) == "cp1251"


@pytest.mark.parametrize(
    "data",
    extend_with_bytes(
        [
            '<?xml encoding="cp1251">',
            "<?xml encoding='cp1251'>",
        ]
    ),
)
def test_detect_html_encoding_xml(data: bytes | str) -> None:
    assert detect_html_encoding(data) == "cp1251"
