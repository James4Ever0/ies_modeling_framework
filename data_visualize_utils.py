
from typing import Iterable,List
import matplotlib.pyplot as plt
from cpExample import IntegratedEnergySystem,Model

def plotSingle(data:Iterable, title_content:str): # 定义画图的规范 自动保存图片
    """
    """
    fig = plt.figure()
    plt.plot(data)
    plt.xlabel("Time/h")
    plt.ylabel("Power/kW")
    plt.title(title_content)
    plt.savefig("fig/" + title_content + ".png")
    plt.close(fig=fig)

def printIntegratedEnergySystemDeviceCounts(integratedEnergySystem_device:List[IntegratedEnergySystem]):
    """
    """
    print("_________DEVICE_COUNT__________")
    for index, item in enumerate(integratedEnergySystem_device):
        subitems = dir(item)
        print(f"objective index: {index}")
        print(f"objective class: {type(item).__name__}")
        for subitem in subitems:
            if subitem.endswith("_device"): # 打印每个类型机组里面的设备数量
                val = item.__dict__[subitem]
                print("value name:", subitem)
                print("value:", val)
        print("_____")
    print("_________DEVICE_COUNT__________")

def printDecisionVariablesFromSolution(model1:Model):
    """
    Print all decision variables, including integer, float and binary variables.
    
    Args:
        model1 (Model): Model to print decision variables
    """
    
    print() # 打印整数可决策变量
    print("___INTEGER DECISION VARIABLES___")
    for variable in model1.iter_integer_vars():
        print("INT", variable, "=", variable.solution_value)
    print("___INTEGER DECISION VARIABLES___")
    print()

    print() # 打印实数可决策变量
    print("___CONTINUOUS DECISION VARIABLES___")
    for variable in model1.iter_continuous_vars():
        print("CONT", variable, "=", variable.solution_value)
    print("___CONTINUOUS DECISION VARIABLES___")
    print()

    print() # 打印二进制可决策变量
    print("___BINARY DECISION VARIABLES___")
    for variable in model1.iter_binary_vars():
        print("BIN", variable, "=", variable.solution_value)
    print("___BINARY DECISION VARIABLES___")
    print()