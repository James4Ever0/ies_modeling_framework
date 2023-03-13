from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class 设备:
    生产厂商:str
    生产型号:str
    设备额定运行参数:dict
    设备运行约束:dict #
    设备经济性参数:dict # 
    设备工况:dict # OperateParam (vue)

class 光伏(设备):
    class 设备额定运行参数(BaseModel):
        光伏板面积 # 
        光电转换效率 # 
    
    class 设备运行约束(BaseModel):
        最大发电功率:float # (kW)
        
    class 设备经济性参数(BaseModel):
        采购成本:float # (万元/台)
        固定维护成本:float#  (万元/年)
        可变维护成本:float#  (元/kWh)
        设计寿命:float # (年)