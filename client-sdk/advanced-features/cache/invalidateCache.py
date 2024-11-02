class Cache:
    def __init__(self):
        self.store = {}

    def set(self, function_name, args, value):
        key = (function_name, tuple(args))
        self.store[key] = value

    def get(self, function_name, args):
        key = (function_name, tuple(args))
        return self.store.get(key)

    def invalidate(self, function_name, args):
        key = (function_name, tuple(args))
        if key in self.store:
            del self.store[key]
            return True
        return False
