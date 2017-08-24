# coding=UTF-8

"""
=========================================
代理服务器获取类
=========================================

:Author: glen
:Date: 2017.5.8
:Tags: proxy
:abstract: 获取代理服务器

**类**
==================
ProxyListFromXiciDaili
    从XiciDaili.com获取代理服务器

**使用方法**
==================

"""

from bs4 import BeautifulSoup
import re
import requests
from libs.database.class_mongodb import MongoDB, MonDatabase, MonCollection


class ProxyScraper:
    def __init__(self):
        self._proxies = []

    @property
    def proxies(self):
        return self._proxies


class ProxyScraperFromXiciDaili(ProxyScraper):
    def __init__(self):
        ProxyScraper.__init__(self)
        self.to_scrape()

    def to_scrape(self):
        r = requests.get('http://api.xicidaili.com/free2016.txt')
        self._proxies = [re.sub('\s+','',item) for item in re.split('\n',r.text)]

    @property
    def proxies(self):
        return self._proxies


if __name__ == '__main__':
    proxy_list = ProxyScraperFromXiciDaili()
    print(proxy_list.proxies)