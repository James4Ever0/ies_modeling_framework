def someFunction(param1, param2, param3=3):
    ...


arg_0 = {"param1": 1}
arg_1 = {"param1": 1, "param2": 2}
arg_2 = {"param1": 1, "param3": 3}
arg_3 = {"param1": 1, "param2": 2, "param3": 3}

args = [arg_0, arg_1, arg_2, arg_3]

for i, arg in enumerate(args):
    try:
        someFunction(**arg)
        print(f"SUCCEED WITH ARG{i}")
    except:
        print(f"FAILED WITH ARG{i}")
