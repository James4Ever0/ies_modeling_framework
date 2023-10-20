import torchpwl

# Create a PWL consisting of 3 segments for 5 channels - each channel will have its own PWL function.
pwl = torchpwl.PWL(num_channels=5, num_breakpoints=3)
x = torch.Tensor(11, 5).normal_()
y = pwl(x)
