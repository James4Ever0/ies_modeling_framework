import pandas as pd

excel_name = "6节点热网动态data.xls"

sheet_names = ['Node','Branch','Device','Dynamic']

for sheet_name in sheet_names:
    df=pd.read_excel(excel_name, sheet_name=sheet_name)
    print(df.head())
    print()
    save_name = f'{excel_name.split(".")[0]}_{sheet_name}.csv'
    df.to_csv(save_name)
    # with open(save_name,'w+') as f:
    #     f.write(content)