from __future__ import annotations

import re

RE_CONTENT_TYPE_CHARSET = re.compile(
    r"charset \s* = \s* ['\"]? ([-_a-z0-9]+)", re.I | re.X
)


def parse_content_type_header_encoding(content_type_header: str) -> None | str:
    match = RE_CONTENT_TYPE_CHARSET.search(content_type_header)
    if match:
        return match.group(1)
    return None
