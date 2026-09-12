# app/tests/test_utils.py
from app.utils import cache


class FakeRedis:
    """Redis falso en memoria, suficiente para probar el decorador redis_cache"""

    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def setex(self, key, ttl, value):
        self.store[key] = value


def test_redis_cache_returns_cached_result_without_recalling_func(monkeypatch):
    monkeypatch.setattr(cache, "redis_client", FakeRedis())
    calls = []

    @cache.redis_cache(ttl=60)
    def add(a, b):
        calls.append((a, b))
        return {"result": a + b}

    assert add(1, 2) == {"result": 3}
    assert add(1, 2) == {"result": 3}
    assert len(calls) == 1  # la segunda llamada vino del caché, no de la función


def test_redis_cache_uses_a_different_key_per_arguments(monkeypatch):
    fake = FakeRedis()
    monkeypatch.setattr(cache, "redis_client", fake)

    @cache.redis_cache(ttl=60)
    def add(a, b):
        return {"result": a + b}

    assert add(1, 2) == {"result": 3}
    assert add(10, 20) == {"result": 30}
    assert len(fake.store) == 2  # cada combinacion de argumentos tiene su propia entrada
