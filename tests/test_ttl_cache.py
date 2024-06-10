from malib import ttl_cache

from malib import RateLimiter
from time import time, sleep


def test_ttl_cache():
    @ttl_cache(ttl=0.1)
    def f():
        return time()

    t0 = f()
    sleep(0.05)
    t1 = f()
    assert t0 == t1
    sleep(0.06)
    t2 = f()
    assert t0 != t2
