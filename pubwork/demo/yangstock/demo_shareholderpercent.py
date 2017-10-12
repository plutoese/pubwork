# coding = UTF-8

import os
import pandas as pd
import pickle

CREATE_STOCK_HOLDER_DATASET_WITH_PERCENT = False
CREATE_BE_HOLDER_PERCENT = False
MERGE_FULL_TABLE = True

MAIN_PATH = 'F:/roombackup/dataset/yang'
# original final datatable
data_table = pd.read_pickle(os.path.join(MAIN_PATH, 'stage_two_full_table.pkl'))
# stock holder datatable
stock_holder_data = pd.read_pickle(os.path.join(MAIN_PATH, 'process_organized_stock_holder.pkl'))
# industry code datatable
industry_code_data = pd.read_pickle(os.path.join(MAIN_PATH, 'industry_code.pkl'))

if CREATE_STOCK_HOLDER_DATASET_WITH_PERCENT:

    process_stock_holder_data = stock_holder_data.loc[:,
                                ['上市公司代码_ComCd', '股东上市公司代码_SHComCd', '股东持股比例_HoldPct', 'myenddate', 'mydays', 'totaldays']]

    process_stock_holder_data['comcd_code'] = process_stock_holder_data['上市公司代码_ComCd'].apply(
        lambda x: industry_code_data.get(x))
    process_stock_holder_data['shcomcd_code'] = process_stock_holder_data['股东上市公司代码_SHComCd'].apply(
        lambda x: industry_code_data.get(x))

    process_stock_holder_data.to_excel(os.path.join(MAIN_PATH, 'in_progress_share_holder_dataset.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'in_progress_share_holder_dataset.pkl'), 'wb')
    pickle.dump(process_stock_holder_data, F)
    F.close()

if CREATE_BE_HOLDER_PERCENT:

    process_stock_holder_data = pd.read_pickle(os.path.join(MAIN_PATH, 'in_progress_share_holder_dataset.pkl'))

    # 2. Process
    grouped = process_stock_holder_data.groupby(['上市公司代码_ComCd', 'myenddate'])

    i = 0
    for name, in_group in grouped:
        inner_df = in_group.iloc[0:1, [0, 3]]
        print(i, '->', in_group['comcd_code'].iloc[0], '-:', set(in_group['shcomcd_code']), '-$',
              in_group['comcd_code'].iloc[0] in set(in_group['shcomcd_code']))

        in_group.index = range(0,in_group.shape[0])

        percent = 0
        for ind in in_group.index:
            if in_group.loc[ind,'comcd_code'] == in_group.loc[ind,'shcomcd_code']:
                percent += in_group.loc[ind,'股东持股比例_HoldPct'] * min(in_group.loc[ind,'mydays']/in_group.loc[ind,'totaldays'],1)

        inner_df['beholderpercent'] = percent

        if i == 0:
            new_df = inner_df
        else:
            new_df = pd.concat([new_df, inner_df])
        i += 1

    new_df.to_excel(os.path.join(MAIN_PATH, 'in_progress_share_be_hold_percent.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'in_progress_share_be_hold_percent.pkl'), 'wb')
    pickle.dump(new_df, F)
    F.close()

if MERGE_FULL_TABLE:
    be_hold_percent = pd.read_pickle(os.path.join(MAIN_PATH, 'in_progress_share_be_hold_percent.pkl'))

    final_table_a = pd.merge(data_table, be_hold_percent,how='outer',on=['上市公司代码_ComCd', 'myenddate'])

    final_table_a = final_table_a.sort_values(by=['上市公司代码_ComCd', 'myenddate'])

    final_table_a['beholderpercent'] = final_table_a['beholderpercent'].fillna(0)

    final_table_a.to_excel(os.path.join(MAIN_PATH, 'stage_three_full_table.xlsx'))
    F = open(os.path.join(MAIN_PATH, 'stage_three_full_table.pkl'), 'wb')
    pickle.dump(final_table_a, F)
    F.close()
