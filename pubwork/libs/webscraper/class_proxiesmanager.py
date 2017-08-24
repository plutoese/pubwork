# coding=UTF-8

"""
=========================================
管理代理服务器
=========================================

:Author: glen
:Date: 2017.6.25
:Tags: proxy
:abstract: 管理代理服务器，包括储存、更新和验证代理服务器

**类**
==================
Proxy
    代理服务器类

ProxyManager
    代理服务器管理类

**使用方法**
==================

"""

import re
import pymongo
import random
from bs4 import BeautifulSoup
import requests
from libs.webscraper.class_proxyscraper import ProxyScraperFromXiciDaili
from libs.multithread.class_multithread import MultiThread
from libs.database.class_mongodb import MongoDB, MonDatabase, MonCollection


class ProxyManager:
    """管理代理服务器

    """
    def __init__(self):
        # 设置数据库
        mongo = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')
        mdb = MonDatabase(mongodb=mongo, database_name='proxy')
        self._collection = MonCollection(database=mdb, collection_name='proxys')

    @property
    def all_valid_proxies(self):
        all_valid_proxies = self._collection.collection.find(
            filter = {'score': {'$gt': 9}},
            projection={'_id':0, 'ip':1, 'port':1, 'protocol':1, 'speed':1},
            sort = [('speed', pymongo.ASCENDING)]
        )
        return list(all_valid_proxies)

    @property
    def top_50_proxies(self):
        proxies = self.all_valid_proxies[0:min(len(self.all_valid_proxies), 50)]
        return [''.join([r'http://',proxy['ip'],r':',str(proxy['port'])]) for proxy in proxies]

    @property
    def random_proxy(self):
        return random.choice(self.all_valid_proxies[0:min(len(self.all_valid_proxies),50)])

    @property
    def random_http_proxy(self):
        while True:
            http_proxy = self.random_proxy
            if http_proxy['protocol'] != 1:
                return ''.join([r'http://',http_proxy['ip'],r':',str(http_proxy['port'])])

    @property
    def random_https_proxy(self):
        while True:
            https_proxy = self.random_proxy
            if https_proxy['protocol'] != 0:
                return ''.join([r'http://', https_proxy['ip'], r':', str(https_proxy['port'])])

if __name__ == '__main__':
    proxy_manager = ProxyManager()

    print(proxy_manager.all_valid_proxies[0:10])
    print(proxy_manager.random_proxy)
    print(proxy_manager.random_https_proxy)
    print(proxy_manager.top_50_proxies)