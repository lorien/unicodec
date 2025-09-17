# References
#
# Control Code Entities (128-159 range):
# - http://i18nguy.com/markup/ncrs.html
import re

__all__ = ["decode_entities"]

RE_CONTROL_CODE_ENTITY = re.compile(r"&#(1[2345][0-9]|x[89][0-9a-f]);")
CONTROL_CODE_MIN = 128
CONTROL_CODE_MAX = 159
HTML_MODULE_AVAIL = False
# These codes are not to be changed
# - 129
# - 141
# - 143
# - 144
# - 157
CONTROL_CODE_REPLACE_MAP = {
    128: 8364,
    130: 8218,
    131: 402,
    132: 8222,
    133: 8230,
    134: 8224,
    135: 8225,
    136: 710,
    137: 8240,
    138: 352,
    139: 8249,
    140: 338,
    142: 381,
    145: 8216,
    146: 8217,
    147: 8220,
    148: 8221,
    149: 8226,
    150: 8211,
    151: 8212,
    152: 732,
    153: 8482,
    154: 353,
    155: 8250,
    156: 339,
    158: 382,
    159: 376,
}
try:
    # only needed for type checking
    from re import Match
except ImportError:
    pass
try:
    from html import unescape
except ImportError:
    from six.moves.html_parser import HTMLParser

    html_parser = HTMLParser()
    # pylint: disable=no-member
    unescape = html_parser.unescape  # type: ignore[attr-defined]
else:
    HTML_MODULE_AVAIL = True


def process_control_code_match(match):  # type: (Match[str]) -> str
    token = match.group(1)
    if token.startswith(("x", "X")):
        code = int(token[1:], 16)
        is_hex = True
    else:
        code = int(token)
        is_hex = False
    try:
        new_code = CONTROL_CODE_REPLACE_MAP[code]
    except KeyError:
        return "&#{};".format(token)
    return "&#x{:x};".format(new_code) if is_hex else "&#{};".format(new_code)


def fix_control_code_entities(data):  # type: (str) -> str
    return re.sub(RE_CONTROL_CODE_ENTITY, process_control_code_match, data)


def decode_entities(data):  # type: (str) -> str
    # html.unescape() correctly handles control code entities
    # We need manually process such entities only in python
    # versions where html module is not available
    if not HTML_MODULE_AVAIL:
        data = fix_control_code_entities(data)
    return unescape(data)
