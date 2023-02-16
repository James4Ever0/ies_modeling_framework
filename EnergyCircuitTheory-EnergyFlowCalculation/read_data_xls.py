import pandas
import os

files = os.listdir(".")

for filepath in files:
    if filepath.endswith(".xls"):
        print(f"reading excel: {filepath}")
        df = pandas.read_excel(filepath)
        # print(df.head())
        print(df)
        print()
        csv_text = df.to_csv()
        csv_filename = filepath.replace(".xls",'.csv')
        with open(csv_filename,'w+',encoding='utf-8') as f:
            f.write(csv_text)