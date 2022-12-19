from __future__ import annotations

from .errors import InvalidEncodingName
from .main import decode_content, detect_content_encoding

__all__ = ["decode_content", "detect_content_encoding", "InvalidEncodingName"]
__version__ = "0.0.4"
