"""Functions to decode HTML bytes content into unicode string.

References:
- https://html.spec.whatwg.org/multipage/parsing.html
"""
from __future__ import annotations

from contextlib import suppress

from . import entities
from .bom_encoding import detect_bom_encoding
from .errors import InvalidEncodingName
from .html_encoding import detect_html_encoding
from .http_encoding import parse_content_type_header_encoding
from .normalization import normalize_encoding_name

__all__ = ["decode_content", "detect_content_encoding"]


def detect_content_encoding(data: bytes, content_type_header: None | str = None) -> str:
    enc = detect_bom_encoding(data)
    if enc:
        with suppress(InvalidEncodingName):
            return normalize_encoding_name(enc)
    if content_type_header:
        enc = parse_content_type_header_encoding(content_type_header)
        if enc:
            with suppress(InvalidEncodingName):
                return normalize_encoding_name(enc)
    enc = detect_html_encoding(data)
    if enc:
        with suppress(InvalidEncodingName):
            return normalize_encoding_name(enc)
    return "utf-8"


def decode_content(
    data: bytes | str,
    decode_entities: bool = True,
    remove_null_bytes: bool = True,
    encoding: None | str = None,
    content_type_header: None | str = None,
) -> str:
    if isinstance(data, bytes):
        if encoding is None:
            encoding = detect_content_encoding(data, content_type_header)
        data = data.decode(encoding)
    if remove_null_bytes:
        data = data.replace("\x00", "")
    if decode_entities:
        data = entities.decode_entities(data)
    return data  # noqa: R504 unnecessary variable assignment
