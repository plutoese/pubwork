# coding = UTF-8

import os
import pandas as pd
import pickle

CREATE_STOCK_HOLDER_DATASET = False
CREATE_SHARE_HOLDER = False
CREATE_BE_HOLDER = False
CREATE_SHARE_HOLDER_HOLDER = False
CREATE_SHARE_BE_HOLDER_HOLDER = False
MERGE_FULL_TABLE = True

MAIN_PATH = 'F:/roombackup/dataset/yang'
# original final datatable
data_table = pd.read_pickle(os.path.join(MAIN_PATH, 'stage_sorted_full_table.pkl'))
# stock holder datatable
stock_holder_data = pd.read_pickle(os.path.join(MAIN_PATH, 'process_organized_stock_holder.pkl'))
# industry code datatable
industry_code_data = pd.read_pickle(os.path.join(MAIN_PATH, 'industry_code.pkl'))

if CREATE_STOCK_HOLDER_DATASET:

    process_stock_holder_data = stock_holder_data.loc[:,
                                ['上市公司代码_ComCd', '股东上市公司代码_SHComCd', 'myenddate', 'mydays', 'totaldays']]

    process_stock_holder_data['comcd_code'] = process_stock_holder_data['上市公司代码_ComCd'].apply(
        lambda x: industry_code_data.get(x))
    process_stock_holder_data['shcomcd_code'] = process_stock_holder_data['股东上市公司代码_SHComCd'].apply(
        lambda x: industry_code_data.get(x))

    process_stock_holder_data.to_excel(os.path.join(MAIN_PATH, 'progress_share_holder_dataset.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'progress_share_holder_dataset.pkl'), 'wb')
    pickle.dump(process_stock_holder_data, F)
    F.close()

if CREATE_SHARE_HOLDER:

    # merge table
    process_stock_holder_data = stock_holder_data.loc[:,['上市公司代码_ComCd','股东上市公司代码_SHComCd','myenddate','mydays','totaldays']]

    process_stock_holder_data['comcd_code'] = process_stock_holder_data['上市公司代码_ComCd'].apply(lambda x: industry_code_data.get(x))
    process_stock_holder_data['shcomcd_code'] = process_stock_holder_data['股东上市公司代码_SHComCd'].apply(lambda x: industry_code_data.get(x))

    # 2. Process
    grouped = process_stock_holder_data.groupby(['股东上市公司代码_SHComCd','myenddate'])

    i = 0
    for name, in_group in grouped:
        inner_df = in_group.iloc[0:1,[1,2]]
        print(i,'->',in_group['shcomcd_code'].iloc[0],'-:',set(in_group['comcd_code']),'-$',in_group['shcomcd_code'].iloc[0] in set(in_group['comcd_code']))

        if in_group['shcomcd_code'].iloc[0] in set(in_group['comcd_code']):
            inner_df['shareholding'] = 1
        else:
            inner_df['shareholding'] = 0

        if i == 0:
            new_df = inner_df
        else:
            new_df = pd.concat([new_df, inner_df])
        i += 1

    new_df = new_df.rename_axis({'股东上市公司代码_SHComCd':'上市公司代码_ComCd'},axis='columns')

    new_df.to_excel(os.path.join(MAIN_PATH, 'progress_share_holder.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'progress_share_holder.pkl'), 'wb')
    pickle.dump(new_df, F)
    F.close()

if CREATE_BE_HOLDER:

    process_stock_holder_data = pd.read_pickle(os.path.join(MAIN_PATH, 'progress_share_holder_dataset.pkl'))

    # 2. Process
    grouped = process_stock_holder_data.groupby(['上市公司代码_ComCd', 'myenddate'])

    i = 0
    for name, in_group in grouped:
        inner_df = in_group.iloc[0:1, [0, 2]]
        print(i, '->', in_group['comcd_code'].iloc[0], '-:', set(in_group['shcomcd_code']), '-$',
              in_group['comcd_code'].iloc[0] in set(in_group['shcomcd_code']))

        if in_group['comcd_code'].iloc[0] in set(in_group['shcomcd_code']):
            inner_df['sharebeholding'] = 1
        else:
            inner_df['sharebeholding'] = 0

        if i == 0:
            new_df = inner_df
        else:
            new_df = pd.concat([new_df, inner_df])
        i += 1

    new_df.to_excel(os.path.join(MAIN_PATH, 'progress_share_be_hold.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'progress_share_be_hold.pkl'), 'wb')
    pickle.dump(new_df, F)
    F.close()

if CREATE_SHARE_HOLDER_HOLDER:
    process_stock_holder_data = pd.read_pickle(os.path.join(MAIN_PATH, 'progress_share_holder_dataset.pkl'))

    grouped = process_stock_holder_data.groupby(['股东上市公司代码_SHComCd', 'myenddate'])
    inn_grouped = process_stock_holder_data.groupby(['股东上市公司代码_SHComCd', 'myenddate'])

    i = 0
    for name, in_group in grouped:
        inner_df = in_group.iloc[0:1, [1, 2]]
        inner_df['shareholdholder'] = 0
        print(i, ': ', name, '->', in_group['shcomcd_code'].iloc[0], '-:', set(in_group['comcd_code']), '-$',
              in_group['shcomcd_code'].iloc[0] in set(in_group['comcd_code']))

        in_group.index = range(0,in_group.shape[0])

        for ind in in_group.index:
            if inner_df['shareholdholder'].any() == 1:
                break
            if in_group.loc[ind,'shcomcd_code'] == in_group.loc[ind,'comcd_code']:
                holder = in_group.loc[ind,'上市公司代码_ComCd']
                holder_tuple = (holder,name[1])
                for inn_name, inn_group in inn_grouped:
                    if holder_tuple == inn_name:
                        #print(holder_tuple,inn_group)
                        if inn_group['shcomcd_code'].iloc[0] in set(inn_group['comcd_code']):
                            inner_df['shareholdholder'] = 1
                        break

        if i == 0:
            new_df = inner_df
        else:
            new_df = pd.concat([new_df, inner_df])
        i += 1

    new_df = new_df.rename_axis({'股东上市公司代码_SHComCd': '上市公司代码_ComCd'}, axis='columns')

    new_df.to_excel(os.path.join(MAIN_PATH, 'progress_share_hold_holder.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'progress_share_hold_holder.pkl'), 'wb')
    pickle.dump(new_df, F)
    F.close()

if CREATE_SHARE_BE_HOLDER_HOLDER:
    process_stock_holder_data = pd.read_pickle(os.path.join(MAIN_PATH, 'progress_share_holder_dataset.pkl'))

    grouped = process_stock_holder_data.groupby(['上市公司代码_ComCd', 'myenddate'])
    inn_grouped = process_stock_holder_data.groupby(['上市公司代码_ComCd', 'myenddate'])

    i = 0
    for name, in_group in grouped:
        inner_df = in_group.iloc[0:1, [0, 2]]
        inner_df['sharebeholdholder'] = 0
        print(i, ': ', name, '->', in_group['comcd_code'].iloc[0], '-:', set(in_group['shcomcd_code']), '-$',
              in_group['comcd_code'].iloc[0] in set(in_group['shcomcd_code']))

        in_group.index = range(0,in_group.shape[0])

        for ind in in_group.index:
            if inner_df['sharebeholdholder'].any() == 1:
                break
            if in_group.loc[ind,'comcd_code'] == in_group.loc[ind,'shcomcd_code']:
                holder = in_group.loc[ind,'股东上市公司代码_SHComCd']
                holder_tuple = (holder,name[1])
                for inn_name, inn_group in inn_grouped:
                    if holder_tuple == inn_name:
                        #print(holder_tuple,inn_group)
                        if inn_group['comcd_code'].iloc[0] in set(inn_group['shcomcd_code']):
                            inner_df['sharebeholdholder'] = 1
                        break

        if i == 0:
            new_df = inner_df
        else:
            new_df = pd.concat([new_df, inner_df])
        i += 1

    new_df.to_excel(os.path.join(MAIN_PATH, 'progress_share_be_hold_holder.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'progress_share_be_hold_holder.pkl'), 'wb')
    pickle.dump(new_df, F)
    F.close()

if MERGE_FULL_TABLE:
    holder = pd.read_pickle(os.path.join(MAIN_PATH, 'progress_share_holder.pkl'))
    hold_holder = pd.read_pickle(os.path.join(MAIN_PATH, 'progress_share_hold_holder.pkl'))

    be_hold = pd.read_pickle(os.path.join(MAIN_PATH, 'progress_share_be_hold.pkl'))
    be_holder_hold = pd.read_pickle(os.path.join(MAIN_PATH, 'progress_share_be_hold_holder.pkl'))

    final_table_a = pd.merge(data_table, holder,how='outer',on=['上市公司代码_ComCd', 'myenddate'])
    final_table_b = pd.merge(final_table_a, hold_holder, how='outer', on=['上市公司代码_ComCd', 'myenddate'])
    final_table_c = pd.merge(final_table_b, be_hold, how='outer', on=['上市公司代码_ComCd', 'myenddate'])
    final_table_d = pd.merge(final_table_c, be_holder_hold, how='outer', on=['上市公司代码_ComCd', 'myenddate'])

    final_table_d = final_table_d.sort_values(by=['上市公司代码_ComCd', 'myenddate'])

    final_table_d['shareholding'] = final_table_d['shareholding'].fillna(0)
    final_table_d['shareholdholder'] = final_table_d['shareholdholder'].fillna(0)
    final_table_d['sharebeholding'] = final_table_d['sharebeholding'].fillna(0)
    final_table_d['sharebeholdholder'] = final_table_d['sharebeholdholder'].fillna(0)

    final_table_d.to_excel(os.path.join(MAIN_PATH, 'stage_two_full_table.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'stage_two_full_table.pkl'), 'wb')
    pickle.dump(final_table_d, F)
    F.close()


'''

new_df = pd.read_pickle(os.path.join(MAIN_PATH,'new_df_01.pkl'))
new_df = new_df.rename_axis({'股东上市公司代码_SHComCd':'上市公司代码_ComCd'},axis='columns')
final_table_a = pd.merge(data_table, new_df, how='outer', on=['上市公司代码_ComCd', 'myenddate'])
final_table_a['shareholding'] = final_table_a['shareholding'].fillna(0)

print(len(data_table),len(final_table_a))
final_table_a.to_excel(os.path.join(MAIN_PATH, 'final_table_b.xlsx'))
#F = open(os.path.join(MAIN_PATH, 'final_table_a.pkl'), 'wb')
#pickle.dump(final_table_a, F)
#F.close()'''