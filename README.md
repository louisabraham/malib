# malib

A few utilities that I find useful.


## RateLimiter

```py
from malib import RateLimiter

# call a function at most 10 times per minute
rl = RateLimiter(max_calls=10, period=60) 
# call .wait_and_call() every time before calling the function
rl.wait_and_call()
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

## Testing

```
poetry install --with dev
pytest
```

