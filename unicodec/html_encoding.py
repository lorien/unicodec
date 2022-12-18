"""Functions to detect HTML document encoding declared in the document itself.

References:
- https://html.spec.whatwg.org/multipage/parsing.html
- https://www.w3.org/International/questions/qa-html-encoding-declarations
"""
from __future__ import annotations

import re
from re import Match

__all__ = ["detect_html_encoding"]

RE_HTML_XML_ENCODING = re.compile(
    r"<meta \s+ (?:"
    r"  charset \s* = \s* ['\"]? (?P<meta_charset>[^'\"\s>]+)"
    r"  |"
    r"  [^>]* http-equiv \s* = \s* ['\"]? content-type ['\"]?"
    r"    [^>]+ content \s* = \s* ['\"]? [^'\"\s>]+"
    r"    ; \s* charset=(?P<http_equiv1>[^'\"\s>]+)"
    r"  |"
    r"  [^>]* content \s* = \s* ['\"]? [^'\"\s>]+ "
    r"    ; \s* charset=(?P<http_equiv2>[^'\"\s>]+)"
    r"    [^>]+ http-equiv \s* = \s* ['\"]? content-type ['\"]?"
    r")"
    r"|"
    r"<\?xml \s+ [^>]* encoding \s* = \s* ['\"] (?P<xml>[^'\"\s>]+)",
    re.X | re.I,
)
RE_BYTES_HTML_XML_ENCODING = re.compile(
    RE_HTML_XML_ENCODING.pattern.encode(), re.X | re.I
)


def detect_html_encoding(data: bytes | str) -> None | str:
    match: None | Match[str] | Match[bytes]
    match = (
        RE_BYTES_HTML_XML_ENCODING.search(data)
        if isinstance(data, bytes)
        else RE_HTML_XML_ENCODING.search(data)
    )
    if match:
        enc = (
            match.group("meta_charset")
            or match.group("http_equiv1")
            or match.group("http_equiv2")
            or match.group("xml")
        )
        return enc.decode("latin-1") if isinstance(enc, bytes) else enc
    return None
