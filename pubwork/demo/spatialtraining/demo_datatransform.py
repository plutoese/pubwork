# coding = UTF-8

import pandas as pd
from libs.database.class_mongodb import MongoDB, MonDatabase, MonCollection

# 数据库
mongo = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')
mdb = MonDatabase(mongodb=mongo, database_name='region')
mcollection = MonCollection(database=mdb, collection_name='admindivision')


def find_code(region):
    found = list(mcollection.collection.find({'year':'2010','region':region},projection={'_id': False, 'acode':True}))
    if len(found) > 1:
        print(found)
        raise Exception
    elif len(found) == 1:
        return found[0]['acode']
    else:
        return None

# 载入
rdata = pd.read_excel(r'D:\data\spatial\industry\ding.xlsx')
rdata['acode'] = rdata['城市'].apply(find_code)
rdata.to_excel(r'D:\data\spatial\industry\ding_code.xls')