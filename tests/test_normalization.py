import codecs

import pytest

from unicodec.errors import InvalidEncodingName
from unicodec.normalization import (
    WHATWG_ALIASES,
    WHATWG_PYTHON_CODEC_FIXES,
    normalize_encoding_name,
)


def test_normalize_encoding_invalid_name():
    # type: () -> None
    with pytest.raises(InvalidEncodingName):
        normalize_encoding_name("asdfasdfasdf")


def test_normalize_encoding_empty_string():
    # type: () -> None
    with pytest.raises(InvalidEncodingName):
        normalize_encoding_name("")


@pytest.mark.parametrize(
    ("test_name", "correct_name"),
    [
        ("utf8", "utf-8"),
        ("cp1251", "windows-1251"),
        # chinees encodings
        ("gbk", "gb18030"),
        ("gb2312", "gb18030"),
        # mysql
        ("utf8mb4", "utf-8"),
        # ascii
        ("ascii", "windows-1252"),
        # typo
        ("uft-8", "utf-8"),
        # whatwg canonical
        ("iso8859-1", "windows-1252"),
        ("iso-8859-1", "windows-1252"),
    ],
)
def test_normalize_encoding(test_name, correct_name):
    # type: (str, str) -> None
    assert normalize_encoding_name(test_name) == correct_name


@pytest.mark.parametrize(
    "name", set(WHATWG_ALIASES.values()) - set(WHATWG_PYTHON_CODEC_FIXES.keys())
)
def test_whatwg_engocing_names_support(name):
    # type: (str) -> None
    assert isinstance(codecs.lookup(name), codecs.CodecInfo)
