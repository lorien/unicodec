from __future__ import annotations

import pytest

from unicodec.http_encoding import parse_content_type_header_encoding


@pytest.mark.parametrize(
    "header,encoding",
    [
        ("", None),
        ("zzzzzz; charset=windows-1252", "windows-1252"),
        ('zzzzzz; charset="utf-8"', "utf-8"),
        ('charset="utf-8"', "utf-8"),
    ],
)
def test_parse_content_type_header_encoding(header: str, encoding: None | str) -> None:
    assert parse_content_type_header_encoding(header) == encoding
