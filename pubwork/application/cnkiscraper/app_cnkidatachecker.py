# coding = UTF-8

from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection

# 1. 连接数据库
mongo = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')
mdb = MonDatabase(mongodb=mongo, database_name='papers')
con = MonCollection(mongo,mdb,collection_name='cnki').collection

journals = con.find().distinct('journal')

i = 1
for journal in journals:
    period = con.find({'journal':journal}).distinct('year')
    if len(period) < 8:
        print(journal)
        #raise Exception
    print(journal,'->',sorted(period))
    #print(i)
    i += 1

