from __future__ import annotations

import codecs

# Order does matter here. UTF-32 BOMs must be preceed UTF-16 BOMs.
BOM_ENCODING = {
    codecs.BOM_UTF32_BE: "utf-32-be",
    codecs.BOM_UTF32_LE: "utf-32-le",
    codecs.BOM_UTF16_BE: "utf-16-be",
    codecs.BOM_UTF16_LE: "utf-16-le",
    codecs.BOM_UTF8: "utf-8",
}


def find_bom(data: bytes) -> None | bytes:
    """Search for bom, return found bom and corresponding encoding."""
    # Reference: https://encoding.spec.whatwg.org/#bom-sniff
    for bom_bytes in BOM_ENCODING:
        if data.startswith(bom_bytes):
            return bom_bytes
    return None


def detect_bom_encoding(data: bytes) -> None | str:
    bom = find_bom(data)
    return BOM_ENCODING[bom] if bom else None


def detect_content_encoding(data: bytes) -> str:
    bom_encoding = detect_bom_encoding(data)
    if bom_encoding:
        return bom_encoding
    return "utf-8"
