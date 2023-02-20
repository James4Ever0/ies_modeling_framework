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
print(intensityOfIllumination1[:100])
# not looping?


for loop in range(1, math.ceil(num_hour / 8760)): # 1/365, clearly not what we want.
    intensityOfIllumination1 = np.concatenate( # what does this concatenate do?
        (intensityOfIllumination1, radiation), axis=0
    )
    print("CHANGING?",loop)
    
print("MATRIX_1_SHAPE", intensityOfIllumination1.shape) # just an excerpt.
print(intensityOfIllumination1[:100])
# seems it is doing nothing
