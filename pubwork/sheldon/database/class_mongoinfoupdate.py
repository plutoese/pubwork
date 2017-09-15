# coding=UTF-8

"""
=========================================
Redis数据库类
=========================================

:Author: glen
:Date: 2017.9.3
:Tags: redis database
:abstract: 连接redis数据库，并进行基本操作。

**类**
==================
Redis
    连接Redis数据库

**使用方法**
==================


**示范代码**
==================
::

"""

from sheldon.database.class_mongodb import MongoDB, MonCollection
from sheldon.database.class_redis import Redis


class AirQualityUpdater:
    def __init__(self, mongo=None, redis=None):
        if mongo is None:
            self._mongo = MonCollection(mongodb=MongoDB(),database='scraperdata', collection_name='airqualityfromMin')
        else:
            self._mongo = mongo

        if redis is None:
            self._redis = Redis()
        else:
            self._redis = redis

    def __call__(self):
        airquality_citycode = sorted(self._mongo.distinct('CITYCODE'))
        airquality_city = [self._mongo.collection.find_one({'CITYCODE': ccode}, projection={'_id': False, 'CITY': True})['CITY'] for ccode in airquality_citycode]
        airquality_date = ([date.strftime("%y-%m-%d") for date in sorted(self._mongo.distinct('OPER_DATE'))])

        # update
        self._redis.set('airquality_city', airquality_city)
        self._redis.set('airquality_citycode', airquality_citycode)
        self._redis.set('airquality_date', airquality_date)


class CEICInfoUpdater:
    def __init__(self, mongo=None, redis=None):
        if mongo is None:
            self._mongo = MonCollection(mongodb=MongoDB(),database='region', collection_name='CEIC')
        else:
            self._mongo = mongo

        if redis is None:
            self._redis = Redis()
        else:
            self._redis = redis

    def __call__(self):
        ceic_period = sorted(self._mongo.distinct('year'))
        ceic_variable = sorted(self._mongo.distinct('variable'))
        ceic_acode = sorted(self._mongo.distinct('acode'))
        ceic_region = [self._mongo.collection.find_one({'acode':acode},projection={'_id':False,'region':True})['region'] for acode in ceic_acode]

        #update
        self._redis.set('ceic_acode',ceic_acode)
        self._redis.set('ceic_period', ceic_period)
        self._redis.set('ceic_variable', ceic_variable)
        self._redis.set('ceic_region', ceic_region)


class MongoDBInfoUpdater:
    updates = {'ceic': CEICInfoUpdater, 'airquality':AirQualityUpdater}

    def __init__(self,to_be_update=['airquality']):
        self._to_be_update = list(to_be_update)

    def __call__(self, *args, **kwargs):
        for to_be_update in self._to_be_update:
            print('update: ', to_be_update)
            self.updates[to_be_update]()()

if __name__ == '__main__':
    mcollection = MonCollection(mongodb=MongoDB(),database='region', collection_name='CEIC')

    updater = MongoDBInfoUpdater()
    updater()