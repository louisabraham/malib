import torch


def interp(x, xp, fp, left=None, right=None):
    assert xp.shape == fp.shape
    if left is None:
        left = fp[0]
    if right is None:
        right = fp[-1]
    idx = torch.clamp(torch.searchsorted(xp, x) - 1, 0, len(xp) - 2)
    val = fp[idx] + (fp[idx + 1] - fp[idx]) * (x - xp[idx]) / (xp[idx + 1] - xp[idx])
    val = torch.where(x < xp[0], left, torch.where(x > xp[-1], right, val))
    return val
