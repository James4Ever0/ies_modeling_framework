
from pydantic import BaseModel
from pyomo.environ import *

model=ConcreteModel()

class 设备:
    def __init__(self,    model,
    生产厂商:str,
    生产型号:str,
    设备额定运行参数:dict,
    设备运行约束:dict ,# if any
    设备经济性参数:dict, #  if any
    设备工况:dict # OperateParam (vue)
    ):
        


class 光伏(设备):
    def __init__(self,model):
        self.model = model
    def 设备额定运行参数(self,model,光伏板面积:float,光电转换效率:float,功率因数:float,输出功率:float,最大输出功率:float,光照强度:):
        self.model=model
        self.光伏板面积=Var(domain=NonNegativeReals)
        self.光电转换效率=Var(domain=NonNegativeReals)
        self.功率因数=Var(domain=NonNegativeReals)
        self.输出功率=min()
    
    class 设备运行约束(BaseModel):
        最大发电功率:float # (kW)
        
    class 设备经济性参数(BaseModel):
        采购成本:float # (万元/台)
        固定维护成本:float#  (万元/年)
        可变维护成本:float#  (元/kWh)
        设计寿命:float # (年)