import asyncio
import inspect
from functools import wraps
from importlib import import_module
from os import getenv
from pathlib import Path
from unittest import mock

import joblib
import nest_asyncio
import pytest
from joblib.func_inspect import get_func_code

nest_asyncio.apply()

RECORD = getenv("RECORD") == "1"
PATH = "tests/cached_stubs"


def _patch_generatorfunction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return list(func(*args, **kwargs))

    wrapper.__wrapped_cached_stubs__ = func

    return wrapper


async def _collect_asyncgenerator(gen):
    return [chunk async for chunk in gen]


def _patch_asyncgenfunction(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(_collect_asyncgenerator(func(*args, **kwargs)))

    wrapper.__wrapped_cached_stubs__ = func
    return wrapper


def _make_asyncgenfunction(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        for item in func(*args, **kwargs):
            yield item

    return wrapper


def _truncate(s, max_len=200):
    return s if len(s) <= max_len else s[: max_len - 3] + "..."


def _raise_not_in_cache_func(func_name):
    def raise_exception(*args, **kwargs):
        arg_str = ", ".join(_truncate(repr(a)) for a in args)
        kwarg_str = ", ".join(f"{k}={_truncate(repr(v))}" for k, v in kwargs.items())
        raise Exception(
            f"Result is not in cache for {func_name}, called with args: ({arg_str}), kwargs: {{{kwarg_str}}}"
        )

    return raise_exception


def _get_func_code(func):
    return get_func_code(getattr(func, "__wrapped_cached_stubs__", func))


mock.patch("joblib.memory.get_func_code", _get_func_code).start()


def create(func, *, modules=None, ignore_args=None):
    memory = joblib.Memory(PATH, verbose=0)
    if isinstance(func, str):
        func = getattr(import_module(modules[0]), func)
    if inspect.isgeneratorfunction(func):
        func = _patch_generatorfunction(func)
    asyncgen = inspect.isasyncgenfunction(func)
    if asyncgen:
        func = _patch_asyncgenfunction(func)
    if modules is None:
        modules = [func.__module__]
    cached_func = memory.cache(func, ignore=ignore_args)
    (Path(PATH) / ".gitignore").unlink(missing_ok=True)
    if not RECORD:
        cached_func._call = _raise_not_in_cache_func(func.__qualname__)
    if asyncgen:
        cached_func = _make_asyncgenfunction(cached_func)
    patches = [
        mock.patch(
            f"{module}.{func.__name__}",
            cached_func,
        )
        for module in modules
    ]

    @pytest.fixture
    def fixture():
        for patch in patches:
            patch.start()
        yield
        for patch in patches:
            patch.stop()

    return fixture
