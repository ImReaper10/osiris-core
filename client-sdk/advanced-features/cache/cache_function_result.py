from .invalidateCache import Cache

class CacheHandler:
    def __init__(self):
        self.cache = Cache()  # Instantiate the Cache class

    def cache_function_result(self, function_name: str, *args) -> any:
        # Mock function result based on name and args
        if function_name == "addNumbers":
            result = sum(args)  # Simple mock for addNumbers
            self.cache.set(function_name, args, result)  # Store the result in cache
            return result
        return None

    def invalidate_cache(self, function_name: str, *args):
        # Invalidate the cache for the given function name and arguments
        return self.cache.invalidate(function_name, args)
