# malib

A few utilities that I find useful.


## RateLimiter

```py
# call a function at most 10 times per minute
rl = RateLimiter(max_calls=10, period=60) 
# call .wait() every time before calling the function
rl.wait()
```


## Testing

`pytest`

