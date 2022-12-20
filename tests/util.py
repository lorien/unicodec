from __future__ import annotations


def extend_with_bytes(items: list[str]) -> list[str | bytes]:
    return items + [x.encode() for x in items]
