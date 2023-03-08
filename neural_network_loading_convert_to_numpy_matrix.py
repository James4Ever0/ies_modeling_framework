from neural_network_demo import model, input_layer, hidden_layer, output_layer
import numpy as np

######## need that hard

model_save_path = "model.pt"

import torch

model.load_state_dict(torch.load(model_save_path))
model.eval()

# input_layer.bias
bias_list = [
    input_layer.bias.detach().numpy(),
    hidden_layer.bias.detach().numpy(),
    output_layer.bias.detach(),
]

weight_list = [
    input_layer.weight.detach(),
    hidden_layer.weight.detach(),
    output_layer.weight.detach(),
]


# what about the hard-tanh?
def hard_tanh(numpy_array: np.ndarray):  # destructive!
    numpy_array[np.where(numpy_array < -1)] = -1
    numpy_array[np.where(numpy_array > 1)] = 1
    return numpy_array # you can discard it anyway.

layer_depth = 3
import random
test_xy_vals = [[random.randrange(0,2),random.randrange()]]
for x_val, y_val in test_xy_vals:
    input_val =np.array([x_val,y_val]).reshape(1,-1)

    for i in range(layer_depth):
        # breakpoint()
        input_val = np.matmul(input_val,weight_list[i].T)
        input_val+= bias_list[i].reshape(1,-1)
        if i != layer_depth-1:
            input_val = hard_tanh(input_val)

    # check the output.
    answer = x_val*np.sin(y_val)
    print("XY VALS:", x_val, y_val)
    print(input_val, answer)
    print()