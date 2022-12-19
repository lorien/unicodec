__all__ = ["UnicodecError", "InvalidEncodingName"]


class UnicodecError(Exception):
    pass


class InvalidEncodingName(UnicodecError):
    pass
