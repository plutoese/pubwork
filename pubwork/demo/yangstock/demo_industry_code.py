# coding = UTF-8

import os
import pandas as pd
import pickle


# 0. Initialization
MAIN_PATH = 'F:/roombackup/dataset/yangstock'
STOCK_INDUSTRY_CODE1 = os.path.join(MAIN_PATH,'（含行业信息）2004年9月-2016年6月上市公司行业分类情况.xls')
STOCK_INDUSTRY_CODE2 = os.path.join(MAIN_PATH,'（按最新股票名称）1992年5月24日-2016年6月30日上市公司行业分类情况.xls')
STOCK_HOLDER_TABLE = os.path.join(MAIN_PATH,'stock_holder_more_df.pkl')
ORIGIN_FINAL_TABLE = os.path.join(MAIN_PATH, 'final_table_3.pkl')

'''
raw_stock_industry_code1 = pd.read_excel(STOCK_INDUSTRY_CODE1)
raw_stock_industry_code2 = pd.read_excel(STOCK_INDUSTRY_CODE2)

# construct industry code dict
stock_industry_code1 = raw_stock_industry_code1[['上市公司代码_ComCd', '证监会行业代码_CsrcICCd']]
stock_industry_code1 = stock_industry_code1.set_index('上市公司代码_ComCd')
stock_industry_code_dict = stock_industry_code1.to_dict()['证监会行业代码_CsrcICCd']

stock_industry_code2 = raw_stock_industry_code2[['上市公司代码_ComCd', '证监会行业代码_CsrcICCd']]
stock_industry_code2 = stock_industry_code2.set_index('上市公司代码_ComCd')
stock_industry_code_dict2 = stock_industry_code2.to_dict()['证监会行业代码_CsrcICCd']

print(len(stock_industry_code_dict), len(stock_industry_code_dict2))

for key in stock_industry_code_dict2:
    if key not in stock_industry_code_dict:
        stock_industry_code_dict.update({key: stock_industry_code_dict2[key]})

print(len(stock_industry_code_dict))

F = open(os.path.join(MAIN_PATH, 'industry_code.pkl'), 'wb')
pickle.dump(stock_industry_code_dict, F)'''

industry_code = pd.read_pickle(os.path.join(MAIN_PATH, 'industry_code.pkl'))
print(len(industry_code))