# import torch
import torch.nn as nn
# from torch import Tensor

hidden_size = 40

input_layer = nn.Linear(2, hidden_size)
# activation_func = nn.ReLU()
# activation_func = nn.RReLU()
activation_func = nn.Hardtanh()
hidden_layer = nn.Linear(hidden_size, hidden_size)
output_layer = nn.Linear(hidden_size, 1)

# model = nn.Sequential(input_layer, output_layer)
model = nn.Sequential(
    input_layer, activation_func, hidden_layer, activation_func, output_layer
)