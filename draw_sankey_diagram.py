# no weights. deprecated.

# import matplotlib.pyplot as plt
# import pandas as pd
# from pysankey2.datasets import load_fruits
# from pysankey2 import Sankey

# df = load_fruits()
# sky = Sankey(df,colorMode="global")
# fig,ax = sky.plot()

from pyecharts.charts import Sankey
from pyecharts import options as opts
# 构建能流桑基图
sankey = Sankey()
# 添加节点
sankey.add("能量流", 
           nodes=["电力", "热力", "氢能", "燃料", "负荷", "储能", "光伏", "风力", "太阳能"],
           # 指定节点样式
           itemstyle_opts=opts.ItemStyleOpts(border_width=0, border_color="#aaa"),
# 添加边
           # 每条边的起点和终点
           links=[{"source": "电力", "target": "负荷", "value": 200},
                  {"source": "电力", "target": "储能", "value": 50},
                  {"source": "热力", "target": "负荷", "value": 100},
                  {"source": "燃料", "target": "电力", "value": 150},
                  {"source": "燃料", "target": "热力", "value": 100},
                  {"source": "氢能", "target": "燃料", "value": 50},
                  {"source": "光伏", "target": "电力", "value": 50},
                  {"source": "风力", "target": "电力", "value": 50},
                  {"source": "太阳能", "target": "电力", "value": 50}],
           # 指定边的样式
           linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color="source")
           )
# 设置全局样式
sankey.set_global_opts(title_opts=opts.TitleOpts(title="能流桑基图"),
                       tooltip_opts=opts.TooltipOpts(trigger="item", trigger_on="mousemove|click"),
                       visualmap_opts=opts.VisualMapOpts(is_piecewise=True,
                                                         pieces=[{"max": 300}, {"min": 100, "max": 200}, {"min": 10, "max": 100}]))
# 绘制能流桑基图
# sankey.render("energy_flow_sankey.html")
from snapshot_phantomjs import snapshot as driver
from pyecharts.render import make_snapshot
make_snapshot(driver, sankey.render(), "sankey.png")