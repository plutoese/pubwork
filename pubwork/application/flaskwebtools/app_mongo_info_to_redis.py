# coding = UTF-8

# --------------------------------------------------------------------------------
# app_mongo_info_to_redis文件
# @introduction: 提取mongodb信息到Redis数据库
# @dependency: None
# @author: plutoese
# @date: 2017.12.04
# ---------------------------------------------------------------------------------


import re
import pandas as pd
from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection
from sheldon.database.class_redis import Redis
from application.citystatistics.class_citystatisticsdatabase import CityStatisticsDatabase, CityStatistics

# 0. 初始化和配置
db = Redis()

IS_DATABASE_INFO = False
IS_CITY_STAT_REGION = True

# 提取数据库信息到Redis数据库
if IS_DATABASE_INFO:
    database_info = [{'database_name':'中国综合社会调查数据库(CGSS)',
                      'introduction':'CGSS是我国最早的全国性、综合性、连续性学术调查项目,全面地收集社会、社区、家庭、个人多个层次的数据。',
                      'link':'/csgg_database','type':'微观社会调查数据库'},
                     {'database_name':'CEIC中国数据库',
                      'introduction':'CEIC数据库有包含超过30万条的中国宏观经济、行业以及区域划分的数据。',
                      'link':'/ceic_database','type':'宏观经济社会数据库'},
                     {'database_name':'中国城市统计数据库',
                      'introduction':'中国省地级的宏观经济数据，来源于中国城市统计年鉴。',
                      'link':'/city_stat_database','type':'宏观经济社会数据库'},
                     {'database_name':'中国城市空气质量数据库',
                      'introduction':'中国主要城市空气质量数据，来源于环境保护部数据中心的空气质量日报。',
                      'link':'/air_quality_database','type':'宏观经济社会数据库'},
                     {'database_name':'中国医院等级数据库',
                      'introduction':'中国主要医院等级数据，来源于国家卫生和计生委。',
                      'link':'/hospital_class_database','type':'宏观经济社会数据库'},
                     {'database_name':'中国省级统计数据库',
                      'introduction':'中国省级地区经济统计数据，来源于国家统计局。',
                      'link':'/province_stat_database','type':'宏观经济社会数据库'}]

    database_name = [item['database_name'] for item in database_info]
    database_intro = [item['introduction'] for item in database_info]
    database_link = [item['link'] for item in database_info]
    database_type = [item['type'] for item in database_info]

    db.delete('database_name')
    db.delete('database_intro')
    db.delete('database_link')
    db.delete('database_type')

    db.set('database_name',database_name)
    db.set('database_intro',database_intro)
    db.set('database_link',database_link)
    db.set('database_type',database_type)

# 提取城市统计数据库信息到Redis数据库
if IS_CITY_STAT_REGION:
    city_db = CityStatisticsDatabase()
    '''
    all_regions = dict()
    for year in range(2015,1999,-1):
        acode_found = city_db.conn.find({'year':year}).distinct('acode')
        for code in acode_found:
            region = city_db.conn.find_one({'year':year, 'acode':code})['region']
            if code in all_regions:
                if len(re.split('\|',all_regions[code])) < 2:
                    if region != all_regions[code]:
                        all_regions[code] = '|'.join([all_regions[code],region])
                else:
                    if region not in re.split('\|',all_regions[code]):
                        all_regions[code] = '|'.join([all_regions[code],region])
            else:
                all_regions[code] = region
    print(len(all_regions))

    regions_sorted = sorted(zip(all_regions.keys(), all_regions.values()))
    print(regions_sorted)

    #db.set('city_stat_db_acode', [item[0] for item in regions_sorted])
    #db.set('city_stat_db_region', [item[1] for item in regions_sorted])'''

    city_stat_variable = city_db.conn.find().distinct('variable')
    #print(city_stat_variable)
    db.set('city_stat_db_variable', city_stat_variable)





