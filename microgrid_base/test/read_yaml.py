import yaml

fpath = "test_config.yaml"
import rich

with open(fpath, "r") as file:
    # data = yaml.safe_load(file)
    # rich.print(data)
    # {'db': {'abc': 'def', 'mykey': None, 'myotherkey': None}}
    #################################
    #     {
    #     'db': {
    #         'abc': 'def',
    #         'mykey': None,
    #         'myotherkey': [None, None]
    #     }
    # }