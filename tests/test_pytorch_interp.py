# %%
import torch
import numpy as np

from malib import interp


def test_interp():
    for _ in range(10):
        x = torch.rand(100) * 2 - 0.5
        xp = torch.linspace(0, 1, 100)
        fp = torch.rand(100)
        assert torch.allclose(
            interp(x, xp, fp), torch.tensor(np.interp(x, xp, fp)).float()
        )
