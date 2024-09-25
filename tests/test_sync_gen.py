import asyncio
from time import time

import pytest

from malib import sync_gen


def test_sync_gen():
    # Test with a synchronous generator
    def sync_generator():
        for i in range(3):
            yield i

    result = list(sync_gen(sync_generator()))
    assert result == [0, 1, 2]

    # Test with an asynchronous generator
    async def async_generator():
        for i in range(3):
            await asyncio.sleep(0.1)
            yield i

    result = list(sync_gen(async_generator()))
    assert result == [0, 1, 2]

    # Test with a regular iterable
    iterable = [1, 2, 3]
    result = list(sync_gen(iterable))
    assert result == [1, 2, 3]

    # Test with an invalid input
    with pytest.raises(TypeError):
        list(sync_gen(42))


async def test_sync_gen_async():
    async def async_generator():
        for i in range(3):
            await asyncio.sleep(0.1)
            yield i

    assert list(sync_gen(async_generator())) == [0, 1, 2]


def test_sync_gen_performance():
    async def slow_async_generator():
        for i in range(3):
            await asyncio.sleep(0.1)
            yield i

    start_time = time()
    result = list(sync_gen(slow_async_generator()))
    end_time = time()

    assert result == [0, 1, 2]
    print(end_time - start_time)
    # Ensure it took at least 0.3 seconds but not much longer
    assert 0.3 < end_time - start_time < 0.31
