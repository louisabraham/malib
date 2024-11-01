from time import perf_counter
from unittest import mock

import numpy as np
import pytest

from malib import RateLimiter, clopper_pearson_confidence_interval


def test_ratelimiter():
    rl = RateLimiter(max_calls=5, period=0.1)
    s = perf_counter()
    for _ in range(rl.max_calls):
        rl.wait_and_call()
    assert perf_counter() - s < 0.01
    s = perf_counter()
    rl.wait_and_call()
    assert abs(perf_counter() - s - rl.period) < 0.01
    s = perf_counter()
    for _ in range(rl.max_calls - 1):
        rl.wait_and_call()
    assert perf_counter() - s < 0.01


def poisson_process(mu, duration):
    n_events = np.random.poisson(mu * duration)
    if n_events == 0:
        return np.empty(0)
    events = np.random.uniform(low=0.0, high=duration, size=n_events)
    events.sort()
    return events


def failure(max_calls, period, events):
    """
    Simulate a Poisson process with rate limit and mu parameter.
    """
    current_time = 0

    def side_effect(t):
        nonlocal current_time
        current_time += t

    rate_limiter = RateLimiter(max_calls, period)
    with mock.patch(
        "malib.ratelimiter.time.time", new_callable=lambda: lambda: current_time
    ):
        with mock.patch(
            "malib.ratelimiter.time.sleep", side_effect=side_effect
        ) as sleep:
            for event in events:
                current_time = event
                rate_limiter.wait_and_call()
                if sleep.call_count:
                    return True
    return False


def failure_alternative(max_calls, period, events):
    events = np.asarray(events)
    return np.any(events[max_calls:] - events[:-max_calls] < period)


TEST_CASES = [
    (period, mu, duration * period, max_calls)
    for period in [1.0, 1.5]
    for mu in [0.1, 1.0, 2.0]
    for duration in [2.0, 3.0, 5.0]
    for max_calls in [1, 2, 5]
]


@pytest.mark.parametrize("period,mu,duration,max_calls", TEST_CASES)
def test_failure(period, mu, duration, max_calls, n_samples=10):
    for _ in range(n_samples):
        events = poisson_process(mu, duration)
        assert failure(max_calls, period, events) == failure_alternative(
            max_calls, period, events
        )


@pytest.mark.parametrize("period,mu,duration,max_calls", TEST_CASES)
def test_prob_exceeded_poisson(period, mu, duration, max_calls, n_samples=2_000):
    for _ in range(5):
        tot = 0
        for it in range(n_samples):
            events = poisson_process(mu, duration)
            f2 = failure_alternative(max_calls, period, events)
            tot += f2
            if it < 10:
                f1 = failure(max_calls, period, events)
                assert f1 == f2
        approx_prob = RateLimiter(max_calls, period).prob_exceeded_poisson(mu, duration)
        a, b = clopper_pearson_confidence_interval(tot, n_samples)
        if a <= approx_prob <= b:
            return
    raise AssertionError
