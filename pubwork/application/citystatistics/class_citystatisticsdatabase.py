# coding=UTF-8

"""
=========================================
CityStatisticsDatabase类
=========================================

:Author: glen
:Date: 2017.11.15
:Tags: stats city database
:abstract: 中国城市统计年鉴数据库

**类**
==================
CityStatisticsDatabase
    中国城市统计数据库接口


**使用方法**
==================

"""

import re
import pymongo
import pandas as pd
from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection
from application.admindivision.class_admindivision import AdminDivision


class CityStatisticsDatabase:
    def __init__(self):
        """ 初始化中国城市统计数据库接口

        """
        mongo = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')
        self.conn = MonCollection(mongo,database='region',collection_name='citystatistics').collection

    def find(self,*args,**kwargs):
        """ 调用查询接口

        :param args:
        :param kwargs:
        :return:
        """
        found = list(self.conn.find(*args,**kwargs))
        if len(found) > 0:
            found_data = pd.DataFrame(found)
            found_data['var'] = found_data['variable'] + found_data['unit'].apply(lambda x: ''.join(['(',x,')']))
            pdata = pd.pivot_table(found_data, values='value', index=['year', 'acode', 'region'], columns=['var'])
            pdata = pdata.swaplevel(0, 1, axis=0)
            return pdata

    @property
    def variables(self):
        found = self.conn.find().distinct('variable')
        return pd.DataFrame(sorted(found))


class CityStatistics:
    def __init__(self):
        self.city_stat_databse = CityStatisticsDatabase()
        self.admindivision = AdminDivision()

    def find(self,year=list(range(2000,2016)),variable=None,region=None,boundary='全市'):
        query_str = {'year':{'$in':year},'boundary':boundary}
        if variable is not None:
            if isinstance(variable,str):
                query_str['variable'] = variable
            elif isinstance(variable,(tuple,list)):
                query_str['variable'] = {'$in':variable}
            else:
                print('Unknown type!')
                raise Exception
        if region is not None:
            if isinstance(region,str):
                if re.match('^\d{6}$',region) is not None:
                    query_str['acode'] = region
                else:
                    for ye in year:
                        self.admindivision.set_year(ye)
                        found = self.admindivision[region]
                        if found.shape[0] > 0:
                            query_str['acode'] = str(found.iloc[0,0])
                            break
            elif isinstance(region,(tuple,list)):
                acodes = []
                for reg in region:
                    if isinstance(reg,str):
                        if re.match('^\d{6}$', reg) is not None:
                            acodes.append(region)
                        else:
                            for ye in year:
                                self.admindivision.set_year(ye)
                                found = self.admindivision[reg]
                                if found.shape[0] > 0:
                                    acodes.append(str(found.iloc[0, 0]))
                                    break
                    else:
                        for ye in year:
                            self.admindivision.set_year(ye)
                            found = self.admindivision[tuple(reg)]
                            if found.shape[0] > 0:
                                acodes.append(str(found.iloc[0, 0]))
                                break
                query_str['acode'] = {'$in':acodes}
            else:
                print('Unknown type!')
                raise Exception
        query_str['boundary'] = boundary

        return city_database.find(query_str,
                                  projection={'_id':0,'year':1,'acode':1,'region':1,'value':1,'unit':1,'variable':1,'boundary':1},
                                  sort=[('year',pymongo.ASCENDING),('acode',pymongo.ASCENDING)])


if __name__ == '__main__':
    city_database = CityStatisticsDatabase()
    #city_database.variables.to_excel('d:/data/output/city_variable.xlsx')

    selected = pd.read_excel(r'D:\data\output\selected_variable.xlsx')
    selected_variables = list(selected['variable'])

    '''
    result = city_database.find({'variable':{'$in':selected_variables},'boundary':'全市'},
                                projection={'_id':0,'year':1,'acode':1,'region':1,'value':1,'unit':1,'variable':1,'boundary':1},
                                sort=[('year',pymongo.ASCENDING),('acode',pymongo.ASCENDING)])'''

    city_stat = CityStatistics()
    result = city_stat.find(variable=['人口密度','人均地区生产总值'],region=['北京市',['江苏省','南京市'],'上海市'],boundary='全市')
    print(result)
    #result.to_excel('d:/data/output/citydata.xlsx')
