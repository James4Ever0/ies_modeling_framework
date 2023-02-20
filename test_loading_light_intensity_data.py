import numpy as np

path = "./jinan_changqing-hour.dat"

data = np.loadtxt(path, dtype=float)
print("SHAPE OF DATA:", data.shape)  #  (8760, 4)
# (row_count, column_count)

breakpoint()
