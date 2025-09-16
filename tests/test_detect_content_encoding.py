import codecs

from unicodec import detect_content_encoding


def test_detect_content_encoding_empty_data():
    # type: () -> None
    assert detect_content_encoding(b"") == "utf-8"


def test_detect_content_encoding_basic_data():
    # type: () -> None
    assert detect_content_encoding(b"asdf") == "utf-8"


def test_detect_content_encoding_bom_data():
    # type: () -> None
    assert detect_content_encoding(codecs.BOM_UTF16_LE + b"asdf") == "utf-16-le"


def test_detect_content_encoding_meta_charset():
    # type: () -> None
    assert detect_content_encoding(b'<meta charset="windows-1251">') == "windows-1251"


def test_detect_content_encoding_http_equiv_charset():
    # type: () -> None
    assert (
        detect_content_encoding(
            b'<meta http-equiv="content-type" content="text/html'
            b'; charset=windows-1251">'
        )
        == "windows-1251"
    )


def test_detect_content_encoding_bom_and_html():
    # type: () -> None
    assert (
        detect_content_encoding(codecs.BOM_UTF16_LE + b'<meta charset="windows-1251">')
        == "utf-16-le"
    )


def test_detect_content_encoding_http_and_html():
    # type: () -> None
    assert (
        detect_content_encoding(
            b'<meta charset="windows-1251">', content_type_header="charset=utf-8"
        )
        == "utf-8"
    )


def test_detect_content_encoding_bom_and_http_and_html():
    # type: () -> None
    assert (
        detect_content_encoding(
            codecs.BOM_UTF16_LE + b'<meta charset="windows-1251">',
            content_type_header="charset=windows-1252",
        )
        == "utf-16-le"
    )
