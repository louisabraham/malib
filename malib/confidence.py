from scipy import stats


def clopper_pearson_confidence_interval(k, n, alpha=0.05):
    """
    Compute the Clopper-Pearson confidence interval for the binomial distribution.
    alpha is the bound of the error probability.
    """
    a, b = stats.beta.ppf([alpha / 2, 1 - alpha / 2], [k, k + 1], [n - k + 1, n - k])
    if k == 0:
        a = 0.0
    if k == n:
        b = 1.0
    return a, b
