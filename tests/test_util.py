import pytest

from unicodec.errors import InvalidEncodingName
from unicodec.util import normalize_encoding_name


def test_normalize_encoding_invalid_name() -> None:
    with pytest.raises(InvalidEncodingName):
        normalize_encoding_name("asdfasdfasdf")


def test_normalize_encoding_empty_string() -> None:
    with pytest.raises(InvalidEncodingName):
        normalize_encoding_name("")


@pytest.mark.parametrize(
    "test_name,correct_name",
    [
        ("utf8", "utf-8"),
        ("windows-1251", "cp1251"),
        ("gbk", "gb18030"),
        ("gb2312", "gb18030"),
        ("utf8mb4", "utf-8"),
    ],
)
def test_normalize_encoding_windows1251(test_name: str, correct_name: str) -> None:
    assert normalize_encoding_name(test_name) == correct_name
