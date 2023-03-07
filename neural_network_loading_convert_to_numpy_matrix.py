from neural_network_demo import model, input_layer, hidden_layer, output_layer
import numpy as np

######## need that hard

model_save_path = "model.pt"

import torch

model.load_state_dict(torch.load(model_save_path))
model.eval()

# input_layer.bias
bias_list = [input_layer.bias.detach().numpy(),hidden_layer.bias.detach().numpy(),]
breakpoint()