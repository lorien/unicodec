"""Functions to decode HTML bytes content into unicode string."""
# References:
# - https://html.spec.whatwg.org/multipage/parsing.html
from typing import Literal

from . import entities
from .bom_encoding import BOM_UNICODE, find_bom_encoding
from .errors import InvalidEncodingNameError
from .html_encoding import detect_html_encoding
from .http_encoding import parse_content_type_header_encoding
from .normalization import normalize_encoding_name
from .xml_encoding import detect_xml_encoding

__all__ = ["decode_content", "detect_content_encoding"]


def detect_content_encoding(
    data,  # type: bytes
    content_type_header=None,  # type: None | str
    markup="html",  # type: Literal["html", "xml"]
):
    # type: (...) -> str
    _, enc = find_bom_encoding(data)
    if enc:
        try:
            return normalize_encoding_name(enc)
        except InvalidEncodingNameError:
            pass
    if content_type_header:
        enc = parse_content_type_header_encoding(content_type_header)
        if enc:
            try:
                return normalize_encoding_name(enc)
            except InvalidEncodingNameError:
                pass
    enc = detect_html_encoding(data) if markup == "html" else detect_xml_encoding(data)
    if enc:
        try:
            return normalize_encoding_name(enc)
        except InvalidEncodingNameError:
            pass
    return "utf-8"


def decode_content(  # pylint: disable=R0917
    data,  # type: bytes | str
    decode_entities=True,  # type: bool
    remove_null_bytes=True,  # type: bool
    encoding=None,  # type: None | str
    content_type_header=None,  # type: None | str
    markup="html",  # type: Literal["html", "xml"]
    errors="strict",  # type: Literal["strict", "ignore", "replace"]
):
    # type: (...) -> str
    if isinstance(data, bytes):
        if encoding is None:
            encoding = detect_content_encoding(
                data, content_type_header=content_type_header, markup=markup
            )
        data = data.decode(encoding, errors=errors)
    # Remove BOM, it might be at the start of decoded unicode text
    if data.startswith(BOM_UNICODE):
        data = data[len(BOM_UNICODE) :]
    if remove_null_bytes:
        data = data.replace("\x00", "")
    if decode_entities:
        data = entities.decode_entities(data)
    return data  # noqa: RET504 unnecessary variable assignment
