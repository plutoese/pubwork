# coding = UTF-8

import os
import pandas as pd


MAIN_PATH = 'D:/data/TFP'
PROVINCE_DATA_FILE = os.path.join(MAIN_PATH,'data_table.xlsx')

province_data = pd.read_excel(os.path.join(MAIN_PATH, PROVINCE_DATA_FILE))

province_data['perGDP'] = 1000000 * province_data['GDP'] / province_data['labour']
province_data['perCapital'] = 1000000 * province_data['capital'] / province_data['labour']
province_data['perHumancapital'] = 100 * province_data['humancapital'] / province_data['labour']

province_data_1990 = province_data[province_data['year']<1991]
province_data_2014 = province_data[province_data['year']>2013]
province_data_1990 = province_data_1990.set_index('region')
province_data_2014 = province_data_2014.set_index('region')
province_data_2014['perGDPgrwoth'] = province_data_2014['perGDP'] / province_data_1990['perGDP'] - 1
province_data_2014['perCapitalgrwoth'] = province_data_2014['perCapital'] / province_data_1990['perCapital'] - 1
province_data_2014['perHumancapitalgrowth'] = province_data_2014['perHumancapital'] / province_data_1990['perHumancapital'] - 1

province_data_2014['initperGDP'] = province_data_1990['perGDP']

print(province_data)
print(province_data_1990)
print(province_data_2014)
print(province_data_2014['perGDP'] / province_data_1990['perGDP'])

province_data_2014.to_excel(os.path.join(MAIN_PATH, 'prov_data.xls'))
