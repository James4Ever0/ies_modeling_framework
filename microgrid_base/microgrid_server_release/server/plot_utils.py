from pyecharts.charts import Graph
from pyecharts.options import InitOpts

from json import load
from log_utils import logger_print

extract_data_key = "mDictList"


def plotSingleTopology(data: dict, output_path: str, index=0):
    devices = data[extract_data_key][index]["nodes"]
    connections = data[extract_data_key][index]["links"]
    categories = [{}, {"name": "设备"}, {"name": "母线"}, {"name": "锚点"}, {"name": "其他"}]

    # 创建节点列表
    nodes = []
    for device in devices:
        if device["type"] == "设备":
            device["name"] = f"{device['subtype']} {device.get('id')}"
            device["symbol"] = "diamond"
            device["symbolSize"] = [100, 30]
            device["category"] = 1
        elif device["type"] == "母线":
            device["name"] = f"{device['type']} {device.get('id')}"
            device["symbol"] = "circle"
            device["symbolSize"] = 50
            device["category"] = 2
        elif device["type"] == "锚点":
            device["name"] = f"{device['port_name']} {device.get('id')}"
            device["symbol"] = "pin"
            device["symbolSize"] = 40
            device["category"] = 3
        else:
            device["name"] = f"{device['type']} {device.get('id')}"
            device["symbol"] = "roundRect"
            device["symbolSize"] = [50, 5]
            device["category"] = 4
        nodes.append(device)
    # 创建连接线列表
    links = []
    for connection in connections:
        connection["symbol"] = ["arrow"]
        connection["lineStyle"] = {"width": 2}
        links.append(connection)

    graph = Graph(init_opts=InitOpts(height="900px", width="1000px", bg_color="white"))
    graph.add("", nodes, links, repulsion=1000, categories=categories)
    logger_print(f"graph #{index} saved to {output_path}")
    graph.render(output_path)


import os


def plotMultipleTopologies(data: dict, output_dir: str):
    for i in range(len(data[extract_data_key])):
        output_path = os.path.join(output_dir, f"plot_{i}.html")
        plotSingleTopology(data, output_path, i)


def plotMultipleTopologiesFromFile(input_path: str, output_dir: str):
    logger_print(f"plotting topologies from file '{input_path}'")
    with open(input_path, "r") as f:
        data = load(f.read())
    plotMultipleTopologies(data, output_dir)
