import codecs

__all__ = ["detect_bom_encoding", "find_bom"]

# Order does matter here. UTF-32 BOMs must be preceed UTF-16 BOMs.
BOM_ENCODINGS = [
    (codecs.BOM_UTF32_BE, "utf-32-be"),
    (codecs.BOM_UTF32_LE, "utf-32-le"),
    (codecs.BOM_UTF16_BE, "utf-16-be"),
    (codecs.BOM_UTF16_LE, "utf-16-le"),
    (codecs.BOM_UTF8, "utf-8"),
]


def find_bom_encoding(data):
    # type: (bytes) -> None | str
    """Search for BOM signature and return encoding which uses such bom.

    Return None if BOM signature not found.
    """
    # Reference: https://encoding.spec.whatwg.org/#bom-sniff
    for bom_bytes, enc in BOM_ENCODINGS:
        if data.startswith(bom_bytes):
            return enc
    return None
