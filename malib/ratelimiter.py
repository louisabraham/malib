import collections
import time

from scipy import stats

__all__ = ["RateLimiter"]


class RateLimiter:
    def __init__(self, max_calls: int, period: float):
        assert max_calls > 0
        self.calls: collections.deque[float] = collections.deque(maxlen=max_calls)
        self.period = period
        self.max_calls = max_calls

    def wait_and_call(self) -> None:
        if len(self.calls) == self.max_calls:
            wait = self.period + self.calls[0] - time.time()
            if wait > 0:
                time.sleep(wait)
        self.calls.append(time.time())

    def prob_exceeded_poisson(self, mu: float, duration: float) -> float:
        """
        Probability that the rate limit is exceeded within a given duration
        when events are Poisson distributed with rate mu.
        Not accurate when duration / period is small (less than 2).

        Naus, J.I., 1982. Approximations for distributions of scan statistics.
        Journal of the American Statistical Association, 77(377), pp.177-183.
        https://annas-archive.org/scidb/10.1080/01621459.1982.10477783
        """
        k = self.max_calls + 1
        mu = mu * self.period
        duration = duration / self.period

        def p(k):
            return stats.poisson.pmf(k, mu)

        def fp(k):
            return stats.poisson.cdf(k, mu)

        q2 = (
            fp(k - 1) ** 2 - (k - 1) * p(k) * p(k - 2) - (k - 1 - mu) * p(k) * fp(k - 3)
        )
        a1 = 2 * p(k) * fp(k - 1) * ((k - 1) * fp(k - 2) - mu * fp(k - 3))
        a2 = (
            0.5
            * p(k) ** 2
            * (
                (k - 1) * (k - 2) * fp(k - 3)
                - 2 * (k - 2) * mu * fp(k - 4)
                + mu**2 * fp(k - 5)
            )
        )
        a3 = sum(p(2 * k - r) * fp(r - 1) ** 2 for r in range(1, k))
        a4 = sum(
            p(2 * k - r) * p(r) * ((r - 1) * fp(r - 2) - mu * fp(r - 3))
            for r in range(2, k)
        )
        q3 = fp(k - 1) ** 3 - a1 + a2 + a3 - a4
        return 1 - q2 * (q3 / q2) ** (duration - 2)
