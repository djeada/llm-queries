import time


class TTLCache:
    def __init__(self, ttl_seconds, clock=time.monotonic):
        self.ttl_seconds = ttl_seconds
        self.clock = clock
        self._items = {}

    def set(self, key, value):
        self._items[key] = (value, self.clock())

    def _expired(self, created_at):
        return self.clock() - created_at >= self.ttl_seconds

    def get(self, key):
        item = self._items.get(key)
        if item is None:
            return None

        value, created_at = item
        if self._expired(created_at):
            del self._items[key]
            return None
        return value

    def __len__(self):
        expired = [
            key
            for key, (_, created_at) in self._items.items()
            if self._expired(created_at)
        ]
        for key in expired:
            del self._items[key]
        return len(self._items)
