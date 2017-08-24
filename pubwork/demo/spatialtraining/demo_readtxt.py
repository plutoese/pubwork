# coding = UTF-8

import pandas as pd

x = pd.read_table(r'D:\data\spatial\industry\dingM.txt', sep='\s+',header=None)

x = x.set_index([0])
x.columns = x.index

print(x.columns)

x.to_excel(r'D:\data\spatial\industry\dingM.xlsx')