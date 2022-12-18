from __future__ import annotations

from . import entities

__all__ = ["decode_html"]


def decode_html(
    inp: bytes | str, decode_entities: bool = True, remove_null_bytes: bool = True
) -> str:
    if isinstance(inp, bytes):
        inp = inp.decode("utf-8")
    if remove_null_bytes:
        inp = inp.replace("\x00", "")
    if decode_entities:
        inp = entities.decode_entities(inp)
    return inp  # noqa: R504 unnecessary variable assignment
