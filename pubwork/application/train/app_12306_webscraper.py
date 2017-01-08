# coding=UTF-8

# ============================
# @app: 检验火车站点间是否有直通车
# @author: glen
# @date: 2017.1.8
# ============================

import pickle
from libs.database.class_mongodb import MongoDB, MonDatabase, MonCollection
from libs.application.train.class_trainscraper import TrainStationScraper, TrainTicketLeftScraper
from libs.application.train.class_trainscraper import StationPairsGenerator, StationPairValidator

# 0. 初始化
train_db = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')
train_station_collection = MonCollection(database=MonDatabase(mongodb=train_db, database_name='train'),
                                         collection_name='stations')
day = '2017-01-10'

DOWNLOAD = False
LOAD = True
FILE_NAME = 'station_pairs.pkl'

# 1. 爬取站点名，并且储存所有站点对进入数据库
if DOWNLOAD:
    F = open(FILE_NAME, 'wb')
    Stations = TrainStationScraper().scrape()
    All_Station_Pairs = list(StationPairsGenerator(stations=Stations)())

    pickle.dump(All_Station_Pairs, F)
    F.close()

# 2. 验证站点
if LOAD:
    F = open(FILE_NAME, 'rb')
    All_Station_Pairs = pickle.load(F)
    All_Station_Pairs = All_Station_Pairs[0:100000]

    validator = StationPairValidator()
    group = 10000
    check_times = 3
    for i in range(0,len(All_Station_Pairs),group):
        station_pairs_list = All_Station_Pairs[i:i+group]
        thread_group = 500
        results = []
        for i in range(check_times):
            results.append(validator.multi_validate_pars(pairs_list=[station_pairs_list[i:(i + thread_group)] for i in range(0, len(station_pairs_list), thread_group)],
                                                         day='2017-01-11'))

        result_len = [len(item) for item in results]
        print(result_len)
        result = results[result_len.index(max(result_len))]
        for record in result:
            record.pop('data')
            found = train_station_collection.find_one(record)
            if found is None:
                train_station_collection.insert_one(record)



