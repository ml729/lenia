import os
import torch
from torch import nn
from torch.utils.data import DataLoader, random_split
import torchvision
from torchvision import transforms
from tqdm import tqdm
from itertools import chain
import torch.nn.functional as F

from .growth_mappings import GROWTH_MAPPINGS
from .kernel_cores import KERNEL_CORES

# parameters
# root="./data/"

# R = 10 # radius of neighborhood, "space resolution"
# T = 1 # timestep, "time resolution"
# P = 20 # state set is 0, 1, .. P, "state resolution"
# dx = 1/R # site distance
# dt = 1/T # time step
# dp = 1/P # state precision
# kernel_core_fn = lambda r: 4 * r * (1-r)
# B = 8
# kernel_peaks = torch.Tensor([1]*(B) + [0])
# growth_mean = 0
# growth_std = 1
# end parameters

class DiscreteLenia:
    def __init__(self, grid_x, grid_y, space_res, time_res, state_res,
                 kernel_core_name, kernel_peaks, growth_mapping_name,
                 growth_center, growth_width):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.R = space_res
        self.T = time_res
        self.P = state_res
        self.dx = 1/self.R
        self.dt = 1/self.T
        self.dp = 1/self.P
        self.kernel_core = KERNEL_CORES[kernel_core_name]
        self.kernel_peaks = kernel_peaks
        self.growth_center = growth_center
        self.growth_width = growth_width
        self.growth_mapping = GROWTH_MAPPINGS[growth_mapping_name]

        self.B = self.kernel_peaks.shape[0] - 1
        self.kernel_size = 2*self.R+1
        self.config = self.init_config()
        self.kernel = self.init_kernel()
        self.history = [self.config]

    def init_config(self):
        return torch.rand(self.grid_x, self.grid_y)

    def init_kernel(self):
        x, y = torch.meshgrid(torch.arange(self.kernel_size), torch.arange(self.kernel_size))
        distance = torch.sqrt((x-self.R)**2 + (y-self.R)**2)
        mask = (distance <= self.R).float()
        mask_dist = distance * mask * self.dx * self.B
        kernel_shell = self.kernel_peaks[torch.floor(mask_dist)] * self.kernel_core(torch.remainder(mask_dist, 1))
        kernel = kernel_shell / torch.sum(kernel_shell)
        return kernel

    def potential(self, config):
        output_tensor = F.conv2d(config.unsqueeze(0,1),
                                 self.kernel.view(1, 1, self.kernel_size, self.kernel_size),
                                 padding=self.R)
        return output_tensor.squeeze(0,1)

    def update(self):
        next_potential = self.potential(self.config)
        next_growth = self.growth_mapping(next_potential, self.growth_center, self.growth_width)
        next_config = self.config + self.dt * next_growth
        self.config = torch.clamp(next_config, min=0, max=1)
        self.history.append(self.config)






if __name__ == '__main__':
    pass
