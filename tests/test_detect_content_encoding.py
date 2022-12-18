from __future__ import annotations

import codecs

from unicodec.util import detect_content_encoding


def test_detect_content_encoding_empty_data() -> None:
    assert detect_content_encoding(b"") == "utf-8"


def test_detect_content_encoding_basic_data() -> None:
    assert detect_content_encoding(b"asdf") == "utf-8"


def test_detect_content_encoding_bom_data() -> None:
    assert detect_content_encoding(codecs.BOM_UTF16_LE + b"asdf") == "utf-16-le"


def test_detect_content_encoding_bom_meta_charset() -> None:
    assert (
        detect_content_encoding(codecs.BOM_UTF16_LE + b'<meta charset="cp1251">')
        == "utf-16-le"
    )


def test_detect_content_encoding_meta_charset() -> None:
    assert detect_content_encoding(b'<meta charset="cp1251">') == "cp1251"


def test_detect_content_encoding_http_equiv_charset() -> None:
    assert (
        detect_content_encoding(
            b'<meta http-equiv="content-type" content="text/html; charset=cp1251">'
        )
        == "cp1251"
    )
