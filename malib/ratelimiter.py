import collections
import time

__all__ = ["RateLimiter"]


class RateLimiter:
    def __init__(self, max_calls, period):
        self.calls = collections.deque(maxlen=max_calls)
        self.period = period
        self.max_calls = max_calls

    def waiting_time(self) -> float:
        if len(self.calls) == self.max_calls:
            return max(0, self.period + self.calls[0] - time.time())
        return 0

    def wait_and_call(self) -> bool:
        wait = self.waiting_time()
        if wait > 0:
            time.sleep(wait)
        self.calls.append(time.time())
        return wait > 0
