# coding = UTF-8

import numpy as np
import pandas as pd


def regulargrad(attendance, homework, basic=0, attendw=1, homeworkw=1):
    attendance_total = attendance.aggregate(np.sum,axis=1) * attendw
    homework_total = homework.aggregate(np.sum, axis=1) * homeworkw

    total = basic + attendance_total + homework_total
    return total

# 0. Constant
DATA_FILE = r'D:\data\exam\statistics.xls'

# 1. import data
rdata_table = pd.read_excel(DATA_FILE)
#print(rdata_table.iloc[8:,3:16])
attendance = rdata_table.iloc[8:,3:7]
homework = rdata_table.iloc[8:,11:15]

print(attendance)
print(homework)


#print(attendance.aggregate(np.sum,axis=1))
regular_score = regulargrad(attendance,homework,basic=48,attendw=5,homeworkw=2)
print(regular_score)
regular_score.to_excel(r'D:\data\exam\statistics_score.xls')