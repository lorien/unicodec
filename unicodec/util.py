import codecs

from .errors import InvalidEncodingName

EXCEPTIONAL_ENCODINGS = {
    # https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-sets.html
    "utf8mb4": "utf-8",  # I have no idea what I am doing
}
SUPERSET_ENCODINGS = {
    # https://en.wikipedia.org/wiki/GBK_(character_encoding)
    "gbk": "gb18030",
    # https://en.wikipedia.org/wiki/GB_2312
    "gb2312": "gb18030",
}


def normalize_encoding_name(name: str) -> str:
    name = EXCEPTIONAL_ENCODINGS.get(name, name)
    try:
        name = codecs.lookup(name).name
    except LookupError as ex:
        raise InvalidEncodingName("Invalid encoding name: {}".format(name)) from ex
    else:
        return SUPERSET_ENCODINGS.get(name, name)
