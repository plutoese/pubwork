# coding = UTF-8

"""
@title: 数据库备份
@introduction: 备份数据库
@author: glen
@date: 2017.12.23
@tag: mongodb backup
"""

from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection

LOCAL_TO_REMOTE = True
REMOTE_TO_LOCAL = False

backup_databases = ['region','microdata','papers','proxy','scraperdata','statsgov','webdata']

local_mongo = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')
remote_mongo = MongoDB(conn_str='mongodb://root:z1Yh2900@dds-bp162bb74b8184e41658-pub.mongodb.rds.aliyuncs.com:3717,dds-bp162bb74b8184e42438-pub.mongodb.rds.aliyuncs.com:3717/admin?replicaSet=mgset-4970435')


def backup(source,target):
    for database in backup_databases:
        if database not in source.database_names:
            print('No Database named {} remotely!'.format(database))
            raise Exception

        if database not in target.database_names:
            print(source.database_names)
            print('No Database name {} locally!'.format(database))
            raise Exception

        source_database = MonDatabase(source, database_name=database)
        target_database = MonDatabase(target, database_name=database)

        for collection in source_database.collection_names:
            if collection not in target_database.collection_names:
                target_database.create_collection(collection)
            else:
                source_collection = MonCollection(source, source_database, collection)
                target_collection = MonCollection(target, target_database, collection)
                if source_collection.collection.count() <= target_collection.collection.count():
                    print('No need to update the collection: {}'.format(collection))
                    continue
                else:
                    print('updating...{}'.format(collection))
                    target_collection.collection.insert_many(source_collection.collection.find())


if LOCAL_TO_REMOTE:
    backup(source=local_mongo, target=remote_mongo)

if REMOTE_TO_LOCAL:
    backup(source=remote_mongo, target=local_mongo)

