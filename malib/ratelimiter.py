import collections
import time

__all__ = ["RateLimiter"]


class RateLimiter:
    def __init__(self, max_calls, period):
        self.calls = collections.deque(maxlen=max_calls)
        self.period = period
        self.max_calls = max_calls

    def wait(self) -> bool:
        ans = False
        if len(self.calls) == self.max_calls:
            wait = self.period + self.calls[0] - time.time()
            if wait > 0:
                time.sleep(wait)
                ans = True
        self.calls.append(time.time())
        return ans
