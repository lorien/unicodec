"""Functions to detect XML document encoding declared in the document itself."""
from __future__ import annotations

import re
from contextlib import suppress
from re import Match

from .errors import InvalidEncodingName
from .normalization import normalize_encoding_name

__all__ = ["detect_xml_encoding"]

RE_XML_ENCODING = re.compile(
    r"<\?xml \s+ [^>]* encoding \s* = \s* ['\"] (?P<xml_prolog>[-_a-z-0-9]+)",
    re.X | re.I,
)
RE_BYTES_XML_ENCODING = re.compile(RE_XML_ENCODING.pattern.encode(), re.X | re.I)


def detect_xml_encoding(data: bytes | str) -> None | str:
    match: None | Match[str] | Match[bytes]
    match = (
        RE_BYTES_XML_ENCODING.search(data)
        if isinstance(data, bytes)
        else RE_XML_ENCODING.search(data)
    )
    if match:
        enc = match.group("xml_prolog")
        with suppress(InvalidEncodingName):
            return normalize_encoding_name(
                enc.decode("latin-1") if isinstance(enc, bytes) else enc
            )
    return None
