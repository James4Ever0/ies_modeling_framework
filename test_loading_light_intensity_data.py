import numpy as np

path = "./jinan_changqing-hour.dat"

data = np.loadtxt(path, dtype=float)
print("SHAPE OF DATA:", data.shape)  #  (8760, 4)
# (row_count, column_count)

# breakpoint()
import math
num_hour = 24

radiation = data[:, 0]
intensityOfIllumination1 = radiation

print("MATRIX_1_SHAPE", intensityOfIllumination1.shape) # just an excerpt.

for loop in range(1, math.ceil(num_hour / 8760)): # 365, days in a year
    intensityOfIllumination1 = np.concatenate( # what does this concatenate do?
        (intensityOfIllumination1, radiation), axis=0
    )
    
print("MATRIX_1_SHAPE", intensityOfIllumination1.shape) # just an excerpt.
