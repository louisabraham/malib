import asyncio
import collections

import nest_asyncio

nest_asyncio.apply()


def sync_gen(gen):
    """
    Converts an asynchronous generator into a synchronous generator.
    If a synchronous generator or iterable is passed, it returns it unchanged.

    Parameters:
    gen (generator): The generator or iterable to convert.

    Yields:
    The items from the generator, either sync or async, in a synchronous manner.
    """

    # Check if the argument is an asynchronous generator
    if hasattr(gen, "__anext__"):
        # Get or create an event loop
        while True:
            try:
                # Await the next item in the async generator and yield it synchronously
                yield asyncio.run(gen.__anext__())
            except StopAsyncIteration:
                break

    # Check if the argument is a synchronous iterable or generator
    elif isinstance(gen, collections.abc.Iterable):
        # If it's a regular sync generator or iterable, just yield from it
        yield from gen

    else:
        raise TypeError(
            "The provided argument is neither a synchronous "
            "nor an asynchronous generator."
        )
