__all__ = ["decode_entities"]

try:
    from html import unescape
except ImportError:
    from six.moves.html_parser import HTMLParser

    html_parser = HTMLParser()
    # pylint: disable=no-member
    unescape = html_parser.unescape  # type: ignore[attr-defined]


def decode_entities(inp):
    # type: (str) -> str
    return unescape(inp)
