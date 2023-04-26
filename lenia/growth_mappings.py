import torch


def growth_exponential(u, mean, std):
    return 2 * torch.exp(-(u-mean)**2 / (2 * std**2)) - 1

def growth_polynomial(u, mean, std):
    indicator = ((u <= mean + 3 * std) & (u >= mean - 3 * std)).float()
    return 2 * indicator * (1 - (u-mean)**2/(9*std**2))**4 - 1

def growth_rectangular(u, mean, std):
    indicator = ((u <= mean + std) & (u >= mean - std)).float()
    return 2 * indicator - 1


GROWTH_MAPPINGS = {
    "exponential" : growth_exponential,
    "polynomial": growth_polynomial,
    "rectangular": growth_rectangular
}
