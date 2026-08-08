class Registry:
    def __init__(self):
        self._store = {}

    def register(self, name: str, obj):
        self._store[name] = obj

    def get(self, name: str):
        return self._store.get(name)

    def all(self):
        return self._store