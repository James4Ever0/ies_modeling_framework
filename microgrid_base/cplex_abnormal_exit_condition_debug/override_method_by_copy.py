def original_func():
    print('abc')

import copy

new_func = copy.copy(original_func)

def original_func():
    print('new_func')
    new_func()

original_func() # working!