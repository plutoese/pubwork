# coding=UTF-8

"""
=========================================
管理代理服务器
=========================================

:Author: glen
:Date: 2017.5.8
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
import random
from bs4 import BeautifulSoup
import requests
from libs.webscraper.class_proxyscraper import ProxyScraperFromXiciDaili
from libs.multithread.class_multithread import MultiThread
from libs.database.class_mongodb import MongoDB, MonDatabase, MonCollection


class Proxy:
    """ Proxy类用来处理代理服务器

    :param str full_address: proxy的地址，形式如http://user:password@host:port/
    :param str type: 代理服务类型
    :return: 无返回值
    """
    def __init__(self, full_address, type='http'):
        self.__full_address = full_address
        self.__type = type

        self.__username = None
        self.__password = None
        if '@' in self.__full_address:
            username_and_password, address_and_port = re.split('@',re.split('//',self.__full_address)[1])
            self.__username, self.__password = re.split(':',username_and_password)
        else:
            address_and_port = re.split('//',self.__full_address)[1]

        address_and_port_list = re.split(':',address_and_port)
        self.__address = address_and_port_list[0]
        if len(address_and_port_list) > 1:
            self.__port = int(address_and_port_list[1])
        else:
            self.__address = 80

    def is_valid(self, check_address=None):
        """ 验证proxy是否有效

        :param str,dict check_address: 验证网址
        :return: 返回验证结果
        :rtype: bool
        """
        if check_address is None:
            check_address = {'address': 'http://epub.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ',
                             'title': '学术期刊—中国知网'}
        try:
            proxies = {'http':self.__full_address}
            to_check_title = False
            if isinstance(check_address,dict):
                to_check_address = check_address['address']
                to_check_title = True
            elif isinstance(check_address,str):
                to_check_address = check_address
            else:
                print('Wrong address Type: ',type(check_address))
                return False

            html = requests.get(url=to_check_address,proxies=proxies,timeout=10)
            if html.status_code != requests.codes.ok:
                print(html.status_code.code)
                return False
            bs = BeautifulSoup(html.content,'lxml')
            # check title
            if to_check_title:
                title = re.split('<',re.split('>',re.sub('\s+','',str(bs.title)))[1])[0]
                if not (title==check_address['title']):
                    print('Wrong title: ',title)
                    return False
            else:
                print(bs.title)
        except Exception:
            return False
        return True

    @property
    def full_address(self):
        """ 返回proxy地址

        :return: 返回proxy地址
        :rtype: str
        """
        return self.__full_address

    @property
    def address(self):
        return self.__address

    @property
    def port(self):
        return self.__port

    @property
    def username(self):
        return self.__username

    @property
    def password(self):
        return self.__password


class ProxyManager:
    """管理代理服务器

    """
    def __init__(self):
        # 设置数据库
        mongo = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')
        mdb = MonDatabase(mongodb=mongo, database_name='proxy')
        self._collection = MonCollection(database=mdb, collection_name='proxy')

        # 验证的网址
        self._checked_websites = [{'address':'http://www.163.com', 'title':'网易'},
                                  {'address':'http://www.sina.com.cn', 'title':'新浪首页'},
                                  {'address':'https://www.douban.com/', 'title':'豆瓣'},
                                  {'address':'http://www.sohu.com/', 'title':'搜狐'},
                                  {'address':'http://www.eastday.com/', 'title':'东方网'},
                                  {'address':'http://www.shanghaiairport.com/', 'title':'上海机场(集团)有限公司'}]

        # 设置检验完的代理服务器列表
        self._checked_proxy_list = dict()

    def scrape_proxies_list(self, store_to_db=True):
        """ 抓取代理服务器

        :param store_to_db: 是否储存进入数据库
        :return: 抓取的代理服务器列表
        :rtype: list
        """
        proxy_list = ProxyScraperFromXiciDaili().proxies
        if store_to_db:
            for proxy in proxy_list:
                found = self._collection.collection.find_one({'proxy':proxy})
                if found is None:
                    self._collection.collection.insert_one({'proxy':proxy})
        return proxy_list

    def update_proxies_in_db(self, min_success=60):
        """ 验证和储存有效的代理服务器地址

        """
        self.multi_thread_check_proxy()

        for key in self._checked_proxy_list:
            self._collection.collection.find_one_and_update({'proxy': key},
                                                            {'$set': {'success': self._checked_proxy_list[key]}})
        self._collection.collection.delete_many({'success': {'$lt': min_success}})

    def multi_thread_check_proxy(self, proxy_list=None):
        """ 多线程验证代理服务器的有效性，调用辅助函数self._check_and_put_proxy

        :return: 无返回值
        """
        threads = []
        if proxy_list is None:
            proxy_list = [item['proxy'] for item in self._collection.collection.find(projection={'_id':0,'proxy':1})]
        for ip in proxy_list:
            t = MultiThread(self.check_one_validity, args=(ip,), name=ip)
            threads.append(t)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    def check_one_validity(self, proxy_address):
        """ 辅助函数，用来检验代理服务器的有效性

        :param str proxy_address: 代理服务器地址，形如13.24.22.34:8080
        :return: 无返回值
        """
        count = 0
        total = len(self._checked_websites)
        for web in self._checked_websites:
            if Proxy(''.join(['http://', proxy_address])).is_valid(check_address=web):
                count += 1
                print('successful: ', proxy_address)
        self._checked_proxy_list.update({proxy_address: int(100*count/total)})

    @property
    def valid_proxies(self):
        all_valid_proxies = self._collection.collection.find(projection={'_id':0,'proxy':1,'success':1})
        return [item['proxy'] for item in sorted(list(all_valid_proxies),key=lambda x:x['success'],reverse=True)]

    @property
    def random_proxy(self):
        return random.choice(self.valid_proxies)

if __name__ == '__main__':
    '''
    #proxy = Proxy(full_address='http://58.247.88.54:80')
    addresses = ['115.213.202.51:808', '168.128.29.75:80', '203.93.0.115:80']
    for address in addresses:
        proxy = Proxy(full_address='http://{}'.format(address))
        print(proxy.full_address,proxy.address,proxy.port,proxy.username,proxy.password)
        if proxy.is_valid(check_address={'address':'http://epub.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ','title':'学术期刊—中国知网'}):
            print('successful: ',proxy.full_address)
        else:
            print('It is a bad proxy!')'''

    proxy_manager = ProxyManager()
    #proxy_manager.scrape_proxies_list()
    #proxy_manager.check_one_validity('168.128.29.75:80')
    #proxy_manager.update_proxies_in_db()
    print(proxy_manager.valid_proxies)