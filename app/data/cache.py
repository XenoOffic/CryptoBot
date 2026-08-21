import time
from typing import Any


class MemoryCache:

    def __init__(
        self,
        ttl_seconds: int = 60,
    ):

        self.ttl_seconds = ttl_seconds

        self._data: dict[
            str,
            tuple[float, Any],
        ] = {}

    def get(
        self,
        key: str,
    ):

        item = self._data.get(key)

        if item is None:
            return None

        created_at, value = item

        if (
            time.time() - created_at
            > self.ttl_seconds
        ):

            self._data.pop(
                key,
                None,
            )

            return None

        return value

    def set(
        self,
        key: str,
        value: Any,
    ):

        self._data[key] = (
            time.time(),
            value,
        )

    def delete(
        self,
        key: str,
    ):

        self._data.pop(
            key,
            None,
        )

    def clear(self):

        self._data.clear()


market_cache = MemoryCache(
    ttl_seconds=300
)

historical_cache = MemoryCache(
    ttl_seconds=900
)
