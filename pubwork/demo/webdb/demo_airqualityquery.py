# coding = UTF-8

from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection
from pymongo import MongoClient, DESCENDING, ASCENDING
import pandas as pd
from datetime import datetime, date

mongodb = MongoDB()
database_name = 'scraperdata'
collection_name = 'airqualityfromMin'
moncollection = MonCollection(mongodb=mongodb, database=database_name, collection_name=collection_name).collection


def query(start_date, end_date):
    print(type(start_date),end_date)
    found = list(moncollection.find({'$and':[{'OPER_DATE':{'$gte':start_date}},{'OPER_DATE':{'$lte':end_date}}]},projection={'_id': False, 'CITYCODE': True, 'OPER_DATE': True, 'AQI': True, 'CITY': True, 'STATUS': True},sort=[('OPER_DATE', ASCENDING), ('CITYCODE', ASCENDING)]))
    #found = []
    if len(found) > 0:
        return pd.DataFrame(list(found),columns=['OPER_DATE','CITYCODE','CITY','AQI','STATUS'])
    else:
        return None


start_date = datetime.strptime(str(date(2017,8,1)),'%Y-%m-%d')
end_date = datetime.strptime(str(date(2017,8,3)),'%Y-%m-%d')
#print(query(start_date,end_date))




