"""
数据显示模块
"""

from typing import Iterable, List
import matplotlib.pyplot as plt
from integratedEnergySystemPrototypes import IntegratedEnergySystem, Model
import os


def plotSingle(
    data: Iterable, title_content: str, save_directory: str = "fig"
):  # 定义画图的规范 自动保存图片
    """
    Plot a single graph with `data` as data and `title_content` as title

    Args:
        data (Iterable): a list of values to be plotted on the x axis
        title_content (str): title to plot on the graph
        save_directory (str): directory to save the images
    """
    fig = plt.figure()
    try:
        if not os.path.exists(save_directory):
            os.mkdir(save_directory)
        plt.plot(data)
        plt.xlabel("Time/h")
        plt.ylabel("Power/kW")
        plt.title(title_content)
        plt.savefig(f"{save_directory}/{title_content}.png")
    except:
        print("ERROR WHILE SAVING PICTURE:",title_content)
    finally:
        plt.close(fig=fig)


def printIntegratedEnergySystemDeviceCounts(
    integratedEnergySystem_device: List[IntegratedEnergySystem], min_value: float = 1e-2
):
    """
    Print all device counts in all kinds of `IntegratedEnergySystem` device sets.

    Args:
        integratedEnergySystem_device (List[IntegratedEnergySystem]): a list of `IntegratedEnergySystem` instances
    """
    print("_________DEVICE_COUNT__________")
    for index, item in enumerate(integratedEnergySystem_device):
        subitems = dir(item)
        print(f"device index: {index}")
        print(f"device class: {type(item).__name__}")
        print()
        print("device inputs:", " ".join(list(item.power_of_inputs.keys())))
        print("device outputs:", " ".join(list(item.power_of_outputs.keys())))
        print()
        for subitem in subitems:
            if "device_count" in subitem and not any(
                [
                    prohibited_keyword in subitem
                    for prohibited_keyword in ["device_count_max", "device_count_min"]
                ]
            ):  # 打印每个类型机组里面的设备数量
                val = item.__dict__[subitem]
                try:
                    value = float(val)
                    if value > min_value:
                        print("value name:", subitem)
                        print("value:", value)
                    else:
                        continue
                    # breakpoint()
                except:
                    continue
        print("_____")
    print("_________DEVICE_COUNT__________")


def printDecisionVariablesFromSolution(model1: Model):
    """
    Print all decision variables, including integer, float and binary variables.

    Args:
        model1 (Model): Model to print decision variables
    """

    print()  # 打印整数可决策变量
    print("___INTEGER DECISION VARIABLES___")
    for variable in model1.iter_integer_vars():
        print("INT", variable, "=", variable.solution_value)
    print("___INTEGER DECISION VARIABLES___")
    print()

    print()  # 打印实数可决策变量
    print("___CONTINUOUS DECISION VARIABLES___")
    for variable in model1.iter_continuous_vars():
        print("CONT", variable, "=", variable.solution_value)
    print("___CONTINUOUS DECISION VARIABLES___")
    print()

    print()  # 打印二进制可决策变量
    print("___BINARY DECISION VARIABLES___")
    for variable in model1.iter_binary_vars():
        print("BIN", variable, "=", variable.solution_value)
    print("___BINARY DECISION VARIABLES___")
    print()
