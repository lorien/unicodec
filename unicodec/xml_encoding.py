"""Functions to detect XML document encoding declared in the document itself."""
import re

try:
    from re import Match  # pylint: disable=unused-import
except ImportError:
    pass

from .errors import InvalidEncodingNameError
from .normalization import normalize_encoding_name

__all__ = ["detect_xml_encoding"]

RE_XML_ENCODING = re.compile(
    r"<\?xml \s+ [^>]* encoding \s* = \s* ['\"] (?P<xml_prolog>[-_a-z-0-9]+)",
    re.VERBOSE | re.IGNORECASE,
)
RE_BYTES_XML_ENCODING = re.compile(
    RE_XML_ENCODING.pattern.encode(), re.VERBOSE | re.IGNORECASE
)


def detect_xml_encoding(data):
    # type: (bytes | str) -> None | str
    match = (
        RE_BYTES_XML_ENCODING.search(data)
        if isinstance(data, bytes)
        else RE_XML_ENCODING.search(data)
    )
    if match:
        enc = match.group("xml_prolog")
        try:
            return normalize_encoding_name(
                enc.decode("latin-1") if isinstance(enc, bytes) else enc
            )
        except InvalidEncodingNameError:
            pass
    return None
