"""Functions to decode HTML bytes content into unicode string.

References:
- https://html.spec.whatwg.org/multipage/parsing.html
"""
from __future__ import annotations

from . import entities
from .encoding import detect_content_encoding

__all__ = ["decode_content"]


def decode_content(
    data: bytes | str,
    decode_entities: bool = True,
    remove_null_bytes: bool = True,
    encoding: None | str = None,
) -> str:
    if isinstance(data, bytes):
        if encoding is None:
            encoding = detect_content_encoding(data)
        data = data.decode(encoding)
    if remove_null_bytes:
        data = data.replace("\x00", "")
    if decode_entities:
        data = entities.decode_entities(data)
    return data  # noqa: R504 unnecessary variable assignment
