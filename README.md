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

## Testing

`pytest`

