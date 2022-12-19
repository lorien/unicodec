import codecs

from .errors import InvalidEncodingName

__all__ = ["normalize_encoding_name"]

COMMON_TYPOS = {
    "uft-8": "utf-8",
}
EXCEPTIONAL_ENCODINGS = {
    # https://dev.mysql.com/doc/refman/8.0/en/charset-unicode-sets.html
    "utf8mb4": "utf-8",
    # https://dev.mysql.com/doc/refman/5.7/en/charset-unicode-sets.html
    "utf8_general_ci": "utf-8",
}
SUPERSET_ENCODINGS = {
    # https://en.wikipedia.org/wiki/GBK_(character_encoding)
    "gbk": "gb18030",
    # https://en.wikipedia.org/wiki/GB_2312
    "gb2312": "gb18030",
    # https://en.wikipedia.org/wiki/ASCII + WHATWG
    "ascii": "cp1252",
}
# https://encoding.spec.whatwg.org/#names-and-labels
WHATWG_ALIASES = {
    # UTF-8 / The Encoding
    "unicode-1-1-utf-8": "utf-8",
    "unicode11utf8": "utf-8",
    "unicode20utf8": "utf-8",
    "utf-8": "utf-8",
    "utf8": "utf-8",
    "x-unicode20utf8": "utf-8",
    # IBM866 / Legacy single-byte encodings
    "866": "ibm866",
    "cp866": "ibm866",
    "csibm866": "ibm866",
    "ibm866": "ibm866",
    # ISO-8859-2 / Legacy single-byte encodings
    "csisolatin2": "iso-8859-2",
    "iso-8859-2": "iso-8859-2",
    "iso-ir-101": "iso-8859-2",
    "iso8859-2": "iso-8859-2",
    "iso88592": "iso-8859-2",
    "iso_8859-2": "iso-8859-2",
    "iso_8859-2:1987": "iso-8859-2",
    "l2": "iso-8859-2",
    "latin2": "iso-8859-2",
    # ISO-8859-3 / Legacy single-byte encodings
    "csisolatin3": "iso-8859-3",
    "iso-8859-3": "iso-8859-3",
    "iso-ir-109": "iso-8859-3",
    "iso8859-3": "iso-8859-3",
    "iso88593": "iso-8859-3",
    "iso_8859-3": "iso-8859-3",
    "iso_8859-3:1988": "iso-8859-3",
    "l3": "iso-8859-3",
    "latin3": "iso-8859-3",
    # ISO-8859-4 / Legacy single-byte encodings
    "csisolatin4": "iso-8859-4",
    "iso-8859-4": "iso-8859-4",
    "iso-ir-110": "iso-8859-4",
    "iso8859-4": "iso-8859-4",
    "iso88594": "iso-8859-4",
    "iso_8859-4": "iso-8859-4",
    "iso_8859-4:1988": "iso-8859-4",
    "l4": "iso-8859-4",
    "latin4": "iso-8859-4",
    # ISO-8859-5 / Legacy single-byte encodings
    "csisolatincyrillic": "iso-8859-5",
    "cyrillic": "iso-8859-5",
    "iso-8859-5": "iso-8859-5",
    "iso-ir-144": "iso-8859-5",
    "iso8859-5": "iso-8859-5",
    "iso88595": "iso-8859-5",
    "iso_8859-5": "iso-8859-5",
    "iso_8859-5:1988": "iso-8859-5",
    # ISO-8859-6 / Legacy single-byte encodings
    "arabic": "iso-8859-6",
    "asmo-708": "iso-8859-6",
    "csiso88596e": "iso-8859-6",
    "csiso88596i": "iso-8859-6",
    "csisolatinarabic": "iso-8859-6",
    "ecma-114": "iso-8859-6",
    "iso-8859-6": "iso-8859-6",
    "iso-8859-6-e": "iso-8859-6",
    "iso-8859-6-i": "iso-8859-6",
    "iso-ir-127": "iso-8859-6",
    "iso8859-6": "iso-8859-6",
    "iso88596": "iso-8859-6",
    "iso_8859-6": "iso-8859-6",
    "iso_8859-6:1987": "iso-8859-6",
    # ISO-8859-7 / Legacy single-byte encodings
    "csisolatingreek": "iso-8859-7",
    "ecma-118": "iso-8859-7",
    "elot_928": "iso-8859-7",
    "greek": "iso-8859-7",
    "greek8": "iso-8859-7",
    "iso-8859-7": "iso-8859-7",
    "iso-ir-126": "iso-8859-7",
    "iso8859-7": "iso-8859-7",
    "iso88597": "iso-8859-7",
    "iso_8859-7": "iso-8859-7",
    "iso_8859-7:1987": "iso-8859-7",
    "sun_eu_greek": "iso-8859-7",
    # ISO-8859-8 / Legacy single-byte encodings
    "csiso88598e": "iso-8859-8",
    "csisolatinhebrew": "iso-8859-8",
    "hebrew": "iso-8859-8",
    "iso-8859-8": "iso-8859-8",
    "iso-8859-8-e": "iso-8859-8",
    "iso-ir-138": "iso-8859-8",
    "iso8859-8": "iso-8859-8",
    "iso88598": "iso-8859-8",
    "iso_8859-8": "iso-8859-8",
    "iso_8859-8:1988": "iso-8859-8",
    "visual": "iso-8859-8",
    # ISO-8859-8-I / Legacy single-byte encodings
    "csiso88598i": "iso-8859-8-i",
    "iso-8859-8-i": "iso-8859-8-i",
    "logical": "iso-8859-8-i",
    # ISO-8859-10 / Legacy single-byte encodings
    "csisolatin6": "iso-8859-10",
    "iso-8859-10": "iso-8859-10",
    "iso-ir-157": "iso-8859-10",
    "iso8859-10": "iso-8859-10",
    "iso885910": "iso-8859-10",
    "l6": "iso-8859-10",
    "latin6": "iso-8859-10",
    # ISO-8859-13 / Legacy single-byte encodings
    "iso-8859-13": "iso-8859-13",
    "iso8859-13": "iso-8859-13",
    "iso885913": "iso-8859-13",
    # ISO-8859-14 / Legacy single-byte encodings
    "iso-8859-14": "iso-8859-14",
    "iso8859-14": "iso-8859-14",
    "iso885914": "iso-8859-14",
    # ISO-8859-15 / Legacy single-byte encodings
    "csisolatin9": "iso-8859-15",
    "iso-8859-15": "iso-8859-15",
    "iso8859-15": "iso-8859-15",
    "iso885915": "iso-8859-15",
    "iso_8859-15": "iso-8859-15",
    "l9": "iso-8859-15",
    # ISO-8859-16 / Legacy single-byte encodings
    "iso-8859-16": "iso-8859-16",
    # KOI8-R / Legacy single-byte encodings
    "cskoi8r": "koi8-r",
    "koi": "koi8-r",
    "koi8": "koi8-r",
    "koi8-r": "koi8-r",
    "koi8_r": "koi8-r",
    # KOI8-U / Legacy single-byte encodings
    "koi8-ru": "koi8-u",
    "koi8-u": "koi8-u",
    # macintosh / Legacy single-byte encodings
    "csmacintosh": "macintosh",
    "mac": "macintosh",
    "macintosh": "macintosh",
    "x-mac-roman": "macintosh",
    # windows-874 / Legacy single-byte encodings
    "dos-874": "windows-874",
    "iso-8859-11": "windows-874",
    "iso8859-11": "windows-874",
    "iso885911": "windows-874",
    "tis-620": "windows-874",
    "windows-874": "windows-874",
    # windows-1250 / Legacy single-byte encodings
    "cp1250": "windows-1250",
    "windows-1250": "windows-1250",
    "x-cp1250": "windows-1250",
    # windows-1251 / Legacy single-byte encodings
    "cp1251": "windows-1251",
    "windows-1251": "windows-1251",
    "x-cp1251": "windows-1251",
    # windows-1252 / Legacy single-byte encodings
    "ansi_x3.4-1968": "windows-1252",
    "ascii": "windows-1252",
    "cp1252": "windows-1252",
    "cp819": "windows-1252",
    "csisolatin1": "windows-1252",
    "ibm819": "windows-1252",
    "iso-8859-1": "windows-1252",
    "iso-ir-100": "windows-1252",
    "iso8859-1": "windows-1252",
    "iso88591": "windows-1252",
    "iso_8859-1": "windows-1252",
    "iso_8859-1:1987": "windows-1252",
    "l1": "windows-1252",
    "latin1": "windows-1252",
    "us-ascii": "windows-1252",
    "windows-1252": "windows-1252",
    "x-cp1252": "windows-1252",
    # windows-1253 / Legacy single-byte encodings
    "cp1253": "windows-1253",
    "windows-1253": "windows-1253",
    "x-cp1253": "windows-1253",
    # windows-1254 / Legacy single-byte encodings
    "cp1254": "windows-1254",
    "csisolatin5": "windows-1254",
    "iso-8859-9": "windows-1254",
    "iso-ir-148": "windows-1254",
    "iso8859-9": "windows-1254",
    "iso88599": "windows-1254",
    "iso_8859-9": "windows-1254",
    "iso_8859-9:1989": "windows-1254",
    "l5": "windows-1254",
    "latin5": "windows-1254",
    "windows-1254": "windows-1254",
    "x-cp1254": "windows-1254",
    # windows-1255 / Legacy single-byte encodings
    "cp1255": "windows-1255",
    "windows-1255": "windows-1255",
    "x-cp1255": "windows-1255",
    # windows-1256 / Legacy single-byte encodings
    "cp1256": "windows-1256",
    "windows-1256": "windows-1256",
    "x-cp1256": "windows-1256",
    # windows-1257 / Legacy single-byte encodings
    "cp1257": "windows-1257",
    "windows-1257": "windows-1257",
    "x-cp1257": "windows-1257",
    # windows-1258 / Legacy single-byte encodings
    "cp1258": "windows-1258",
    "windows-1258": "windows-1258",
    "x-cp1258": "windows-1258",
    # x-mac-cyrillic / Legacy single-byte encodings
    "x-mac-cyrillic": "x-mac-cyrillic",
    "x-mac-ukrainian": "x-mac-cyrillic",
    # GBK / Legacy multi-byte Chinese (simplified) encodings
    "chinese": "gbk",
    "csgb2312": "gbk",
    "csiso58gb231280": "gbk",
    "gb2312": "gbk",
    "gb_2312": "gbk",
    "gb_2312-80": "gbk",
    "gbk": "gbk",
    "iso-ir-58": "gbk",
    "x-gbk": "gbk",
    # gb18030 / Legacy multi-byte Chinese (simplified) encodings
    "gb18030": "gb18030",
    # Big5 / Legacy multi-byte Chinese (traditional) encodings
    "big5": "big5",
    "big5-hkscs": "big5",
    "cn-big5": "big5",
    "csbig5": "big5",
    "x-x-big5": "big5",
    # EUC-JP / Legacy multi-byte Japanese encodings
    "cseucpkdfmtjapanese": "euc-jp",
    "euc-jp": "euc-jp",
    "x-euc-jp": "euc-jp",
    # ISO-2022-JP / Legacy multi-byte Japanese encodings
    "csiso2022jp": "iso-2022-jp",
    "iso-2022-jp": "iso-2022-jp",
    # Shift_JIS / Legacy multi-byte Japanese encodings
    "csshiftjis": "shift_jis",
    "ms932": "shift_jis",
    "ms_kanji": "shift_jis",
    "shift-jis": "shift_jis",
    "shift_jis": "shift_jis",
    "sjis": "shift_jis",
    "windows-31j": "shift_jis",
    "x-sjis": "shift_jis",
    # EUC-KR / Legacy multi-byte Korean encodings
    "cseuckr": "euc-kr",
    "csksc56011987": "euc-kr",
    "euc-kr": "euc-kr",
    "iso-ir-149": "euc-kr",
    "korean": "euc-kr",
    "ks_c_5601-1987": "euc-kr",
    "ks_c_5601-1989": "euc-kr",
    "ksc5601": "euc-kr",
    "ksc_5601": "euc-kr",
    "windows-949": "euc-kr",
    # UTF-16BE / Legacy miscellaneous encodings
    "unicodefffe": "utf-16be",
    "utf-16be": "utf-16be",
    # UTF-16LE / Legacy miscellaneous encodings
    "csunicode": "utf-16le",
    "iso-10646-ucs-2": "utf-16le",
    "ucs-2": "utf-16le",
    "unicode": "utf-16le",
    "unicodefeff": "utf-16le",
    "utf-16": "utf-16le",
    "utf-16le": "utf-16le",
}


def normalize_encoding_name(name: str) -> str:
    name = name.lower()
    name = COMMON_TYPOS.get(name, name)
    name = EXCEPTIONAL_ENCODINGS.get(name, name)
    name = WHATWG_ALIASES.get(name, name)
    try:
        codec_name = codecs.lookup(name).name
        # Use codec name only if it is not an alias in WHATWG table
        if codec_name not in WHATWG_ALIASES:
            name = codec_name
    except LookupError as ex:
        raise InvalidEncodingName("Invalid encoding name: {}".format(name)) from ex
    else:
        return SUPERSET_ENCODINGS.get(name, name)
