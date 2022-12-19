# Unicodec Package Documentation

[![Test Status](https://github.com/lorien/unicodec/actions/workflows/test.yml/badge.svg)](https://github.com/lorien/unicodec/actions/workflows/test.yml)
[![Code Quality](https://github.com/lorien/unicodec/actions/workflows/check.yml/badge.svg)](https://github.com/lorien/unicodec/actions/workflows/test.yml)
[![Type Check](https://github.com/lorien/unicodec/actions/workflows/mypy.yml/badge.svg)](https://github.com/lorien/unicodec/actions/workflows/mypy.yml)
[![Test Coverage Status](https://coveralls.io/repos/github/lorien/unicodec/badge.svg)](https://coveralls.io/github/lorien/unicodec)

This package provides functions for:

- decoding bytes content of HTML document into Unicode text
- detecting encoding of bytes content of HTML document
- normalization of encoding's name to canonical form, according to WHATWG HTML standard

Feel free to give feedback in Telegram groups: [@grablab](https://t.me/grablab) and [@grablab\_ru](https://t.me/grablab_ru).

## Installation

`pip install -U unicodec`

## Usage Example #1

Download web document with urllib and convert its content to Unicode.

```python
from urllib.request import urlopen

from unicodec import decode_content, detect_content_encoding

res = urlopen("http://lib.ru")
rawdata = res.read()
data = decode_content(rawdata, content_type_header=res.headers["content-type"])
print(data[:70])
print(detect_content_encoding(rawdata, res.headers["content-type"]))
```

Output:
```
<html><head><title>Lib.Ru: Библиотека Максима Мошкова</title></head><b
koi8-r
```

## Usage Example #2

Download web document with urllib3 and convert its content to Unicode.

```python
from urllib3 import PoolManager

from unicodec import decode_content, detect_content_encoding

res = PoolManager().urlopen("GET", "http://lib.ru")
rawdata = res.data
data = decode_content(rawdata, content_type_header=res.headers["content-type"])
print(data[:70])
print(detect_content_encoding(rawdata, res.headers["content-type"]))
```

Output:
```
<html><head><title>Lib.Ru: Библиотека Максима Мошкова</title></head><b
koi8-r
```

## Usage Example #3

Convert names of encodings to canonical form (according to WHATWG HTML standard).

```python
from unicodec.normalization import normalize_encoding_name

for name in ["iso8859-1", "utf8", "cp1251"]:
    print("{} -> {}".format(name, normalize_encoding_name(name)))
```

Output:

```
iso8859-1 -> windows-1252
utf8 -> utf-8
cp1251 -> windows-1251
```

## References

- https://docs.python.org/3/library/html.html
- https://docs.python.org/3/library/html.entities.html
- https://html.spec.whatwg.org/multipage/parsing.html
- https://encoding.spec.whatwg.org/#names-and-labels
- https://www.i18nqa.com/debug/table-iso8859-1-vs-windows-1252.html
