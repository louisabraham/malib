# malib

A few utilities that I find useful.


## RateLimiter

```py
from malib import RateLimiter

# call a function at most 10 times per minute
rl = RateLimiter(max_calls=10, period=60) 
# call .wait() every time before calling the function
rl.wait()
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

## Testing

`pytest`

