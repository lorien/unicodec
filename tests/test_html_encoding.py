import pytest

from unicodec.html_encoding import detect_html_encoding

from .util import add_encoded_duplicates


def test_detect_html_encoding_empty_bytes():
    # type: () -> None
    assert detect_html_encoding(b"") is None


def test_detect_html_encoding_empty_str():
    # type: () -> None
    assert detect_html_encoding("") is None


@pytest.mark.parametrize(
    "data",
    add_encoded_duplicates(
        [
            '<meta charset="windows-1251">',
            "<meta charset='windows-1251'>",
            "<meta charset=windows-1251>",
        ]
    ),
)
def test_detect_html_encoding_meta_charset(data):
    # type: (str|bytes) -> None
    assert detect_html_encoding(data) == "windows-1251"


@pytest.mark.parametrize(
    "data",
    add_encoded_duplicates(
        [
            '<meta http-equiv="content-type" content="text/html'
            '; charset=windows-1251">',
            "<meta http-equiv='content-type' content='text/html"
            "; charset=windows-1251'>",
            "<meta http-equiv=content-type content=text/html; charset=windows-1251>",
        ]
    ),
)
def test_detect_html_encoding_http_equiv(data):
    # type: (str|bytes) -> None
    assert detect_html_encoding(data) == "windows-1251"


@pytest.mark.parametrize(
    "data",
    add_encoded_duplicates(
        [
            '<meta content="text/html; charset=windows-1251"'
            ' http-equiv="content-type">',
            "<meta content='text/html; charset=windows-1251'"
            " http-equiv='content-type'>",
            "<meta content=text/html; charset=windows-1251 http-equiv=content-type>",
        ]
    ),
)
def test_detect_html_encoding_http_equiv_reversed(data):
    # type: (str|bytes) -> None
    assert detect_html_encoding(data) == "windows-1251"


@pytest.mark.parametrize(
    "data",
    add_encoded_duplicates(
        [
            '<?xml encoding="windows-1251">',
            "<?xml encoding='windows-1251'>",
        ]
    ),
)
def test_detect_html_encoding_xml(data):
    # type: (str|bytes) -> None
    assert detect_html_encoding(data) == "windows-1251"


@pytest.mark.parametrize(
    "data",
    add_encoded_duplicates(
        [
            '<meta content="text/html; charset=WINDOWS-1251"'
            ' http-equiv="content-type">',
            '<meta http-equiv="content-type" content="text/html;'
            ' charset=WINDOWS-1251">',
            '<meta charset="WINDOWS-1251">',
        ]
    ),
)
def test_detect_html_encoding_upper_case(data):
    # type: (str|bytes) -> None
    assert detect_html_encoding(data) == "windows-1251"


def test_detect_html_encoding_http_equiv_multiple_tokens():
    # type: () -> None
    assert (
        detect_html_encoding(
            '<meta http-equiv="content-type" content="text/html'
            '; charset=windows-1251;charset=windows-1251">'
        )
        == "windows-1251"
    )


def test_detect_html_encoding_http_equiv_nospace():
    # type: () -> None
    assert (
        detect_html_encoding(
            '<meta http-equiv="content-type" content="text/html;charset=windows-1251">'
        )
        == "windows-1251"
    )
