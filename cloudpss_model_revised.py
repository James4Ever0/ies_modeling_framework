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
        功率因数
    
    class 光伏设备运行约束(BaseModel):
        最大发电功率