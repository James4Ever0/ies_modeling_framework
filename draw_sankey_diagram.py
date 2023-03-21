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
# sankey = Sankey()
# 添加节点

sankey = Sankey().add(
    series_name="毕业生流向",  ###给个桑基宝宝取个名字
    nodes=[
        {"name": "北京"},
        {"name": "湖南"},
        {"name": "清华"},
        {"name": "北大"},
        {"name": "人大"},
        {"name": "浙大"},
        {"name": "复旦"},
        {"name": "中山"},
        {"name": "厦大"},
        {"name": "武大"},
        {"name": "川大"},
        {"name": "工作1"},
        {"name": "工作2"},
        {"name": "工作3"},
        {"name": "工作4"},
    ],  ##配置有多少个节点
    links=[
        {"source": "北京", "target": "清华", "value": 50},
        {"source": "北京", "target": "北大", "value": 60},
        {"source": "北京", "target": "人大", "value": 40},
        {"source": "北京", "target": "复旦", "value": 60},
        {"source": "北京", "target": "中山", "value": 30},
        {"source": "北京", "target": "浙大", "value": 33},
        {"source": "北京", "target": "厦大", "value": 22},
        {"source": "北京", "target": "武大", "value": 5},
        {"source": "北京", "target": "川大", "value": 12},
        {"source": "湖南", "target": "清华", "value": 30},
        {"source": "湖南", "target": "北大", "value": 40},
        {"source": "湖南", "target": "人大", "value": 20},
        {"source": "湖南", "target": "复旦", "value": 40},
        {"source": "湖南", "target": "中山", "value": 10},
        {"source": "湖南", "target": "浙大", "value": 13},
        {"source": "湖南", "target": "厦大", "value": 9},
        {"source": "湖南", "target": "武大", "value": 30},
        {"source": "湖南", "target": "川大", "value": 25},
        {"source": "清华", "target": "工作1", "value": 80},
        {"source": "北大", "target": "工作3", "value": 100},
        {"source": "人大", "target": "工作2", "value": 60},
        {"source": "复旦", "target": "工作2", "value": 100},
        {"source": "中山", "target": "工作4", "value": 40},
        {"source": "浙大", "target": "工作3", "value": 46},
        {"source": "厦大", "target": "工作4", "value": 31},
        {"source": "武大", "target": "工作3", "value": 35},
        {"source": "川大", "target": "工作2", "value": 37},
    ],  ###配置节点之间的信息流关系
    linestyle_opt=opts.LineStyleOpts(
        opacity=0.2,  ###透明度设置
        curve=0.5,  ###信息流的曲线弯曲度设置
        color="source",  ##颜色设置，source表示使用节点的颜色
    ),  ##线条格式 ,设置所有线条的格式
    label_opts=opts.LabelOpts(
        font_size=16, position="left"
    ),  ##标签配置，具体参数详见opts.LabelOpts()
    levels=[
        opts.SankeyLevelsOpts(
            depth=0,  ##第一层的配置
            itemstyle_opts=opts.ItemStyleOpts(color="#fbb4ae"),  ##节点格式的配置
            linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.2, curve=0.5),
        ),  ##信息流的配置
        opts.SankeyLevelsOpts(
            depth=1,  ##第二层的配置
            itemstyle_opts=opts.ItemStyleOpts(color="#b3cde3"),  ##节点格式的配置
            linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.2, curve=0.5),
        ),  ##信息的配置
        opts.SankeyLevelsOpts(
            depth=2,  ##第三层的配置
            itemstyle_opts=opts.ItemStyleOpts(color="#ccebc5"),  ##节点格式的配置
            linestyle_opts=opts.LineStyleOpts(color="source", opacity=0.2, curve=0.5),
        ),  ##信息的配置
    ],  # 桑基图每一层的设置。可以逐层设置
)

# 绘制能流桑基图
# sankey.render("energy_flow_sankey.html")
from snapshot_phantomjs import snapshot as driver
from pyecharts.render import make_snapshot

make_snapshot(driver, sankey.render(), "sankey.png")
