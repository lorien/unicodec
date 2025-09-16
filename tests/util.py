def add_encoded_duplicates(items):
    # type: (list[str]) -> list[str | bytes]
    return items + [x.encode() for x in items]
