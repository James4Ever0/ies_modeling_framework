# %%
# import data from dataset, or from termbin?
# termbin instead? since we are running on two computers.

# first let's spin up some RWKV model on CPU.
# !curl -o device_params.json https://termbin.com/766n

# you cannot use gpu on this machine.
# cpu is too damn slow.

# %%
import json

with open('device_params.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())

# %%
# you can use other models as well. as long as you like.
# but first let's define the prompt.

prompt_template = lambda device_type, device_name, device_params: f"""

为了建模需要，对设备参数进行确定。

设备类型: {device_type}

设备名称: {device_name}

设备参数: 

{device_params}

根据参数内容提出你的质疑，可以质疑其中参数的单位，提出对于非必填参数如何参与计算的质疑（如何在不填写非必填参数和填写非必填参数的两种情况下计算出结果），提出是不是应该删除其中的某些参数，增加新的参数，以及对参数增加和删除合理性的质疑。

"""



# %%
# IGNORE EXAMPLE DATA, WHICH IS THE SECOND ELEM.
# import os
output_path = "output_auto_questions.log"

# since it is slow we don't overwrite.
# if os.path.exists(output_path):
#     os.remove(output_path)

def fprint(f, content):
    f.write(content)
    f.write('\n')
    print(content)

import pyperclip

with open(output_path,'a+', encoding='utf-8') as f:
    for device_type, devices in data.items():
        for device_name, device_param_list in devices.items():
            device_params = []
            for a, _, c in device_param_list:
                if c is None:
                    c = ""
                device_params.append(f"    {a} {c}")
            device_params = "\n".join(device_params)
            question = prompt_template(device_type,device_name,device_params)
            fprint(f,"*"*20+"QUESTION"+"*"*20)
            fprint(f,question)
            pyperclip.copy(question)
            fprint(f,"*"*20+"ANSWER"+"*"*20)
            input("CONTINUE?")
            answer = pyperclip.paste()
            fprint(f, answer)
    #         answer = evaluate(get_request(question), *invokeParams[0])
    #         print(answer)
    # SHALL BE ANSWER HERE.


