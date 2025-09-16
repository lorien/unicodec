__all__ = [
    "InvalidEncodingName",
    "InvalidEncodingNameError",
    "UnicodecError",
]


class UnicodecError(Exception):
    pass


class InvalidEncodingNameError(UnicodecError):
    pass


# Backward-compatibility
InvalidEncodingName = InvalidEncodingNameError
