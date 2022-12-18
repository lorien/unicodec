import html

__all__ = ["decode_entities"]


def decode_entities(inp: str) -> str:
    return html.unescape(inp)
