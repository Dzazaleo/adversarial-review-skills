"""Minimal key-value table backed by a dict."""


class KeyValueStore:
    def __init__(self) -> None:
        self._data: dict[str, bytes] = {}

    def get(self, key: str) -> bytes | None:
        return self._data.get(key)

    def put(self, key: str, value: bytes) -> None:
        self._data[key] = value
