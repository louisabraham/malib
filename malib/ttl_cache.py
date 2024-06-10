from functools import cache, _make_key, update_wrapper
from time import time


def _ttl_cache_wrapper(user_function, typed, ttl):
    cache = {}

    def wrapper(*args, **kwargs):
        key = _make_key(args, kwargs, typed)
        ts, result = cache.get(key, (None, None))
        if result is None or time() - ts > ttl:
            result = user_function(*args, **kwargs)
            cache[key] = time(), result
        return result

    return wrapper


def ttl_cache(ttl=60, typed=False):
    if ttl is None:
        return cache(typed=typed)
    elif callable(ttl):
        user_function, ttl = ttl, 60
        return _ttl_cache_wrapper(user_function, typed, ttl)
    ttl = float(ttl)
    assert ttl > 0, "ttl must be positive"

    def decorating_function(user_function):
        wrapper = _ttl_cache_wrapper(user_function, typed, ttl)
        return update_wrapper(wrapper, user_function)

    return decorating_function
