# coding = UTF-8

import re
import os
import pickle
import pandas as pd
import numpy as np
from collections import OrderedDict

STEP_ONE_PROVINCE = False
STEP_TWO_GDP = False
STEP_THREE_CAPITAL = False
STEP_FOUR_LABOUR = False
STEP_FILE_HUMANCAPITAL = False
STEP_DATA_TABLE = True

MAIN_PATH = 'D:/data/TFP'
PROVINCE_FILE = os.path.join(MAIN_PATH,'province.xlsx')
GDP_FILE = os.path.join(MAIN_PATH,'GDP.xls')
CAPITAL_FILE = os.path.join(MAIN_PATH,'capital.xlsx')
LABOUR_FILE = os.path.join(MAIN_PATH,'labour.xlsx')
HUMANCAPITAL_FILE = os.path.join(MAIN_PATH,'humancapital.xlsx')

F = open(os.path.join(MAIN_PATH, 'province.pkl'), 'rb')
province_dict = pickle.load(F)

if STEP_ONE_PROVINCE:
    province_id = []
    province_name = []
    province = pd.read_excel(os.path.join(MAIN_PATH, PROVINCE_FILE))
    for item in province['province']:
        item = re.sub('\s+','',item)
        province_id.append(item[0:6])
        province_name.append(item[6:])
    print(province_id,province_name)
    province_dict = OrderedDict(zip(province_name,province_id))
    print(province_dict)
    F = open(os.path.join(MAIN_PATH, 'province.pkl'), 'wb')
    pickle.dump(province_dict, F)
    F.close()

if STEP_TWO_GDP:
    raw_gdp_data = pd.read_excel(os.path.join(MAIN_PATH, GDP_FILE))
    raw_gdp_data.index = range(1978,2015)
    del raw_gdp_data['时间']

    for i in range(len(raw_gdp_data.columns.values)):
        raw_gdp_data.columns.values[i] = province_dict[raw_gdp_data.columns.values[i]]

    gdp_df = pd.DataFrame({'GDP':raw_gdp_data.loc[range(1990,2015),:].stack()})
    index_df = gdp_df.index.to_frame()
    gdp_df = pd.concat([gdp_df,index_df],axis=1)
    gdp_df = gdp_df.rename(index=int, columns={0: 'year', 1: 'region'})

    gdp_df.to_excel(os.path.join(MAIN_PATH,'gdp_df.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'gdp_df.pkl'), 'wb')
    pickle.dump(gdp_df, F)
    F.close()

if STEP_THREE_CAPITAL:
    raw_capital_data = pd.read_excel(os.path.join(MAIN_PATH, CAPITAL_FILE))
    raw_capital_data.index = range(1978, 2016)
    del raw_capital_data['时间']

    for i in range(len(raw_capital_data.columns.values)):
        found = [province_dict[item] for item in province_dict if re.match(raw_capital_data.columns.values[i],item)]
        if len(found) == 1:
            raw_capital_data.columns.values[i] = found[0]

    capital_df = pd.DataFrame({'capital': raw_capital_data.loc[range(1990, 2015), :].stack()})
    index_df = capital_df.index.to_frame()
    capital_df = pd.concat([capital_df, index_df], axis=1)
    capital_df = capital_df.rename(index=int, columns={0: 'year', 1: 'region'})

    print(capital_df)
    capital_df.to_excel(os.path.join(MAIN_PATH, 'capital_df.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'capital_df.pkl'), 'wb')
    pickle.dump(capital_df, F)
    F.close()

if STEP_FOUR_LABOUR:
    raw_labour_data = pd.read_excel(os.path.join(MAIN_PATH, LABOUR_FILE))
    raw_labour_data = raw_labour_data.set_index('region')
    raw_labour_data = raw_labour_data.T
    raw_labour_data.index = range(1985, 2015)
    raw_labour_data.columns.name = None

    for i in range(len(raw_labour_data.columns.values)):
        found = [province_dict[item] for item in province_dict if re.match(raw_labour_data.columns.values[i],item)]
        if len(found) == 1:
            raw_labour_data.columns.values[i] = found[0]

    labour_df = pd.DataFrame({'labour': raw_labour_data.loc[range(1990, 2015), :].stack()})
    index_df = labour_df.index.to_frame()
    labour_df = pd.concat([labour_df, index_df], axis=1)
    labour_df = labour_df.rename(index=int, columns={0: 'year', 1: 'region'})

    print(labour_df)
    labour_df.to_excel(os.path.join(MAIN_PATH, 'labour_df.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'labour_df.pkl'), 'wb')
    pickle.dump(labour_df, F)
    F.close()

if STEP_FILE_HUMANCAPITAL:
    raw_humancapital_data = pd.read_excel(os.path.join(MAIN_PATH, HUMANCAPITAL_FILE))
    raw_humancapital_data.index = range(1990, 2015)

    for i in range(len(raw_humancapital_data.columns.values)):
        found = [province_dict[item] for item in province_dict if re.match(raw_humancapital_data.columns.values[i],item)]
        if len(found) == 1:
            raw_humancapital_data.columns.values[i] = found[0]

    raw_humancapital_data = raw_humancapital_data.sort_index(axis=1)
    humancapital_df = pd.DataFrame({'humancapital': raw_humancapital_data.loc[range(1990, 2015), :].stack()})
    index_df = humancapital_df.index.to_frame()
    humancapital_df = pd.concat([humancapital_df, index_df], axis=1)
    humancapital_df = humancapital_df.rename(index=int, columns={0: 'year', 1: 'region'})

    print(humancapital_df)
    humancapital_df.to_excel(os.path.join(MAIN_PATH, 'humancapital_df.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'humancapital_df.pkl'), 'wb')
    pickle.dump(humancapital_df, F)
    F.close()

if STEP_DATA_TABLE:
    F1 = open(os.path.join(MAIN_PATH, 'gdp_df.pkl'), 'rb')
    gdp_df = pickle.load(F1)

    F2 = open(os.path.join(MAIN_PATH, 'capital_df.pkl'), 'rb')
    capital_df = pickle.load(F2)

    F3 = open(os.path.join(MAIN_PATH, 'labour_df.pkl'), 'rb')
    labour_df = pickle.load(F3)

    F4 = open(os.path.join(MAIN_PATH, 'humancapital_df.pkl'), 'rb')
    humancapital_df = pickle.load(F4)

    data_table = pd.concat([gdp_df, capital_df, labour_df, humancapital_df], axis=1)
    data_table.to_excel(os.path.join(MAIN_PATH, 'data_table.xlsx'))






