
import torch


def kernel_core_exponential(r):
    return torch.exp(4 - 4/(4 * r * (1 - r)))

def kernel_core_polynomial(r):
    return (4 * r * (1 - r))**4

def kernel_core_rectangular(r):
    indicator = ((r <= 3/4) & (r >= 1/4)).float()
    return indicator

KERNEL_CORES = {
    "exponential" : kernel_core_exponential,
    "polynomial" : kernel_core_polynomial,
    "rectangular" : kernel_core_rectangular
    }
