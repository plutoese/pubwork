# coding = UTF-8


import os
import re
import datetime
import pickle
import pandas as pd
import numpy as np

STEP_IMPORT_EMPLOYEE = False
CLEANING_EMPLOYEE = False
SETP_IMPORT_PROFIT = False
STEP_IMPORT_CASH = False
STEP_IMPORT_PROPERTY = False

STEP_MERGE_EMPLOYEE_PROFIT_CASH_PROPERTY = False
SETP_INDUSTRY_CODE_ADD = False
STEP_STOCK_HOLDER = False
STEP_STOCK_HOLDER_CLEANING = False
STEP_STOCK_HOLDER_REORGANIZING = False
STEP_FOUR_TABLE_WITH_STOCK_HOLDER = False
STEP_STATE_OWNED_DATA = False
STEP_CREATE_CHS2 = False
STEP_STOCKER_HOLDER_MORE = False
STEP_CREATE_CHS1 = False
STEP_MERGE_FINAL_TABLE = True

MAIN_PATH = 'F:/room/dataset/yangstock'
EMPLOYEE_PATH = os.path.join(MAIN_PATH,'2005-2016上市公司员工信息')
PROFIT_PATH = os.path.join(MAIN_PATH,'利润分配表2005-2016主要指标.xls')
CASH_PATH = os.path.join(MAIN_PATH,'现金流量表2005-2016主要指标.xls')
PROPERTY_PATH_1 = os.path.join(MAIN_PATH,'资产负债表2005-2016主要指标（1）.xls')
PROPERTY_PATH_2 = os.path.join(MAIN_PATH,'资产负债表2005-2016主要指标（2）.xls')
STOCK_HOLDER_PATH = os.path.join(MAIN_PATH,'持股数据主表-2005-2016年我国上市公司交叉持股情况.xls')
STOCK_INDUSTRY_CODE1 = os.path.join(MAIN_PATH,'（含行业信息）2004年9月-2016年6月上市公司行业分类情况.xls')
STOCK_INDUSTRY_CODE2 = os.path.join(MAIN_PATH,'（按最新股票名称）1992年5月24日-2016年6月30日上市公司行业分类情况.xls')
STATE_OWNED_STOCKER_HOLDER = os.path.join(MAIN_PATH,'（汇总数据）年度报告-国有股东-2005-2016年主要股东名单与股权结构.xls')


def datematcher(col, month=12, day=31):
    return col.apply(lambda x: (x.month == month) and (x.day == day))


def qmatcher(col, q='Q4'):
    return col.apply(lambda x: x == q)


# 1. 导入员工信息数据
if STEP_IMPORT_EMPLOYEE:
    i = 1
    for file in os.listdir(EMPLOYEE_PATH):
        employee_data = pd.read_excel(os.path.join(EMPLOYEE_PATH,file))
        grouped = employee_data[['上市公司代码_ComCd','截止日期_EndDt','员工数_EmpNum']].groupby(['上市公司代码_ComCd','截止日期_EndDt'],as_index=False)
        result = pd.merge(employee_data, grouped.agg(np.max), how='inner', on=['上市公司代码_ComCd','截止日期_EndDt','员工数_EmpNum'])
        if i == 1:
            employee_pdata = result
        else:
            employee_pdata = pd.concat([employee_pdata, result])
        i += 1
    # 输出员工信息数据
    employee_pdata= employee_pdata.loc[datematcher(employee_pdata['截止日期_EndDt'], month=12, day=31)]
    employee_pdata.to_excel(os.path.join(MAIN_PATH,'output_employee.xlsx'))
    F = open(os.path.join(MAIN_PATH,'output_employee.pkl'), 'wb')
    pickle.dump(employee_pdata, F)
    F.close()

if CLEANING_EMPLOYEE:
    F = open(os.path.join(MAIN_PATH,'output_employee.pkl'), 'rb')
    organized_employee_data = pickle.load(F)

if SETP_IMPORT_PROFIT:
    raw_profit_data = pd.read_excel(PROFIT_PATH)
    organized_profit_data = raw_profit_data.loc[qmatcher(raw_profit_data['信息来源标识_InfoSourceFlg'])]
    organized_profit_data.to_excel(os.path.join(MAIN_PATH,'output_profit.xlsx'))
    F = open(os.path.join(MAIN_PATH,'output_profit.pkl'), 'wb')
    pickle.dump(organized_profit_data, F)
    F.close()

if STEP_IMPORT_CASH:
    raw_cash_data = pd.read_excel(CASH_PATH)
    #print(raw_cash_data.shape)
    #print(raw_cash_data.loc[datematcher(raw_cash_data['截止日期_EndDt'], month=12, day=31)].shape)
    #print(raw_cash_data.loc[qmatcher(raw_cash_data['信息来源标识_InfoSourceFlg'])].shape)
    organized_cash_data = raw_cash_data.loc[qmatcher(raw_cash_data['信息来源标识_InfoSourceFlg'])]
    organized_cash_data.to_excel(os.path.join(MAIN_PATH,'output_cash.xlsx'))
    F = open(os.path.join(MAIN_PATH,'output_cash.pkl'), 'wb')
    pickle.dump(organized_cash_data, F)
    F.close()

if STEP_IMPORT_PROPERTY:
    raw_property_data1 = pd.read_excel(PROPERTY_PATH_1)
    raw_property_data2 = pd.read_excel(PROPERTY_PATH_2)

    #print(raw_property_data1.shape)
    #print(raw_property_data1.loc[datematcher(raw_property_data1['截止日期_EndDt'], month=12, day=31)].shape)
    #print(raw_property_data2.loc[qmatcher(raw_property_data2['信息来源标识_InfoSourceFlg'])].shape)

    organized_property_data1 = raw_property_data1.loc[qmatcher(raw_property_data1['信息来源标识_InfoSourceFlg'])]
    organized_property_data2 = raw_property_data2.loc[qmatcher(raw_property_data2['信息来源标识_InfoSourceFlg'])]

    organized_property_data = pd.concat([organized_property_data1,organized_property_data2])

    organized_property_data.to_excel(os.path.join(MAIN_PATH,'output_property.xlsx'))
    F = open(os.path.join(MAIN_PATH,'output_property.pkl'), 'wb')
    pickle.dump(organized_property_data, F)
    F.close()

if STEP_MERGE_EMPLOYEE_PROFIT_CASH_PROPERTY:
    F = open(os.path.join(MAIN_PATH,'output_employee.pkl'), 'rb')
    organized_employee_data = pickle.load(F)

    organized_employee_data['mid'] = organized_employee_data['上市公司代码_ComCd'].apply(lambda x:str(x)).str.cat(organized_employee_data['截止日期_EndDt'].apply(lambda x:str(x.year)))
    #print(organized_employee_data.shape)
    #print(organized_employee_data.drop_duplicates('mid').shape)
    organized_employee_data = organized_employee_data.drop_duplicates('mid')
    del organized_employee_data['mid']

    F = open(os.path.join(MAIN_PATH, 'output_profit.pkl'), 'rb')
    organized_profit_data = pickle.load(F)

    organized_profit_data['mid'] = organized_profit_data['上市公司代码_ComCd'].apply(lambda x: str(x)).str.cat(organized_profit_data['截止日期_EndDt'].apply(lambda x: str(x.year)))
    organized_profit_data = organized_profit_data.drop_duplicates('mid')
    del organized_profit_data['mid']

    F = open(os.path.join(MAIN_PATH, 'output_cash.pkl'), 'rb')
    organized_cash_data = pickle.load(F)

    organized_cash_data['mid'] = organized_cash_data['上市公司代码_ComCd'].apply(lambda x: str(x)).str.cat(organized_cash_data['截止日期_EndDt'].apply(lambda x: str(x.year)))
    organized_cash_data = organized_cash_data.drop_duplicates('mid')
    del organized_cash_data['mid']

    F = open(os.path.join(MAIN_PATH, 'output_property.pkl'), 'rb')
    organized_property_data = pickle.load(F)

    organized_property_data['mid'] = organized_property_data['上市公司代码_ComCd'].apply(lambda x: str(x)).str.cat(organized_property_data['截止日期_EndDt'].apply(lambda x: str(x.year)))
    organized_property_data = organized_property_data.drop_duplicates('mid')
    del organized_property_data['mid']

    print(organized_employee_data.shape, organized_profit_data.shape, organized_cash_data.shape, organized_property_data.shape)

    # merge
    result = pd.merge(organized_employee_data,organized_profit_data,how='outer',on=['上市公司代码_ComCd','截止日期_EndDt'])
    result = pd.merge(result,organized_cash_data,how='outer',on=['上市公司代码_ComCd','截止日期_EndDt'])
    result = pd.merge(result,organized_property_data,how='outer',on=['上市公司代码_ComCd','截止日期_EndDt'])
    print(result.shape)
    result['myenddate'] = result['截止日期_EndDt'].apply(lambda x: x.year)

    result.to_excel(os.path.join(MAIN_PATH, 'result1.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'output_fourtable.pkl'), 'wb')
    pickle.dump(result, F)
    F.close()

if SETP_INDUSTRY_CODE_ADD:
    F = open(os.path.join(MAIN_PATH, 'output_fourtable.pkl'), 'rb')
    raw_four_table = pickle.load(F)

    raw_stock_holder = pd.read_excel(STOCK_HOLDER_PATH)
    raw_stock_industry_code1 = pd.read_excel(STOCK_INDUSTRY_CODE1)
    raw_stock_industry_code2 = pd.read_excel(STOCK_INDUSTRY_CODE2)

    # construct industry code dict
    stock_industry_code1 = raw_stock_industry_code1[['上市公司代码_ComCd', '证监会行业代码_CsrcICCd']]
    stock_industry_code1 = stock_industry_code1.set_index('上市公司代码_ComCd')
    stock_industry_code_dict = stock_industry_code1.to_dict()['证监会行业代码_CsrcICCd']

    # construct industry code dict
    stock_industry_code2 = raw_stock_industry_code2[['上市公司代码_ComCd', '证监会行业代码_CsrcICCd']]
    stock_industry_code2 = stock_industry_code2.set_index('上市公司代码_ComCd')
    stock_industry_code_dict2 = stock_industry_code2.to_dict()['证监会行业代码_CsrcICCd']
    print(len(stock_industry_code_dict), len(stock_industry_code_dict2))
    for key in stock_industry_code_dict2:
        if key not in stock_industry_code_dict:
            stock_industry_code_dict.update({key: stock_industry_code_dict2[key]})

    raw_four_table['industry_code'] = raw_four_table['上市公司代码_ComCd'].apply(lambda x:stock_industry_code_dict.get(x))

    raw_four_table.to_excel(os.path.join(MAIN_PATH, 'result1_with_code.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'output_fourtable_with_code.pkl'), 'wb')
    pickle.dump(raw_four_table, F)
    F.close()

if STEP_STOCK_HOLDER:
    raw_stock_holder = pd.read_excel(STOCK_HOLDER_PATH)
    raw_stock_industry_code1 = pd.read_excel(STOCK_INDUSTRY_CODE1)
    raw_stock_industry_code2 = pd.read_excel(STOCK_INDUSTRY_CODE2)

    #print(raw_stock_holder.columns)
    #print(raw_stock_holder[raw_stock_holder['股东上市公司代码_SHComCd'].notnull()]['股东上市公司代码_SHComCd'].shape)

    # construct industry code dict
    stock_industry_code1 = raw_stock_industry_code1[['上市公司代码_ComCd','证监会行业代码_CsrcICCd']]
    stock_industry_code1 = stock_industry_code1.set_index('上市公司代码_ComCd')
    stock_industry_code_dict = stock_industry_code1.to_dict()['证监会行业代码_CsrcICCd']

    # construct industry code dict
    stock_industry_code2 = raw_stock_industry_code2[['上市公司代码_ComCd', '证监会行业代码_CsrcICCd']]
    stock_industry_code2 = stock_industry_code2.set_index('上市公司代码_ComCd')
    stock_industry_code_dict2 = stock_industry_code2.to_dict()['证监会行业代码_CsrcICCd']
    print(len(stock_industry_code_dict),len(stock_industry_code_dict2))
    for key in stock_industry_code_dict2:
        if key not in stock_industry_code_dict:
            stock_industry_code_dict.update({key:stock_industry_code_dict2[key]})
    #print(len(stock_industry_code_dict))

    keep_index = []
    for ind in raw_stock_holder[raw_stock_holder['股东上市公司代码_SHComCd'].notnull()].index:
        owner_code = stock_industry_code_dict.get(raw_stock_holder.loc[ind,'上市公司代码_ComCd'])
        holder_code = stock_industry_code_dict.get(raw_stock_holder.loc[ind,'股东上市公司代码_SHComCd'])
        if (owner_code is not None) and (holder_code is not None):
            if owner_code == holder_code:
                #print(owner_code,holder_code)
                keep_index.append(ind)
    #print(len(keep_index))

    #print(raw_stock_holder.loc[keep_index,].shape)
    raw_stock_holder.loc[keep_index,].to_excel(os.path.join(MAIN_PATH, 'result_tmp.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'cross_stock_holder.pkl'), 'wb')
    pickle.dump(raw_stock_holder.loc[keep_index,], F)
    F.close()

if STEP_STOCK_HOLDER_CLEANING:
    F = open(os.path.join(MAIN_PATH, 'cross_stock_holder.pkl'), 'rb')
    raw_cross_stock_holder = pickle.load(F)
    print(raw_cross_stock_holder.shape, raw_cross_stock_holder.columns)

    n = 0
    for ind in raw_cross_stock_holder.index:
        print(raw_cross_stock_holder.loc[ind, '关联起始日_RelStartDt'],raw_cross_stock_holder.loc[ind, '关联截止日_RelEndDt'])
        if isinstance(raw_cross_stock_holder.loc[ind, '关联起始日_RelStartDt'],pd.tslib.NaTType) and isinstance(raw_cross_stock_holder.loc[ind, '关联截止日_RelEndDt'],pd.tslib.NaTType):
            continue

        if isinstance(raw_cross_stock_holder.loc[ind, '关联起始日_RelStartDt'],pd.tslib.NaTType):
            start_date = datetime.datetime(2005,1,1)
            end_date = raw_cross_stock_holder.loc[ind, '关联截止日_RelEndDt']
        elif isinstance(raw_cross_stock_holder.loc[ind, '关联截止日_RelEndDt'],pd.tslib.NaTType):
            start_date = raw_cross_stock_holder.loc[ind, '关联起始日_RelStartDt']
            end_date = datetime.datetime(2016,12,31)
        else:
            start_date = raw_cross_stock_holder.loc[ind, '关联起始日_RelStartDt']
            end_date = raw_cross_stock_holder.loc[ind, '关联截止日_RelEndDt']

        if start_date <  datetime.datetime(2005,1,1):
            start_date = datetime.datetime(2005,1,1)
        if end_date >  datetime.datetime(2016,12,31):
            start_date = datetime.datetime(2016,12,31)

        print('-------------',start_date,' ---> ',end_date,'-------------')
        i = 0
        while end_date > start_date:
            if (end_date - start_date) >= pd.Timedelta('365 days'):
                days = datetime.datetime(start_date.year,12,31) - start_date + pd.Timedelta('1 days')
                print('ppppp',days.days)
                if days <= pd.Timedelta('1 days'):
                    days = datetime.datetime(start_date.year+1,12,31) - start_date
                    print('left',days)
                    sign_end_date = datetime.datetime(start_date.year+1, 12, 31)
                else:
                    sign_end_date = datetime.datetime(start_date.year,12,31)
                start_date = sign_end_date + pd.Timedelta('1 days')
                print('nnnn', end_date, start_date, sign_end_date, start_date)
                if i == 0:
                    one_stock_df = raw_cross_stock_holder.loc[ind].copy()
                    one_stock_df['myenddate'] = sign_end_date.year
                    one_stock_df['mydays'] = days.days
                    one_stock_df = one_stock_df.to_frame().transpose()
                else:
                    one_tmp_stock_df = raw_cross_stock_holder.loc[ind].copy()
                    one_tmp_stock_df['myenddate'] = sign_end_date.year
                    one_tmp_stock_df['mydays'] = days.days
                    one_tmp_stock_df = one_tmp_stock_df.to_frame().transpose()
                    one_stock_df = pd.concat([one_stock_df,one_tmp_stock_df])
            else:
                days = datetime.datetime(start_date.year, 12, 31) - start_date + pd.Timedelta('1 days')
                if days <= pd.Timedelta('1 days'):
                    days = end_date - start_date
                    sign_end_date = datetime.datetime(end_date.year, 12, 31)
                    start_date = end_date + pd.Timedelta('1 days')
                else:
                    if start_date.year < end_date.year:
                        days = datetime.datetime(start_date.year, 12, 31) - start_date + pd.Timedelta('1 days')
                        sign_end_date = datetime.datetime(start_date.year, 12, 31)
                        start_date = sign_end_date + pd.Timedelta('1 days')
                    else:
                        days = end_date - start_date + pd.Timedelta('1 days')
                        sign_end_date = datetime.datetime(end_date.year, 12, 31)
                        start_date = end_date + pd.Timedelta('1 days')
                print('ppp', start_date, end_date, days, type(days), days.days)
                #start_date = start_date + pd.Timedelta('365 days')
                if i == 0:
                    one_stock_df = raw_cross_stock_holder.loc[ind].copy()
                    one_stock_df['myenddate'] = sign_end_date.year
                    one_stock_df['mydays'] = days.days
                    one_stock_df = one_stock_df.to_frame().transpose()
                else:
                    one_tmp_stock_df = raw_cross_stock_holder.loc[ind].copy()
                    one_tmp_stock_df['myenddate'] = sign_end_date.year
                    one_tmp_stock_df['mydays'] = days.days
                    one_tmp_stock_df = one_tmp_stock_df.to_frame().transpose()
                    one_stock_df = pd.concat([one_stock_df, one_tmp_stock_df])
            i += 1
        if n == 0:
            stock_holder_df = one_stock_df
        else:
            stock_holder_df = pd.concat([stock_holder_df,one_stock_df])
        n += 1
    #print(stock_holder_df)
    stock_holder_df['totaldays'] = stock_holder_df['myenddate'].apply(lambda x: (datetime.datetime(x,12,31)-datetime.datetime(x,1,1)).days + 1)
    stock_holder_df.to_excel(os.path.join(MAIN_PATH, 'stock_holder_df.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'stock_holder_df.pkl'), 'wb')
    pickle.dump(stock_holder_df, F)
    F.close()

if STEP_STOCK_HOLDER_REORGANIZING:
    F = open(os.path.join(MAIN_PATH, 'stock_holder_df.pkl'), 'rb')
    raw_stock_holder_to_be_organized = pickle.load(F)
    grouped = raw_stock_holder_to_be_organized.groupby('上市公司代码_ComCd')

    num = 0
    for name, in_group in grouped:
        innn_num = 0
        myindex = dict()
        in_group.index = range(in_group.shape[0])
        for innd in in_group.index:
            if in_group.loc[innd,'myenddate'] in myindex:
                #in_group.loc[myindex[in_group.loc[innd, 'myenddate']], 'sharehold'] = 'hello'
                in_group.loc[myindex[in_group.loc[innd,'myenddate']], 'sharehold'] = (in_group.loc[innd,'股东持股比例_HoldPct'] * in_group.loc[innd,'mydays'] / in_group.loc[innd,'totaldays'] + in_group.loc[myindex[in_group.loc[innd,'myenddate']], 'sharehold'])/2
            else:
                in_group.loc[innd,'sharehold'] = in_group.loc[innd,'股东持股比例_HoldPct'] * in_group.loc[innd,'mydays'] / in_group.loc[innd,'totaldays']
                myindex.update({in_group.loc[innd,'myenddate']:innd})
            innn_num += 1
        in_group_df = in_group.loc[sorted(myindex.values())]
        if num == 0:
            stock_df = in_group_df
        else:
            stock_df = pd.concat([stock_df,in_group_df])
        num += 1

    #print(stock_df)
    stock_df.to_excel(os.path.join(MAIN_PATH, 'stock_df.xlsx'))
    #F = open(os.path.join(MAIN_PATH, 'stock_df.pkl'), 'wb')
    #pickle.dump(stock_df, F)
    #F.close()

if STEP_FOUR_TABLE_WITH_STOCK_HOLDER:
    F = open(os.path.join(MAIN_PATH, 'output_fourtable_with_code.pkl'), 'rb')
    raw_four_table_with_code = pickle.load(F)

    raw_stock_df = pd.read_excel(os.path.join(MAIN_PATH,'stock_df.xlsx'))
    print(raw_stock_df.columns)
    print(raw_four_table_with_code.columns)

    print(raw_four_table_with_code.shape, raw_stock_df.shape)
    raw_stock_df['stockbeheld'] = 1
    data_table = pd.merge(raw_four_table_with_code,raw_stock_df,how='left',on=['上市公司代码_ComCd','myenddate'])
    data_table['stockbeheld'] = data_table['stockbeheld'].fillna(0)
    print(data_table.shape)

    data_table.to_excel(os.path.join(MAIN_PATH, 'final_table.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'final_table.pkl'), 'wb')
    pickle.dump(data_table, F)
    F.close()

if STEP_STATE_OWNED_DATA:
    F = open(os.path.join(MAIN_PATH, 'raw_state_owned_data.pkl'), 'rb')
    raw_state_owned_data = pickle.load(F)
    raw_state_owned_data['myenddate'] = raw_state_owned_data['截止日期_EndDt'].apply(lambda x: x.year)
    raw_state_owned_data = raw_state_owned_data[['上市公司代码_ComCd','myenddate','股东名单_SHLst','持股数占总股本比例_PctTotShr']]

    result_df = None
    grouped = raw_state_owned_data.groupby('上市公司代码_ComCd')
    for compid, group in grouped:
        for year, inn_group in group.groupby('myenddate'):
            inn_group = inn_group.drop_duplicates('股东名单_SHLst','last')
            #print(inn_group.shape)
            inn_df = inn_group[['上市公司代码_ComCd', 'myenddate', '持股数占总股本比例_PctTotShr']]
            sum_of_share = inn_df['持股数占总股本比例_PctTotShr'].sum()
            inner_df = inn_df[0:1]
            inner_df['sumofshare'] = sum_of_share
            if result_df is None:
                result_df = inner_df
            else:
                result_df = result_df.append(inner_df)
    del result_df['持股数占总股本比例_PctTotShr']
    result_df['chs2'] = 1

    result_df.to_excel(os.path.join(MAIN_PATH, 'state_owned_data.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'state_owned_data.pkl'), 'wb')
    pickle.dump(result_df, F)
    F.close()

if STEP_CREATE_CHS2:
    F = open(os.path.join(MAIN_PATH, 'state_owned_data.pkl'), 'rb')
    state_owned_data = pickle.load(F)
    print(state_owned_data.columns)

    F = open(os.path.join(MAIN_PATH, 'final_table.pkl'), 'rb')
    final_table_1 = pickle.load(F)

    print(final_table_1.shape)
    final_table_2 = pd.merge(final_table_1, state_owned_data[['上市公司代码_ComCd', 'myenddate','chs2']], how='left', on=['上市公司代码_ComCd', 'myenddate'])
    final_table_2['chs2'] = final_table_2['chs2'].fillna(0)
    print(final_table_2.shape)
    print(final_table_2[final_table_2['chs2']==1].shape)
    print(final_table_2[['上市公司代码_ComCd', 'myenddate','chs2']])

    final_table_2.to_excel(os.path.join(MAIN_PATH, 'final_table_2.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'final_table_2.pkl'), 'wb')
    pickle.dump(final_table_2, F)
    F.close()

if STEP_STOCKER_HOLDER_MORE:
    raw_stock_holder = pd.read_excel(STOCK_HOLDER_PATH)
    print(raw_stock_holder.shape)
    raw_stock_holder = raw_stock_holder.dropna(subset=['股东上市公司代码_SHComCd'])
    raw_cross_stock_holder = raw_stock_holder
    print(raw_cross_stock_holder.shape)

    n = 0
    for ind in raw_cross_stock_holder.index:
        print(raw_cross_stock_holder.loc[ind, '关联起始日_RelStartDt'],raw_cross_stock_holder.loc[ind, '关联截止日_RelEndDt'])
        if isinstance(raw_cross_stock_holder.loc[ind, '关联起始日_RelStartDt'],pd.tslib.NaTType) and isinstance(raw_cross_stock_holder.loc[ind, '关联截止日_RelEndDt'],pd.tslib.NaTType):
            continue

        if isinstance(raw_cross_stock_holder.loc[ind, '关联起始日_RelStartDt'],pd.tslib.NaTType):
            start_date = datetime.datetime(2005,1,1)
            end_date = raw_cross_stock_holder.loc[ind, '关联截止日_RelEndDt']
        elif isinstance(raw_cross_stock_holder.loc[ind, '关联截止日_RelEndDt'],pd.tslib.NaTType):
            start_date = raw_cross_stock_holder.loc[ind, '关联起始日_RelStartDt']
            end_date = datetime.datetime(2016,12,31)
        else:
            start_date = raw_cross_stock_holder.loc[ind, '关联起始日_RelStartDt']
            end_date = raw_cross_stock_holder.loc[ind, '关联截止日_RelEndDt']

        if start_date <  datetime.datetime(2005,1,1):
            start_date = datetime.datetime(2005,1,1)
        if end_date >  datetime.datetime(2016,12,31):
            start_date = datetime.datetime(2016,12,31)

        print('-------------',start_date,' ---> ',end_date,'-------------')
        i = 0
        while end_date > start_date:
            if (end_date - start_date) >= pd.Timedelta('365 days'):
                days = datetime.datetime(start_date.year,12,31) - start_date + pd.Timedelta('1 days')
                print('ppppp',days.days)
                if days <= pd.Timedelta('1 days'):
                    days = datetime.datetime(start_date.year+1,12,31) - start_date
                    print('left',days)
                    sign_end_date = datetime.datetime(start_date.year+1, 12, 31)
                else:
                    sign_end_date = datetime.datetime(start_date.year,12,31)
                start_date = sign_end_date + pd.Timedelta('1 days')
                print('nnnn', end_date, start_date, sign_end_date, start_date)
                if i == 0:
                    one_stock_df = raw_cross_stock_holder.loc[ind].copy()
                    one_stock_df['myenddate'] = sign_end_date.year
                    one_stock_df['mydays'] = days.days
                    one_stock_df = one_stock_df.to_frame().transpose()
                else:
                    one_tmp_stock_df = raw_cross_stock_holder.loc[ind].copy()
                    one_tmp_stock_df['myenddate'] = sign_end_date.year
                    one_tmp_stock_df['mydays'] = days.days
                    one_tmp_stock_df = one_tmp_stock_df.to_frame().transpose()
                    one_stock_df = pd.concat([one_stock_df,one_tmp_stock_df])
            else:
                days = datetime.datetime(start_date.year, 12, 31) - start_date + pd.Timedelta('1 days')
                if days <= pd.Timedelta('1 days'):
                    days = end_date - start_date
                    sign_end_date = datetime.datetime(end_date.year, 12, 31)
                    start_date = end_date + pd.Timedelta('1 days')
                else:
                    if start_date.year < end_date.year:
                        days = datetime.datetime(start_date.year, 12, 31) - start_date + pd.Timedelta('1 days')
                        sign_end_date = datetime.datetime(start_date.year, 12, 31)
                        start_date = sign_end_date + pd.Timedelta('1 days')
                    else:
                        days = end_date - start_date + pd.Timedelta('1 days')
                        sign_end_date = datetime.datetime(end_date.year, 12, 31)
                        start_date = end_date + pd.Timedelta('1 days')
                print('ppp', start_date, end_date, days, type(days), days.days)
                #start_date = start_date + pd.Timedelta('365 days')
                if i == 0:
                    one_stock_df = raw_cross_stock_holder.loc[ind].copy()
                    one_stock_df['myenddate'] = sign_end_date.year
                    one_stock_df['mydays'] = days.days
                    one_stock_df = one_stock_df.to_frame().transpose()
                else:
                    one_tmp_stock_df = raw_cross_stock_holder.loc[ind].copy()
                    one_tmp_stock_df['myenddate'] = sign_end_date.year
                    one_tmp_stock_df['mydays'] = days.days
                    one_tmp_stock_df = one_tmp_stock_df.to_frame().transpose()
                    one_stock_df = pd.concat([one_stock_df, one_tmp_stock_df])
            i += 1
        if n == 0:
            stock_holder_df = one_stock_df
        else:
            stock_holder_df = pd.concat([stock_holder_df,one_stock_df])
        n += 1
    stock_holder_df['totaldays'] = stock_holder_df['myenddate'].apply(lambda x: (datetime.datetime(x,12,31)-datetime.datetime(x,1,1)).days + 1)
    stock_holder_df.to_excel(os.path.join(MAIN_PATH, 'stock_holder_more_df.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'stock_holder_more_df.pkl'), 'wb')
    pickle.dump(stock_holder_df, F)
    F.close()

if STEP_CREATE_CHS1:
    F = open(os.path.join(MAIN_PATH, 'state_owned_data.pkl'), 'rb')
    state_owned_data = pickle.load(F)
    state_owned_data.columns.values[0] = '股东上市公司代码_SHComCd'
    state_owned_data.columns.values[3] = 'chs1'
    print(state_owned_data.columns)

    F = open(os.path.join(MAIN_PATH, 'stock_holder_more_df.pkl'), 'rb')
    stock_holder_more_df = pickle.load(F)
    print(stock_holder_more_df.shape)

    stock_holder_state_owned_df = pd.merge(stock_holder_more_df, state_owned_data[['股东上市公司代码_SHComCd', 'myenddate', 'chs1']],
                                           how='left',on=['股东上市公司代码_SHComCd', 'myenddate'])
    stock_holder_state_owned_df = stock_holder_state_owned_df.dropna(subset=['chs1'])
    print(stock_holder_state_owned_df.shape)

    grouped = stock_holder_state_owned_df.groupby('上市公司代码_ComCd')

    num = 0
    for name, in_group in grouped:
        innn_num = 0
        myindex = dict()
        in_group.index = range(in_group.shape[0])
        for innd in in_group.index:
            if in_group.loc[innd, 'myenddate'] in myindex:
                # in_group.loc[myindex[in_group.loc[innd, 'myenddate']], 'sharehold'] = 'hello'
                in_group.loc[myindex[in_group.loc[innd, 'myenddate']], 'sharehold'] = (in_group.loc[
                                                                                           innd, '股东持股比例_HoldPct'] *
                                                                                       in_group.loc[innd, 'mydays'] /
                                                                                       in_group.loc[innd, 'totaldays'] +
                                                                                       in_group.loc[myindex[
                                                                                                        in_group.loc[
                                                                                                            innd, 'myenddate']], 'sharehold']) / 2
            else:
                in_group.loc[innd, 'sharehold'] = in_group.loc[innd, '股东持股比例_HoldPct'] * in_group.loc[innd, 'mydays'] / \
                                                  in_group.loc[innd, 'totaldays']
                myindex.update({in_group.loc[innd, 'myenddate']: innd})
            innn_num += 1
        in_group_df = in_group.loc[sorted(myindex.values())]
        if num == 0:
            stock_df = in_group_df
        else:
            stock_df = pd.concat([stock_df, in_group_df])
        num += 1

    print(stock_df.shape)
    stock_df.to_excel(os.path.join(MAIN_PATH, 'stock_state_owned_df.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'stock_state_owned_df.pkl'), 'wb')
    pickle.dump(stock_df, F)
    F.close()

if STEP_MERGE_FINAL_TABLE:
    F = open(os.path.join(MAIN_PATH, 'stock_state_owned_df.pkl'), 'rb')
    stock_state_owned_df = pickle.load(F)
    stock_state_owned_df = stock_state_owned_df[['上市公司代码_ComCd','myenddate','chs1','sharehold']]
    stock_state_owned_df.columns.values[3] = 'stateownsharehold'
    print(stock_state_owned_df.columns)

    F = open(os.path.join(MAIN_PATH, 'final_table_2.pkl'), 'rb')
    final_table_2 = pickle.load(F)
    final_table_3 = pd.merge(final_table_2, stock_state_owned_df, how='left', on=['上市公司代码_ComCd', 'myenddate'])
    final_table_3['chs1'] = final_table_3['chs1'].fillna(0)
    print(final_table_2.shape,final_table_3.shape)

    final_table_3.to_excel(os.path.join(MAIN_PATH, 'final_table_3.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'final_table_3.pkl'), 'wb')
    pickle.dump(final_table_3, F)
    F.close()