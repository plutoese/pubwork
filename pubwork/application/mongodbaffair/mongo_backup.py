# coding = UTF-8

from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection

LOCAL_TO_REMOTE = False
REMOTE_TO_LOCAL = True

backup_databases = ['region','microdata','papers','proxy','scraperdata','statsgov']

remote_mongo = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')
local_mongo = MongoDB(conn_str=None)


def backup(source,target):
    for database in backup_databases:
        if database not in source.database_names:
            print('No Database named {} remotely!'.format(database))
            raise Exception

        if database not in target.database_names:
            print('No Database name {} locally!'.format(database))
            raise Exception

        source_database = MonDatabase(source, database_name=database)
        target_database = MonDatabase(target, database_name=database)

        for collection in source_database.collection_names:
            if collection not in target_database.collection_names:
                target_database.create_collection(collection)

            source_collection = MonCollection(source,source_database,collection)
            target_collection = MonCollection(target,target_database,collection)

            for record in source_collection.find():
                target_collection.collection.insert_one(record)



if LOCAL_TO_REMOTE:
    backup(source=local_mongo, target=remote_mongo)

if REMOTE_TO_LOCAL:
    backup(source=remote_mongo, target=local_mongo)

