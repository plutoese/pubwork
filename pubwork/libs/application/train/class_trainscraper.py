# coding=UTF-8

"""
=========================================
12306火车余票实时数据爬虫
=========================================

:Author: glen
:Date: 2017.1.7
:Tags: scrape web train
:abstract: 抓取12306火车票实时数据

**类**
==================
TrainStationScraper
    火车站点查询

TrainTicketLeftScraper
    火车余票查询

TrainPriceScraper
    火车票价查询


**简介**
==================
火车站点查询可见http://blog.csdn.net/sentimental_dog/article/details/52673935。


**使用方法**
==================

"""

import re
import itertools
import arrow
from libs.webscraper.class_staticwebscraper import StaticSingleWebScraper
from libs.multithread.class_multithread import MultiThread


class TrainStationScraper:
    def __init__(self, web_site='https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.8994'):
        # 抓取所有站点
        self._static_webscraper = StaticSingleWebScraper(web_site=web_site)

    def scrape(self):
        self._static_webscraper.scrape(verify=False)

        return self.to_stations()

    def to_stations(self):
        stations = dict()
        station_str = re.split('\'',re.split('\'',self._static_webscraper.content)[1])[0]
        for item in re.split('\d*@',station_str)[1:]:
            split_str = re.split('\|',item)
            stations[split_str[2]] = split_str[1]

        return stations


class StationPairsGenerator():
    def __init__(self, stations=None):
        self._stations = stations

    def __call__(self):
        return itertools.permutations(list(self._stations.keys()), 2)


class StationPairValidator:
    def __init__(self):
        self._ticket_left_scraper = TrainTicketLeftScraper()

    def validate_pairs(self, station_pairs, day=None):
        if day is None:
            day = arrow.utcnow().replace(days=1).format('YYYY-MM-DD')
        result = self._ticket_left_scraper.multi_station_pairs_query(pairs=station_pairs,day=day)

        return [record for record in result if len(record['data']) > 0]

    def multi_validate_pars(self, pairs_list, day=None):
        threads = []
        results = []

        for pairs in pairs_list:
            t = MultiThread(self.validate_pairs,(pairs,day))
            threads.append(t)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            results.extend(thread.get_result())

        print('Total', len(results))
        return results


class TrainTicketLeftScraper:
    def __init__(self, station_pairs=None):
        self._station_pairs = station_pairs
        self._fmt = 'http://mobile.12306.cn/weixin/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'
        self._today = arrow.utcnow().format('YYYY-MM-DD')

    def multi_station_pairs_query(self, pairs, day=None):
        result = []
        while pairs:
            one_pair = pairs[0]
            scrape_data = self.one_station_pair_query(pair=one_pair,day=day)
            if scrape_data is not None:
                result.append(scrape_data)
                pairs.pop(0)
        return result

    def multi_thread_query(self, pairs_list, day=None):
        threads = []
        results = []

        for pairs in pairs_list:
            t = MultiThread(self.multi_station_pairs_query,(pairs,day))
            threads.append(t)

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            results.extend(thread.get_result())

        print('Total', len(results))

    def one_station_pair_query(self, pair, day=None):
        try:
            if day is None:
                day = self._today
            website = self._fmt.format(day, pair[0], pair[1])
            web_scraper = StaticSingleWebScraper(website)
            web_scraper.scrape(verify=False, json=True)

            return {'from':pair[0], 'to':pair[1], 'day':day, 'data': web_scraper.json['data']}

        except Exception:
            return None

    @staticmethod
    def generate_check_days(plus=30):
        days = []
        for i in range(plus):
            days.append(arrow.utcnow().replace(days=i).format('YYYY-MM-DD'))
        return days

if __name__ == '__main__':
    station_scraper = TrainStationScraper()
    ticket_scraper = TrainTicketLeftScraper()

    print(ticket_scraper.one_station_pair_query(day='2017-01-09', pair=('JCJ','DIP')))
    print(ticket_scraper.multi_station_pairs_query(day='2017-01-09', pairs=[('JCJ', 'DIP'),('DIP', 'JCJ'),('DIP', 'JCE')]))

