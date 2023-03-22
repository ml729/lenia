import os
import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
import torchvision
from torchvision import transforms
from tqdm import tqdm
from itertools import chain

# parameters
root="./data/"

R = 10 # radius of neighborhood, "space resolution"
T = 1 # timestep, "time resolution"
P = 20 # state set is 0, 1, .. P, "state resolution"
dx = 1/R # site distance
dt = 1/T # time step
dp = 1/P # state precision
kernel_core_fn = lambda r: 4 * r * (1-r)
kernel_peaks = torch.Tensor([1]*8)
# end parameters



def construct_kernel_shell(kernel_core, kernel_peaks):
    """
    kernel_peaks in [0,1]^B
    """
    B = kernel_peaks.shape[0]
    def kernel_shell(r):
        Br = B * r
        floor_peak = kernel_peaks.gather(torch.floor(Br))
        core_val = kernel_core(torch.remainder(Br, 1))
        return floor_peak * core_val
    return kernel_shell

def construct_kernel(kernel_shell, neighborhood):
    def kernel(n):
        mag = kernel_shell(neighborhood).sum() * dx**2
        return kernel_shell(n.norm(dim=1, p=2)) / mag
    return kernel



class CellularAutomata:
    def __init__(self, lattice, timeline, state_set, neighborhood, local_rule):
        self.lattice = lattice
        self.timeline = timeline
        self.state_set = state_set
        self.neighborhood = neighborhood
        self.local_rule = local_rule

    def evolve(self):
        pass

class DiscreteLenia(CellularAutomata):
    def __init__(self, lattice, timeline, state_set, neighborhood, local_rule):
        super().__init__(lattice, timeline, state_set, neighborhood, local_rule)
        self.kernel_shell = construct_kernel_shell(kernel_core_fn, kernel_peaks)
        self.kernel = construct_kernel(self.kernel_shell, self.neighborhood)

    def evolve(self):
        pass




def render_lenia():
    pass
