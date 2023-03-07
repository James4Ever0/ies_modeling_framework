import numpy as np

x_lb, x_ub = 0,3
y_lb, y_ub = 0, 2*np.pi

x_sample_size = y_sample_size = 100

# expression: z = x * sin(y)

x = np.linspace(x_lb, x_ub, x_sample_size)
y = np.linspace(y_lb, y_ub, y_sample_size)


z = outputs = np.array(
    [x_element * np.sin(y_element) for y_element in y for x_element in x]
)

inputs = np.array([[x_element, y_element] for y_element in y for x_element in x])

import torch
from torch import Tensor

from neural_network_demo import model

print(model)

inputs_tensor = Tensor(inputs)
outputs_tensor = Tensor(outputs.reshape(-1, 1))

print(inputs_tensor.shape, outputs_tensor.shape)

# The nn package also contains definitions of popular loss functions; in this
# case we will use Mean Squared Error (MSE) as our loss function.
learning_rate = 1e-4
train_epoches = 30000

optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
loss_fn = torch.nn.MSELoss(reduction='sum')

for t in range(train_epoches):
    # Forward pass: compute predicted y by passing x to the model. Module objects
    # override the __call__ operator so you can call them like functions. When
    # doing so you pass a Tensor of input data to the Module and it produces
    # a Tensor of output data.
    y_pred = model(inputs_tensor)

    # Compute and print loss. We pass Tensors containing the predicted and true
    # values of y, and the loss function returns a Tensor containing the
    # loss.
    loss = loss_fn(y_pred, outputs_tensor)
    if t % 100 == 99:
        print(t, loss.item())

    # Zero the gradients before running the backward pass.
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

print("TRAINING COMPLETE")
# You can access the first layer of `model` like accessing the first item of a list
# bias_1 = input_layer.bias
# weight_1 = input_layer.weight

model_save_path = "model.pt"
torch.save(model.state_dict(), model_save_path)
# breakpoint()

# # For linear layer, its parameters are stored as `weight` and `bias`.
# print(f'Result: y = {linear_layer.bias.item()} + {linear_layer.weight[:, 0].item()} x + {linear_layer.weight[:, 1].item()} x^2 + {linear_layer.weight[:, 2].item()} x^3')
