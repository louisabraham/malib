# malib

A few utilities that I find useful.


## Cached stubs

Create pytest fixtures to cache the output of functions. See the [blog post](https://louisabraham.github.io/articles/cached-stubs) for more details.

```py
# in your conftest.py

from os import getenv
from malib import cached_stubs

from my_module import network_function, a, b

# default values for configuration
cached_stubs.RECORD = getenv("RECORD") == "1" 
cached_stubs.PATH = "tests/cached_stubs"

# this patches my_module.network_function by default
fixture = cached_stubs.create(network_function, ignore_args=["api_key"])

# this will patch other_module.network_function too
fixture = cached_stubs.create(network_function, modules=["my_module, ""other_module"])

# to combine two fixtures in one
fixture_a = cached_stubs.create(a)
fixture_b = cached_stubs.create(b)

@pytest.fixture
def fixture_ab(fixture_a, fixture_b):
    pass
```

## RateLimiter

```py
from malib import RateLimiter

# call a function at most 10 times per minute
rl = RateLimiter(max_calls=10, period=60) 
# call .wait_and_call() every time before calling the function
rl.wait_and_call()
# approximate probability that the rate limit is exceeded within 1 hour
# when events are Poisson distributed with rate 3 per minute
print(rl.prob_exceeded_poisson(mu=3 / 60, duration=3600))
# 0.09958253462915534
```

## ttl_cache

```py
from malib import ttl_cache
from time import sleep


@ttl_cache(ttl=1)
def f():
    print("computing")
    return "result"


print(f()) # prints "computing"
print(f()) # cached
sleep(1)
print(f()) # prints "computing"
```

## Exact cover

Code inspired by this [blog post](https://louisabraham.github.io/articles/exact-cover).
```py
from malib import exact_cover

piece_to_constraints = {"A": {1}, "B": {2, 4}, "C": {2, 3, 5}, "D": {3, 5}}
next(exact_cover(piece_to_constraints))
# ("A", "B", "D")
```

## PyTorch bivariate normal cdf

Provide two functions to compute a differentiable cumulative distribution function of a bivariate normal distribution.

Requires scipy and pytorch.

```py
import torch
from malib import standard_bivariate_normal_cdf, bivariate_normal_cdf

# standard bivariate normal cdf
x = torch.tensor([0.0, 0.0], requires_grad=True)
cor = 0.5
y = standard_bivariate_normal_cdf(x, cor)
print(y)
# tensor(0.3333, grad_fn=<StandardBivariateNormalCDFBackward>)
y.backward()
print(x.grad)
# tensor([0.1995, 0.1995])

# bivariate_normal_cdf
x = torch.tensor([0.0, 0.0], requires_grad=True)
mean = torch.tensor([0.0, 0.0])
cov = torch.tensor([[1.0, 0.5], [0.5, 1.0]])
y = bivariate_normal_cdf(x, mean, cov)
print(y)
# tensor(0.3333, grad_fn=<BivariateNormalCDFBackward>)
y.backward()
print(x.grad)
# tensor([0.1995, 0.1995])
```

## PyTorch interpolation

```py
import torch
from malib import interp

x = torch.tensor([0.0, 1.0, 2.0])
y = torch.tensor([0.0, 1.0, 4.0])
interp(torch.tensor([0.5, 1.5]), x, y)
# tensor([0.5000, 2.5000])
```

## Async to sync generator

The `sync_gen` function allows you to convert an asynchronous generator into a synchronous one. This can be useful when you want to use async code in a synchronous context.

```python
import asyncio
from malib import sync_gen

async def async_generator():
    for i in range(5):
        await asyncio.sleep(0.1)
        yield i

# Convert async generator to sync generator
sync_generator = sync_gen(async_generator())

# Use the sync generator in a regular for loop
for item in sync_generator:
    print(item)
```


## Confidence interval

```py
from malib import clopper_pearson_confidence_interval

print(clopper_pearson_confidence_interval(100, 1000, alpha=0.05))
# (0.08210533435557998, 0.12028793651869261)
```

## Testing

```
poetry install --with dev
pytest
```

