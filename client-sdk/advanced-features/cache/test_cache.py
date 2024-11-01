

import unittest
from .cache_function_result import CacheHandler

class TestCache(unittest.TestCase):
    def setUp(self):
        self.cache_handler = CacheHandler()

    def test_cache_function_result(self):
        result = self.cache_handler.cache_function_result("addNumbers", 3, 5)
        self.assertEqual(result, 8)

        # Now retrieve the result from the cache
        result_from_cache = self.cache_handler.cache.get("addNumbers", (3, 5))
        self.assertEqual(result_from_cache, 8)

    def test_invalidate_cache(self):
        self.cache_handler.cache_function_result("addNumbers", 3, 5)
        self.cache_handler.invalidate_cache("addNumbers", 3, 5)
        result_from_cache_after_invalidating = self.cache_handler.cache.get("addNumbers", (3, 5))
        self.assertIsNone(result_from_cache_after_invalidating)

    def test_invalidate_non_existing_cache(self):
        # Try to invalidate a cache entry that does not exist
        result = self.cache_handler.invalidate_cache("addNumbers", 10, 20)  # Non-existing entry
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
