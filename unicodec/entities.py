__all__ = ["decode_entities"]

try:
    from html import unescape
except ImportError:
    from HTMLParser import HTMLParser

    html_parser = HTMLParser()
    unescape = html_parser.unescape


def decode_entities(inp):
    # type: (str) -> str
    return unescape(inp)
