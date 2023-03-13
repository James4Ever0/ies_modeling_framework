from dataclasses import dataclass
from pydantic import BaseModel

@dataclass
class 设备:
    生产厂商:str
    生产型号:str
    设备额定运行参数:dict
    设备运行约束:dict
    设备经济性参数:dict

class 光伏:
    class 光伏设备额定运行参数(BaseModel):
        光伏板面积
        光电转换效率
    
    class 光伏设备运行约束(BaseModel):
        最大发电功率
        
    class 光伏设备经济性参数(BaseModel):
        采购成本(万元/台)
0.0
固定维护成本(万元/年)
可变维护成本(元/kWh)
0.005
设计寿命(年