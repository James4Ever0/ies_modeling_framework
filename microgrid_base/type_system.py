
import pandas

output_path = "microgrid_type_system.xlsx"

class MicrogridPortTypes:
    供电端输出
    母线输入
    母线输出
    储能端输入输出
    双向变流器输入输出
    可连接母线
    不可连接母线
    可连接供电端母线
    不可连接供电端母线
    可连接储能端母线
    不可连接储能端母线