import unittest

from cache import TTLCache


class FakeClock:
    def __init__(self):
        self.value = 100.0

    def __call__(self):
        return self.value

    def advance(self, seconds):
        self.value += seconds


class CacheTests(unittest.TestCase):
    def test_round_trip_before_expiry(self):
        clock = FakeClock()
        cache = TTLCache(10, clock)
        cache.set("answer", 42)
        clock.advance(5)
        self.assertEqual(cache.get("answer"), 42)

    def test_missing_key(self):
        cache = TTLCache(10, FakeClock())
        self.assertIsNone(cache.get("missing"))


if __name__ == "__main__":
    unittest.main()
