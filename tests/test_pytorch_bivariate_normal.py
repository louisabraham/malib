from malib import standard_bivariate_normal_cdf, bivariate_normal_cdf

import torch
from scipy.stats import multivariate_normal


def test_gradient():
    for _ in range(100):
        cor = 1 * torch.rand(1) - 1
        x = 5 * torch.randn(1, 2, requires_grad=True, dtype=torch.float64)
        torch.autograd.gradcheck(standard_bivariate_normal_cdf, (x, cor))


def test_reparametrization():
    for _ in range(10):
        cov = torch.randn(2, 2, dtype=torch.float64)
        cov = 10 * cov @ cov.T
        mean = torch.randn(2, dtype=torch.float64)
        x = 5 * torch.randn(10, 2, dtype=torch.float64)
        assert torch.allclose(
            torch.tensor(multivariate_normal.cdf(x, mean, cov)),
            bivariate_normal_cdf(x, mean, cov),
        )


def test_reparametrization_gradient():
    for _ in range(100):
        cov = torch.randn(2, 2, dtype=torch.float64)
        cov = 10 * cov @ cov.T
        mean = torch.randn(2, dtype=torch.float64)
        x = 5 * torch.randn(1, 2, requires_grad=True, dtype=torch.float64)
        torch.autograd.gradcheck(bivariate_normal_cdf, (x, mean, cov))
