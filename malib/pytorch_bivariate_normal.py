from scipy.stats import multivariate_normal
import torch


__all__ = ["standard_bivariate_normal_cdf", "bivariate_normal_cdf"]


class StandardBivariateNormalCDF(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x, cor):
        cor = float(cor)
        ctx.save_for_backward(x, torch.tensor(cor, dtype=x.dtype))
        assert x.shape[-1] == 2
        return torch.tensor(
            multivariate_normal.cdf(x, cov=[[1, cor], [cor, 1]], allow_singular=True),
            dtype=x.dtype,
        )

    @staticmethod
    def _partial_derivative(x, y, cor):
        """derivative in x"""
        return (
            torch.exp(-x * x / 2)
            / 2
            / torch.sqrt(2 * torch.tensor(torch.pi, dtype=x.dtype))
            * (1 + torch.erf((y - cor * x) / torch.sqrt(2 * (1 - cor * cor))))
        )

    @staticmethod
    def backward(ctx, grad_output):
        x, cor = ctx.saved_tensors
        x, y = x[..., 0], x[..., 1]
        return (
            grad_output[..., None]
            * torch.stack(
                [
                    StandardBivariateNormalCDF._partial_derivative(x, y, cor),
                    StandardBivariateNormalCDF._partial_derivative(y, x, cor),
                ],
                dim=-1,
            ),
            None,
        )


standard_bivariate_normal_cdf = StandardBivariateNormalCDF.apply


def bivariate_normal_cdf(x, mean, cov):
    # assert x.shape[-1] == 2
    # assert cov.shape == (2, 2)
    # assert torch.allclose(cov[0, 1], cov[1, 0])
    cor = cov[0, 1] / torch.sqrt(cov[0, 0] * cov[1, 1])
    return standard_bivariate_normal_cdf((x - mean) / torch.sqrt(cov.diag()), cor)
