import matplotlib.pyplot as plt
import pandas as pd
from pysankey2.datasets import load_fruits
from pysankey2 import Sankey

df = load_fruits()
sky = Sankey(df,colorMode="global")
fig,ax = sky.plot()