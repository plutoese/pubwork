# coding = UTF-8

# --------------------------------------
# @title: cnki文献抓取主程序
# @author: glen
# @date: 2017.06.26
# --------------------------------------


from sheldon.webscraper.class_proxymanager import ProxyManager
from application.cnkiscraper.class_cnkiscraper import CnkiScraperInterface
import concurrent.futures


# 0. 函数
def scraper(journal, year, proxy_manager=None):
    cnki_interface = CnkiScraperInterface(proxy=proxy_manager.top_50_proxies,type=0)

    literatures = cnki_interface.query(querystr="JN='{}'".format(journal),
                                       period={'start_year': year, 'end_year': year})

    cnki_interface.insert_to_db(literatures=literatures, condition=('journal', journal))


# 1. 初始化设置
JOURNALS = ['河北经贸大学学报']

for i in range(0,1):
    JOURNAL = JOURNALS[i]
    YEAR = [str(year) for year in range(2010,2018)]

    proxy_manager = ProxyManager()

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for y in YEAR:
            executor.submit(scraper, JOURNAL, y, proxy_manager)
