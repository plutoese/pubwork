# coding=UTF-8

"""
=========================================
静态网页爬虫
=========================================

:Author: glen
:Date: 2017.1.3
:Tags: scrape web
:abstract: 主要用于静态网页的抓取

**类**
==================
StaticSingleWebScraper
    静态单一页面爬虫

StaticWebScraper
    静态网页爬虫


**使用方法**
==================


**示范代码**
==================
::

    >>># 创建pandas.DataFrame格式数据
    >>>pd.DataFrame({'one' : pd.Series([1., 2., 3., 6.], index=['a', 'b', 'c', 'd']),'two' : pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])})
    >>># 创建VariableApplyFunc对象
    >>>var_func = VariableCreator(data=data, func=np.log, name='log', variable_names=['one'])
    >>># 调用回调函数
    >>>print(var_func())
"""

import requests
from bs4 import BeautifulSoup
from libs.class_htmlparser import HtmlParser
import warnings

warnings.filterwarnings("ignore")


class StaticSingleWebScraper:
    def __init__(self, web_site=None, usr=None, psword=None, encoding='utf-8'):
        self._web_address = web_site
        self._usr = usr
        self._psword = psword
        self._request = None
        self._bsobj = None
        self._html_parser = None
        self._encoding = encoding
        self._json = None
        self._content = None

    def scrape(self, verify=None, bs=True, json=False):

        if self._usr is None:
            if verify is None:
                self._request = requests.get(self._web_address)
            else:
                self._request = requests.get(self._web_address, verify=verify)
        else:
            if verify is None:
                self._request = requests.get(self._web_address, auth=(self._usr, self._psword))
            else:
                self._request = requests.get(self._web_address, auth=(self._usr, self._psword), verify=verify)

        self._request.encoding = self._encoding

        self._content = self._request.text

        if json:
            self._json = self._request.json()

        if bs:
            self._html_parser = HtmlParser(html_content=self._content)

    def is_title(self,title=None):
        return self._html_parser.title == title

    @property
    def request(self):
        return self._request

    @property
    def html_parser(self):
        return self._html_parser

    @property
    def encoding(self):
        return self._request.encoding

    @property
    def url(self):
        return self._request.url

    @property
    def json(self):
        return self._json

    @property
    def content(self):
        return self._content

if __name__ == '__main__':
    scraper = StaticSingleWebScraper(web_site='http://mobile.12306.cn/weixin/leftTicket/query?leftTicketDTO.train_date=2017-01-07&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT')

    scraper = StaticSingleWebScraper(web_site='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8994')
    scraper.scrape(verify=False)
    #print(scraper.html_parser.title, scraper.is_title('车票预订 | 客运服务 | 铁路客户服务中心'))
    #print(scraper.encoding)
    #print(scraper.url)
    #print(scraper.json)

    print(scraper.request.text)
    '''
    result = scraper.json['data']
    for key in result:
        print(key)
        #print('{}: {}-{},历时{}'.format(key['station_train_code'],
        #                         key['start_station_name'],
        #                         key['to_station_name'],
        #                              key['lishi']))'''
