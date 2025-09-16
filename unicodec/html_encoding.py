"""Functions to detect HTML document encoding declared in the document itself."""

# References:
# - https://html.spec.whatwg.org/multipage/parsing.html
# - https://www.w3.org/International/questions/qa-html-encoding-declarations

import re

try:
    from re import Match  # pylint: disable=unused-import
except ImportError:
    pass

from .errors import InvalidEncodingNameError
from .normalization import normalize_encoding_name

__all__ = ["detect_html_encoding"]

RE_HTML_ENCODING = re.compile(
    r"<meta \s+ (?:"
    r"  charset \s* = \s* ['\"]? (?P<meta_charset>[-_a-z0-9]+)"
    r"  |"
    r"  [^>]* http-equiv \s* = \s* ['\"]? content-type ['\"]?"
    r"    [^>]+ content \s* = \s* ['\"]? [^'\"\s>]+"
    r"    ; \s* charset=(?P<http_equiv1>[-_a-z0-9]+)"
    r"  |"
    r"  [^>]* content \s* = \s* ['\"]? [^'\"\s>]+ "
    r"    ; \s* charset=(?P<http_equiv2>[-_a-z0-9]+)"
    r"    [^>]+ http-equiv \s* = \s* ['\"]? content-type ['\"]?"
    r")"
    r"|"
    r"<\?xml \s+ [^>]* encoding \s* = \s* ['\"] (?P<xml_prolog>[-_a-z-0-9]+)",
    re.VERBOSE | re.IGNORECASE,
)
RE_BYTES_HTML_ENCODING = re.compile(
    RE_HTML_ENCODING.pattern.encode(), re.VERBOSE | re.IGNORECASE
)


def detect_html_encoding(data):
    # type: (bytes | str) -> None | str
    match = (
        RE_BYTES_HTML_ENCODING.search(data)
        if isinstance(data, bytes)
        else RE_HTML_ENCODING.search(data)
    )
    if match:
        enc = (
            match.group("meta_charset")
            or match.group("http_equiv1")
            or match.group("http_equiv2")
            or match.group("xml_prolog")
        )
        # pylint: disable=duplicate-code
        try:
            return normalize_encoding_name(
                enc.decode("latin-1") if isinstance(enc, bytes) else enc
            )
        except InvalidEncodingNameError:
            pass
    return None
