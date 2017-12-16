# coding = UTF-8

# --------------------------------------------------------------------------------
# utility_web_data_provider文件
# @introduction: 网页数据提供商
# @dependency: None
# @author: plutoese
# @date: 2017.12.04
# ---------------------------------------------------------------------------------

import re
import pymongo
import pandas as pd
from .class_redis import Redis
from .class_mongodb import MongoDB, MonDatabase, MonCollection
from .class_citystatisticsdatabase import CityStatisticsDatabase, CityStatistics


class WebUIDataProvider:
    """ 提供网站UI所需的数据，数据一般储存在Redis数据库

    :return: 无返回值
    """
    def __init__(self):
        self._redisdb = Redis()
        self._mongodb = MongoDB()
        #self._city_stat_db = CityStatisticsDatabase()
        #self._city_stat = CityStatistics()

    @property
    def databse_info(self):
        """ 数据库基本信息

        :return: 返回数据库基本信息
        """
        result = []

        # 数据库名称
        database_names = self._redisdb.get('database_name')
        # 数据库简介
        database_intro = self._redisdb.get('database_intro')
        # 数据库链接
        database_link = self._redisdb.get('database_link')
        # 数据库类型
        database_type = self._redisdb.get('database_type')

        for i in range(len(database_names)):
            result.append({'key':i, 'database_name':database_names[i],
                           'database_intro':database_intro[i],'database_link':database_link[i],
                           'database_type':database_type[i]})
        return result

    @property
    def ceic_data_query_info(self):
        """ CEIC数据查询基本信息

        :return: 返回CEIC查询所需信息
        """
        result = dict()

        # CEIC的时间跨度
        ceic_period = sorted(self._redisdb.get('ceic_period'))
        ceic_start_year = ceic_period[0]
        ceic_end_year = ceic_period[-1]
        result['startYear'] = ceic_start_year
        result['endYear'] = ceic_end_year

        # CEIC的地区
        regions = []
        ceic_region = self._redisdb.get('ceic_region')
        ceic_acode = self._redisdb.get('ceic_acode')
        for i in range(len(ceic_acode)):
            regions.append({'label':ceic_region[i], 'value':ceic_acode[i], 'key':ceic_acode[i]})
        result['region'] = regions

        # CEIC的变量
        ceic_variables = self._redisdb.get('ceic_variable')
        result['variable'] = sorted(list(set(ceic_variables)))

        return result

    @property
    def city_stat_query_info(self):
        """ 城市统计数据查询UI信息

        :return: 返回城市统计数据查询UI信息
        """
        result = dict()

        # 起始和终止年份
        result['startYear'] = 2000
        result['endYear'] = 2015

        # 城市统计数据库的地区
        regions = []
        city_stat_region = self._redisdb.get('city_stat_db_region')
        city_stat_acode = self._redisdb.get('city_stat_db_acode')
        single_province = dict()
        for i in range(len(city_stat_region)):
            if re.match('^[0-9]{2}0{4}$',city_stat_acode[i]) is not None:
                if len(single_province) > 1:
                    regions.append(single_province)

                single_province = {'label': city_stat_region[i], 'value': city_stat_acode[i],
                                   'key': city_stat_acode[i],
                                   'children': []}
            else:
                single_province['children'].append({'label': city_stat_region[i], 'value': city_stat_acode[i], 'key': city_stat_acode[i]})
        result['region'] = regions

        # 城市统计数据库的变量
        city_stat_variables = self._redisdb.get('city_stat_db_variable')
        result['variable'] = city_stat_variables

        return result


class WebDataQuerier:
    """ 网页数据查询接口

    :return: 无返回值
    """
    def __init__(self):
        self._redisdb = Redis()
        self._mongodb = MongoDB()

    @staticmethod
    def region_panel_query(conn, variable, region, start_year, end_year, region_scale=None):
        # 处理地区
        if len(region) == 1 and region[0] == '000000':
            is_all_region = True
        else:
            is_all_region = False

        if region_scale is None:
            if is_all_region:
                found = list(conn.find({'variable': {'$in': variable},
                                        'year': {'$in': list(range(int(start_year),int(end_year)+1))}},
                                       projection={'_id': False, 'acode': True, 'region': True, 'unit': True,
                                                   'variable': True, 'value': True, 'year': True},
                                       sort=[('year', pymongo.ASCENDING), ('acode', pymongo.ASCENDING)]))
            else:
                found = list(conn.find({'variable': {'$in': variable},
                                        'acode': {'$in': region},
                                        'year': {'$in': list(range(int(start_year), int(end_year) + 1))}},
                                       projection={'_id': False, 'acode': True, 'region': True, 'unit': True,
                                                   'variable': True, 'value': True, 'year': True},
                                       sort=[('year', pymongo.ASCENDING), ('acode', pymongo.ASCENDING)]))
        else:
            if region_scale < 2:
                boundary = '全市'
            else:
                boundary = '市辖区'
            if is_all_region:
                found = list(conn.find({'variable': {'$in': variable}, 'boundary':boundary,
                                        'year': {'$in': list(range(int(start_year), int(end_year) + 1))}},
                                       projection={'_id': False, 'acode': True, 'region': True, 'unit': True,
                                                   'variable': True, 'value': True, 'year': True},
                                       sort=[('year', pymongo.ASCENDING), ('acode', pymongo.ASCENDING)]))
            else:
                found = list(conn.find({'variable': {'$in': variable}, 'boundary':boundary,
                                        'acode': {'$in': region},
                                        'year': {'$in': list(range(int(start_year), int(end_year) + 1))}},
                                       projection={'_id': False, 'acode': True, 'region': True, 'unit': True,
                                                   'variable': True, 'value': True, 'year': True},
                                       sort=[('year', pymongo.ASCENDING), ('acode', pymongo.ASCENDING)]))
        return found

    def ceic_query(self, variable, region, start_year, end_year):
        """ CEIC数据查询

        :param list,tuple variable: 变量
        :param region:
        :param start_year:
        :param end_year:
        :return:
        """
        ceic = MonCollection(mongodb=self._mongodb, database='region', collection_name='CEIC')
        found = WebDataQuerier.region_panel_query(ceic.collection, variable=variable,
                                                  region=region, start_year=start_year, end_year=end_year)

        if len(found) > 0:
            found_data = pd.DataFrame(found)
            if 'unit' in list(found_data.columns):
                found_data['var'] = found_data['variable'] + found_data['unit'].apply(lambda x: ''.join(['(', str(x), ')']))
            else:
                found_data['var'] = found_data['variable']
            pdata = pd.pivot_table(found_data, values='value', index=['year', 'acode', 'region'], columns=['var'])
            pdata = pdata.swaplevel(0, 1, axis=0)
            return WebDataQuerier.record_to_ant_table_data(pdata,index_name=['地区代码', '年份', '地区'])
        else:
            return WebDataQuerier.record_to_ant_table_data(pdata=None)

    def city_stat_query(self, variable, region, start_year, end_year, region_scale):
        """ 中国城市统计数据库查询

        :param list,tuple variable: 变量
        :param region:
        :param start_year:
        :param end_year:
        :return:
        """
        citystat = MonCollection(mongodb=self._mongodb, database='region', collection_name='citystatistics')
        found = WebDataQuerier.region_panel_query(citystat.collection, variable=variable, region=region,
                                                  start_year=start_year, end_year=end_year, region_scale=region_scale)

        if len(found) > 0:
            found_data = pd.DataFrame(found)
            if 'unit' in list(found_data.columns):
                found_data['var'] = found_data['variable'] + found_data['unit'].apply(lambda x: ''.join(['(', str(x), ')']))
            else:
                found_data['var'] = found_data['variable']
            pdata = pd.pivot_table(found_data, values='value', index=['year', 'acode', 'region'], columns=['var'])
            pdata = pdata.swaplevel(0, 1, axis=0)
            return WebDataQuerier.record_to_ant_table_data(pdata,index_name=['地区代码', '年份', '地区'])
        else:
            return WebDataQuerier.record_to_ant_table_data(pdata=None)

    def dataset_query(self,user):
        dataset_db = MonCollection(mongodb=self._mongodb, database='webdata', collection_name='userdataset')
        found = list(dataset_db.collection.find({'owner':user},
                                                projection={'_id': False, 'name': True, 'label': True, 'introduction': True,
                                                            'link': True, 'public': True},
                                                sort=[('created', pymongo.DESCENDING)]))
        column_index = ['name','label','introduction']
        mongo_index = ['name','label','introduction']
        file_link = {item['name']:item['link'] for item in found}
        dataset_status = {item['name']:item['public'] for item in found}
        return {'table_data':WebDataQuerier.mongodb_to_ant_table_data(found,column_index,mongo_index),
                'file_link':file_link, 'dataset_status':dataset_status}

    @staticmethod
    def mongodb_to_ant_table_data(mongo_data, column_index, mongo_index):
        table_data = []
        num = 0
        for item in mongo_data:
            record = {column_index[i]:item[mongo_index[i]] for i in range(len(column_index))}
            record.update({'key':str(num)})
            num += 1
            table_data.append(record)
        return table_data


    @staticmethod
    def record_to_ant_table_data(pdata, index_name=None):
        if pdata is None:
            return {'data': None, 'table_columns': [], 'table_data': []}

        new_pdata = pdata.fillna('')
        if index_name is not None:
            table_columns = [{'title':index_name[i], 'dataIndex': pdata.index.names[i],
                              'key': pdata.index.names[i], 'width': 100}
                              for i in range(len(index_name))]
        table_columns.extend([{'title': re.sub('\(nan\)','',pdata.columns[i]), 'dataIndex': ''.join(['var',str(i)]),  'key': ''.join(['var',str(i)])}
                          for i in range(len(pdata.columns))])

        keys = [item['dataIndex'] for item in table_columns]
        num = 1
        table_data = []
        for ind in new_pdata.index:
            record = {'key':str(num)}
            record.update(dict(zip(keys, list(ind) + list(new_pdata.loc[ind,:]))))
            num += 1
            table_data.append(record)

        width = 100 * len(table_columns)

        return {'data': pdata, 'table_columns': table_columns, 'table_data': table_data, 'width': width}

if __name__ == '__main__':
    provider = WebUIDataProvider()
    print(provider.databse_info)
    print(provider.ceic_data_query_info)

    querier = WebDataQuerier()
    querier.ceic_query()
