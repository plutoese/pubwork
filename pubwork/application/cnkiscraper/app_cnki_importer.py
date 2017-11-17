# coding = UTF-8

import os
import numpy as np
import pandas as pd
import re
from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection

# 0. Initialize
PATH = r'D:\data\cnki\forimport'

# 1. connect to db
mongo = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')
mdb = MonDatabase(mongodb=mongo, database_name='papers')
con = MonCollection(mongo,mdb,collection_name='cnki').collection

for file in os.listdir(PATH):
    file_name = os.path.join(PATH,file)
    mdata = pd.read_excel(file_name)
    records = mdata.to_dict(orient='index')
    for num in records:
        db_record = dict()
        # 标题
        db_record['title'] = records[num]['Title']
        # 作者
        if isinstance(records[num]['Author'],str):
            db_record['author'] = [author for author in  re.split(';',records[num]['Author']) if re.match('^\s*$',author) is None]
        else:
            continue
        # 地址
        if isinstance(records[num]['Author Address'],str):
            db_record['address'] = [author for author in  re.split(';',records[num]['Author Address']) if re.match('^\s*$',author) is None]
        # 期刊名称
        if records[num]['Journal'] == re.split('\.',file)[0]:
            db_record['journal'] = records[num]['Journal']
        else:
            continue
        # 年份
        db_record['year'] = str(records[num]['Year'])
        db_record['issue'] = str(records[num]['Issue'])
        db_record['pages'] = str(records[num]['Pages'])
        # 关键词
        if isinstance(records[num]['Keywords'],str):
            db_record['keyword'] = [keyword for keyword in  re.split(';',records[num]['Keywords']) if re.match('^\s*$',keyword) is None]
        else:
            continue
        # 摘要
        db_record['abstract'] = records[num]['Abstract']
        db_record['ISBN/ISSN'] = records[num]['ISBN/ISSN']

        found = con.find_one(db_record)
        if found is None:
            print('OK')
            print(db_record)
            con.insert_one(db_record)




