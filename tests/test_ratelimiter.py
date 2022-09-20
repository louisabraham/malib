from malib import RateLimiter
from time import perf_counter


def test_ratelimiter():
    rl = RateLimiter(max_calls=5, period=0.1)
    s = perf_counter()
    for _ in range(rl.max_calls):
        rl.wait()
    assert perf_counter() - s < 0.01
    s = perf_counter()
    rl.wait()
    assert abs(perf_counter() - s - rl.period) < 0.01
    s = perf_counter()
    for _ in range(rl.max_calls - 1):
        rl.wait()
    assert perf_counter() - s < 0.01
