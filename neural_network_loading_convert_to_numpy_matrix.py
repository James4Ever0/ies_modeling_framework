from neural_network_demo import model, input_layer, hidden_layer, output_layer
import numpy as np

model_save_path = "model.pt"

import torch

model.load_state_dict(torch.load(model_save_path))
model.eval()

layers = [input_layer, hidden_layer, output_layer]

bias_list = [layer.bias.detach().numpy() for layer in layers]

weight_list = [layer.weight.detach().numpy() for layer in layers]


# what about the hard-tanh?
def hard_tanh(numpy_array: np.ndarray):  # destructive!
    numpy_array[np.where(numpy_array < -1)] = -1
    numpy_array[np.where(numpy_array > 1)] = 1
    return numpy_array  # you can discard it anyway.


layer_depth = len(layers)
sample_size = 100
import random

test_xy_vals = [
    [random.uniform(0, 3), random.uniform(0, 2 * np.pi)] for _ in range(sample_size)
]

for x_val, y_val in test_xy_vals:
    input_val = np.array([x_val, y_val]).reshape(1, -1)

    for i in range(layer_depth):
        # breakpoint()
        input_val = np.matmul(input_val, weight_list[i].T)
        input_val += bias_list[i].reshape(1, -1)
        if i != layer_depth - 1:
            input_val = hard_tanh(input_val)

    # check the output.
    answer = x_val * np.sin(y_val)
    print("XY VALS:", x_val, y_val)
    print(input_val, answer)
    print()
