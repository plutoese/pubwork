# coding = UTF-8

import numpy as np
import pandas as pd


def regulargrad(attendance, homework, basic=0, attendw=1, homeworkw=1):
    attendance_total = attendance.aggregate(np.sum,axis=1) * attendw
    homework_total = homework.aggregate(np.sum, axis=1) * homeworkw

    total = basic + attendance_total + homework_total
    print(homework_total)
    return total

# 0. Constant
DATA_FILE = r'D:\data\exam\inter_econ.xlsx'

# 1. import data
rdata_table = pd.read_excel(DATA_FILE,header=None)
#print(rdata_table.iloc[8:,3:16])
attendance = rdata_table.iloc[0:,0:4]
homework = rdata_table.iloc[0:,4:7]

#print(attendance)
print(len(homework))
print(homework)

#print(attendance.aggregate(np.sum,axis=1))
regular_score = regulargrad(attendance,homework,basic=0,attendw=0,homeworkw=5)
print(regular_score)
regular_score.to_excel(r'D:\data\exam\inter_econometrics_score.xls')