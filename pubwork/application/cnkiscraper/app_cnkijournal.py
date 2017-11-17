# coding = UTF-8

import pandas as pd
from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection

# 1. 连接数据库
mongodb='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/'
database='papers'
collection_name='csscijournals'
conn = MonCollection(mongodb=mongodb, database=database, collection_name=collection_name)

# 2. 导入杂志文件
journals = pd.read_excel('d:/data/cnki/economic_journals.xlsx')
for item in journals.to_dict(orient='record'):
    print(item)
    conn.collection.insert_one(item)