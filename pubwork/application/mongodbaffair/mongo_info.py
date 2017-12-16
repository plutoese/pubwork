# coding = UTF-8

import pandas as pd
from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection

# 0. Initialization
OUTPUT_PATH = r'D:\data\output\mongodb_info.xlsx'

# 1. 连接数据库
mongo = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')

# 2. 数据库信息列表
database_info = []
for database_name in sorted(mongo.database_names):
    database_con = MonDatabase(mongo,database_name=database_name)
    if len(database_con.collection_names) > 0:
        for collection_name in sorted(database_con.collection_names):
            conn = MonCollection(mongo,database=database_name,collection_name=collection_name)
            database_info.append([database_name, collection_name, conn.collection.count()])
    else:
        database_info.append([database_name,None,None])

database_info_pdrame = pd.DataFrame(database_info,columns=['database','collection','count'])
#database_info_pdrame.to_excel(OUTPUT_PATH)







