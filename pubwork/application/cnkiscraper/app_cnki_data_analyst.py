# coding = UTF-8

from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection

mongodb = MongoDB()
database_name = 'papers'
collection_name = 'cnki'
conn = MonCollection(mongodb=mongodb, database=database_name, collection_name=collection_name).collection

# 作者信息：{姓名：{年份：address}}
unmatched_records = []
matched_authors = dict()
for record in conn.find():
    if (record.get('author') is not None) and (record.get('address') is not None):
        if len(record.get('author')) == len(record.get('address')):
            for author in record.get('author'):
                if author in matched_authors.keys():
                    pass
                else:
                    matched_authors.update({author:set(record.get('year'),record.get('address'))})
        else:
            pass








