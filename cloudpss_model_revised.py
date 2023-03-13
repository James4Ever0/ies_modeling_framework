from dataclasses import dataclass

@dataclass
class 设备:
    生产厂商:str
    生产型号:str
    设备额定运行参数:dict
    设备运行约束:dict

class 光伏:
    class 光伏设备额定运行参数