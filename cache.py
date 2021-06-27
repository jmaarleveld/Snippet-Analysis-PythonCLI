import json
import os

from config import *


class Cache:

    def __init__(self, filename):
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                json.dump({}, file, indent=4)
        with open(filename) as file:
            self.cache_info = json.load(file)
        self.filename = filename

    def __contains__(self, key):
        if not isinstance(key, str):
            key = str(key)
        return key in self.cache_info

    def all(self):
        return self.cache_info.values()

    def reverse_lookup(self, value):
        # reverse cache on the fly
        rev = {v: k for k, v in self.cache_info.items()}
        return rev[value]

    def retrieve(self, *keys):
        return self.cache_info[str(keys)]

    def store(self, item, *keys):
        self.cache_info[str(keys)] = item
        with open(self.filename, 'w') as file:
            json.dump(self.cache_info, file, indent=4)


cache = Cache(CACHE_INFO)
