import time
import collections

__all__ = ["RateLimiter"]


class RateLimiter:
    def __init__(self, max_calls, period):
        self.calls = collections.deque(maxlen=max_calls)
        self.period = period
        self.max_calls = max_calls

    def wait(self):
        if len(self.calls) == self.max_calls:
            wait = self.period + self.calls[0] - time.time()
            if wait > 0:
                time.sleep(wait)
        self.calls.append(time.time())
