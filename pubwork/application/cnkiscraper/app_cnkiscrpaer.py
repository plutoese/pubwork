# coding = UTF-8

# --------------------------------------
# @title: cnki文献抓取主程序
# @author: glen
# @date: 2017.06.26
# --------------------------------------


import time
from libs.multithread.class_multithread import MultiThread
from libs.webscraper.class_proxiesmanager import ProxyManager
from application.cnkiscraper.class_cnkiscraper import CnkiScraperInterface


# 0. 函数
def scraper(journal, year, proxy_manager=None):
    if proxy_manager is not None:
        cnki_interface = CnkiScraperInterface(proxy=proxy_manager.top_50_proxies)
    else:
        cnki_interface = CnkiScraperInterface()

    literatures = cnki_interface.query(querystr="JN='{}'".format(journal),
                                       period={'start_year': year, 'end_year': year})

    cnki_interface.insert_to_db(literatures=literatures, condition=('journal', journal))


# 1. 初始化设置
JOURNALS = ['经济研究','经济学(季刊)','金融研究','世界经济','中国工业经济','产业经济研究','经济科学','经济学家']
JOURNAL = JOURNALS[2]
YEAR = [str(year) for year in range(2000,2005)]

proxy_manager = ProxyManager()

# 2. 抓取文献数据
threads = []

for y in YEAR:
    t = MultiThread(scraper, args=(JOURNAL,y,proxy_manager), name=y)
    threads.append(t)

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()

'''
def good():
    sign = True
    while sign:
        try:
            print('I am here!')
            bad()
            return 24
        except Exception:
            print('continue!')

def bad():
    return 24/0

print(good())'''