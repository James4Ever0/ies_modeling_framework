# to run code faster:
# conda create -n pypy -c conda-forge pypy

import cProfile

# import re
print("before run")


def subfunc():
    val = 0
    for i in range(100):
        val += i
    return val


def test():
    while True:
        subfunc()


import func_timeout
import os

fpath = "profile.bin"
from ForthGK_CLASS_new2 import *


def model_build():
    mdl = Model("test_model")
    num_h = 24
    cool_max, cool_min, heat_max, heat_min = 20000, 10000, 20000, 10000
    set_price = 20
    ele_price = [1] * 24
    dev = ForthGK(
        num_h, mdl, cool_max, cool_min, heat_max, heat_min, set_price, ele_price
    )
    dev.cons_register(mdl)


def profile():
    os.system(f"rm {fpath}")
    # cProfile.run("test()", filename=fpath)
    cProfile.run("model_build()", filename=fpath)
    # cProfile.run('re.compile("foo|bar")')
    print("after run")


profile() # run this indefinitely
# tout = 20
# print("timeout in %d seconds..." % tout)
# try:
#     func_timeout.func_timeout(tout, profile)
# except func_timeout.FunctionTimedOut:
#     pass
# except Exception as e:
#     raise e

import pstats
# from contextlib import redirect_stderr

log_fpath = "profile.log"
with open(log_fpath, "w+") as f:
    # with redirect_stderr(f):
    p = pstats.Stats(fpath,stream=f)
    p.strip_dirs().sort_stats(2).print_stats()
# os.system(f"type {log_fpath}")
print('write to:', log_fpath)