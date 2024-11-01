from time import sleep, time

from malib import ttl_cache


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

    @ttl_cache
    def f():
        return "result"

    assert f() == "result"
