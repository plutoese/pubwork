# coding = UTF-8

from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection
from pymongo import MongoClient, DESCENDING, ASCENDING
import re
from datetime import datetime, date

mongodb = MongoDB()
database_name = 'scraperdata'
collection_name = 'airqualityfromMin'
moncollection = MonCollection(mongodb=mongodb, database=database_name, collection_name=collection_name).collection

found_all = moncollection.find()

for item in found_all:
    if isinstance(item['OPER_DATE'],str):
        id = item['_id']
        print(item['OPER_DATE'])
        #oper_date = datetime(*[int(i) for i in re.split('-',item['OPER_DATE'])])
        #moncollection.update_one({'_id':id},{'$set':{'OPER_DATE':oper_date}})

