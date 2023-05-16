import pandas

output_path = "microgrid_type_system.xlsx"

class MicrogridPortTypes:
    母线输入 = 0
    母线输出 = 0
    储能端输入输出 = 1
    双向变流器输入输出 = 1
    可连接母线 = 2
    不可连接母线 = 2
    可连接供电端母线 = 3
    不可连接供电端母线 = 3
    可连接储能端母线 = 4
    不可连接储能端母线 = 4
    供电端输出 = 0

T = MicrogridPortTypes
triplets = [(T.可连接供电端母线,,)]

供电端输出, 