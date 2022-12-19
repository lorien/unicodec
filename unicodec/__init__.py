from __future__ import annotations

from .errors import InvalidEncodingName
from .main import decode_content, detect_content_encoding
from .normalization import normalize_encoding_name

__all__ = [
    "decode_content",
    "detect_content_encoding",
    "InvalidEncodingName",
    "normalize_encoding_name",
]
__version__ = "0.0.5"
