import pytest

from unicodec.xml_encoding import detect_xml_encoding

from .util import add_encoded_duplicates


def test_detect_xml_encoding_empty_bytes():
    # type: () -> None
    assert detect_xml_encoding(b"") is None


def test_detect_xml_encoding_empty_str():
    # type: () -> None
    assert detect_xml_encoding("") is None


@pytest.mark.parametrize(
    "data",
    add_encoded_duplicates(
        [
            '<meta charset="windows-1251">',
            "<meta charset='windows-1251'>",
            "<meta charset=windows-1251>",
            '<meta http-equiv="content-type" content="text/html'
            '; charset=windows-1251">',
            "<meta http-equiv='content-type' content='text/html"
            "; charset=windows-1251'>",
            "<meta http-equiv=content-type content=text/html; charset=windows-1251>",
            '<meta content="text/html; charset=windows-1251"'
            ' http-equiv="content-type">',
            "<meta content='text/html; charset=windows-1251'"
            " http-equiv='content-type'>",
            "<meta content=text/html; charset=windows-1251 http-equiv=content-type>",
        ]
    ),
)
def test_detect_xml_encoding_html_meta_tags(data):
    # type: (str | bytes) -> None
    assert detect_xml_encoding(data) is None


@pytest.mark.parametrize(
    "data",
    add_encoded_duplicates(
        [
            '<?xml encoding="windows-1251">',
            "<?xml encoding='windows-1251'>",
        ]
    ),
)
def test_detect_xml_encoding_xml(data):
    # type: (str | bytes) -> None
    assert detect_xml_encoding(data) == "windows-1251"
