# coding = UTF-8

import re
import os
import pickle
import pandas as pd
import numpy as np
import math
from itertools import combinations, permutations
from sheldon.database.class_mongodb import MongoDB, MonDatabase, MonCollection
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6

# output to static HTML file
output_file("chart.html")

# 0. Setup
BASE_PATH = r'D:\data\cnki\pkl'
XLS_PATH = r'D:\data\cnki\xls'

# 1. 数据库
mongo = MongoDB(conn_str='mongodb://mongouser:z1Yh2900@123.207.185.126:27017/')
mdb = MonDatabase(mongodb=mongo, database_name='papers')
con = MonCollection(mongo,mdb,collection_name='cnki').collection

journals = sorted(con.find().distinct('journal'))
period = [str(year) for year in range(2010,2018)]

ORIGINAL_AUTHOR_OUTPUT = False
BUILD_AUTHOR_DICT = False
ORGANIZE_AUTHOR = False
RECORD_DATAFRAME = False
CREATE_WEIGHT = False
CREATE_WEIGHT2 = False
DEA = False
DEA2 = True


# 是否同一个地址
def is_same_address(addresses):
    if len(addresses) < 2:
        return True
    sorted_addresses = sorted(addresses,key=len)
    starter = ''.join(re.split('(大学|学院|银行|党校|实验室)', sorted_addresses[0])[0:2])
    for item in sorted_addresses[1:]:
        #print(sorted_addresses[0],'=>',starter,'->',item)
        if re.search(starter, item) is None:
            return False
    return True


if ORIGINAL_AUTHOR_OUTPUT:
    for journal in journals:
        author_data = []
        for year in period:
            records = con.find({'journal':journal,'year':year})
            for record in records:
                authors = record.get('author')
                addresses = record.get('address')
                if authors is None:
                    print('No author!')
                    raise Exception
                else:
                    if addresses is None:
                        for author in authors:
                            author_data.append((author,'',year))
                        print('No address', record)
                    else:
                        if len(authors) == len(addresses):
                            for author,address in zip(authors,addresses):
                                author_data.append((author, address, year))
                        elif len(addresses) == 1:
                            for author in authors:
                                author_data.append((author, addresses[0], year))
                        else:
                            author_data.append(('|'.join(authors),'|'.join(addresses),year))

        print(author_data)
        author_data = pd.DataFrame.from_records(author_data, columns=['author', 'address', 'year'])
        author_data.to_excel(os.path.join(BASE_PATH,'{}.xlsx'.format(journal)))

if BUILD_AUTHOR_DICT:
    F = open(os.path.join(r'D:\data\cnki\process','author_dict.pkl'), 'wb')

    author_dict = dict()
    author_year_dict = dict()
    unknown_author_dict = dict()
    unknown_author_year_dict = dict()
    multiple_author_dict = dict()
    multiple_author_year_dict = dict()
    for xls_file in os.listdir(XLS_PATH):
        file_name = os.path.join(XLS_PATH, xls_file)
        mdata = pd.read_excel(file_name)
        for ind in mdata.index:
            authors = re.split('\|',mdata.loc[ind,'author'])
            if len(authors) < 2:
                if isinstance(mdata.loc[ind,'address'],str):
                    if authors[0] in author_dict:
                        author_dict[authors[0]].add(mdata.loc[ind,'address'])
                    else:
                        author_dict[authors[0]] = set([mdata.loc[ind,'address']])

                    if (authors[0],mdata.loc[ind,'year']) not in author_year_dict:
                        author_year_dict[(authors[0],mdata.loc[ind,'year'])] = set([mdata.loc[ind,'address']])
                    else:
                        author_year_dict[(authors[0],mdata.loc[ind,'year'])].add(mdata.loc[ind,'address'])
                else:
                    unknown_author_dict[authors[0]] = mdata.loc[ind,'address']
                    unknown_author_year_dict[(authors[0],mdata.loc[ind,'year'])] = mdata.loc[ind,'address']
            else:
                if mdata.loc[ind,'author'] in multiple_author_dict:
                    multiple_author_dict[mdata.loc[ind,'author']].add(mdata.loc[ind,'address'])
                else:
                    multiple_author_dict[mdata.loc[ind,'author']] = set([mdata.loc[ind,'address']])

                if (mdata.loc[ind,'author'], mdata.loc[ind, 'year']) not in multiple_author_year_dict:
                    multiple_author_year_dict[(mdata.loc[ind,'author'], mdata.loc[ind, 'year'])] = set([mdata.loc[ind, 'address']])
                else:
                    multiple_author_year_dict[(mdata.loc[ind,'author'], mdata.loc[ind, 'year'])].add(mdata.loc[ind, 'address'])


    #print(author_dict)
    #print(author_year_dict)
    #print(unknown_author_dict)
    #print(unknown_author_year_dict)
    print(multiple_author_dict)
    print(multiple_author_year_dict)

    pickle.dump([author_dict, author_year_dict, unknown_author_dict, unknown_author_year_dict,multiple_author_dict,multiple_author_year_dict], F)
    F.close()

if ORGANIZE_AUTHOR:
    F = open(os.path.join(r'D:\data\cnki\process','author_dict.pkl'), 'rb')
    author_dict, author_year_dict, unknown_author_dict, unknown_author_year_dict, multiple_author_dict, multiple_author_year_dict = pickle.load(F)
    print(len(author_dict),len(unknown_author_dict),len(multiple_author_dict))

    author_address_dict = dict()
    for key in author_dict:
        if len(author_dict[key]) < 2:
            author_address_dict[key] = author_dict[key]
        else:
            if is_same_address(author_dict[key]):
                author_address_dict[key] = author_dict[key]
            else:
                origin_address = set()
                try_address = set()
                temp_address = set()
                count = 1
                for year in range(2010,2018):
                    if author_year_dict.get((key, year)) is not None:
                        try_address.update(author_year_dict.get((key, year)))
                        if not is_same_address(try_address):
                            for item in author_year_dict.get((key, year)):
                                tmp_address = set(origin_address)
                                tmp_address.add(item)
                                if is_same_address(tmp_address):
                                    origin_address = set(tmp_address)
                                else:
                                    temp_address.add(item)
                            origin_address = set(try_address)
                            try_address = set(temp_address)
                            count += 1
                        else:
                            origin_address = set(try_address)
                if count < 3:
                    author_address_dict[key] = author_dict[key]

    print(len(author_address_dict))
    updated_author_address_dict = dict()
    for key in author_address_dict:
        if len(key) < 4:
            updated_author_address_dict[key] = author_address_dict[key]
    print(len(updated_author_address_dict))

    F1 = open(os.path.join(r'D:\data\cnki\process', 'updated_author_address_dict.pkl'), 'wb')
    pickle.dump(updated_author_address_dict,F1)
    F1.close()

if RECORD_DATAFRAME:
    print('start!')
    F2 = open(os.path.join(r'D:\data\cnki\process', 'updated_author_address_dict.pkl'), 'rb')
    updated_author_address_dict = pickle.load(F2)

    my_record = []
    for journal in journals:
        for year in period:
            records = con.find({'journal': journal, 'year': year})
            for record in records:
                authors = record.get('author')
                valid_authors = dict()
                if authors is not None:
                    for i in range(len(authors)):
                        if authors[i] in updated_author_address_dict and record.get('address') is not None:
                            if len(updated_author_address_dict[authors[i]] & set(record.get('address'))) > 0:
                                valid_authors[authors[i]] = i
                if len(valid_authors) > 0:
                    print({'author': valid_authors, 'journal': journal, 'year': year})
                    my_record.append({'author': valid_authors, 'journal': journal, 'year': year})
    print(len(my_record))
    F3 = open(os.path.join(r'D:\data\cnki\process', 'valid_records.pkl'), 'wb')
    pickle.dump(my_record, F3)
    F3.close()

if CREATE_WEIGHT:
    F4 = open(os.path.join(r'D:\data\cnki\process', 'valid_records.pkl'), 'rb')
    valid_records = pickle.load(F4)

    # valid_record for years
    valid_records_2010 = []
    valid_records_2011 = []
    valid_records_2012 = []
    valid_records_2013 = []
    valid_records_2014 = []
    valid_records_2015 = []
    valid_records_2016 = []
    valid_records_2017 = []
    valid_records_2010_to_2016 = []
    for record in valid_records:
        if record['year'] == '2010':
            valid_records_2010.append(record)
            valid_records_2010_to_2016.append(record)
        if record['year'] == '2011':
            valid_records_2011.append(record)
            valid_records_2010_to_2016.append(record)
        if record['year'] == '2012':
            valid_records_2012.append(record)
            valid_records_2010_to_2016.append(record)
        if record['year'] == '2013':
            valid_records_2013.append(record)
            valid_records_2010_to_2016.append(record)
        if record['year'] == '2014':
            valid_records_2014.append(record)
            valid_records_2010_to_2016.append(record)
        if record['year'] == '2015':
            valid_records_2015.append(record)
            valid_records_2010_to_2016.append(record)
        if record['year'] == '2016':
            valid_records_2016.append(record)
            valid_records_2010_to_2016.append(record)
        if record['year'] == '2017':
            valid_records_2017.append(record)

    authors = []
    for record in valid_records_2010_to_2016:
        authors.extend(record['author'].keys())
    authors = set(authors)

    F5 = open(os.path.join(r'D:\data\cnki\process', 'authors_and_recore2010_2016.pkl'), 'wb')
    pickle.dump([valid_records_2010_to_2016,authors], F5)
    F5.close()

if CREATE_WEIGHT2:
    F6 = open(os.path.join(r'D:\data\cnki\process', 'authors_and_recore2010_2016.pkl'), 'rb')
    valid_records_2010_to_2016, authors = pickle.load(F6)

    author_publication = dict(zip(sorted(authors),[0]*len(authors)))

    for record in valid_records_2010_to_2016:
        for author in record['author']:
            author_publication[author] = author_publication[author] + 1

    active_authors = set()
    for author in author_publication:
        if author_publication[author] > 7:
            active_authors.add(author)
    sorted_active_authors = sorted(active_authors)
    num_of_active_authors = len(sorted_active_authors)
    active_number_authors_dict = dict(zip(range(num_of_active_authors),sorted_active_authors))
    active_authors_number_dict = {active_number_authors_dict[key]:key for key in active_number_authors_dict}

    # impactor
    impact_file = pd.read_excel(os.path.join(r'D:\data\cnki\process', 'journal_if.xlsx'))
    impact_file = impact_file.set_index(['journal'])
    tdict = impact_file.to_dict(orient='dict')
    fif_dict = tdict['fif']
    zif_dict = tdict['zif']
    fif_dict['现代财经(天津财经大学学报)'] = 1.502
    zif_dict['现代财经(天津财经大学学报)'] = 0.722
    fif_dict['经济学(季刊)'] = 6.482
    zif_dict['经济学(季刊)'] = 4.561
    print(fif_dict)

    # author weight matrix
    author_wmatix = pd.DataFrame(np.mat(np.zeros([num_of_active_authors,num_of_active_authors])),index=sorted_active_authors,columns=sorted_active_authors)
    print(author_wmatix)


    active_records = []
    author_output = pd.DataFrame(np.zeros([num_of_active_authors,3]),index=sorted_active_authors,columns=['quantity','fifquality','zifquality'])
    for record in valid_records_2010_to_2016:
        authors = set(record['author'].keys()) & active_authors
        if len(authors) > 1:
            for pair in permutations(authors,2):
                author_wmatix.loc[pair] += 1

        if len(authors) > 0:
            weight = {i:(math.pow(2,-i)/sum([math.pow(2,-i) for i in range(max(record['author'].values())+1)])) for i in range(max(record['author'].values())+1)}

            #print('------',record)
            #print('weight: ',weight)
            for author in record['author']:
                if author in authors:
                    #print('hh',record['author'][author],weight)
                    author_output.loc[author,'quantity'] += weight[record['author'][author]]
                    author_output.loc[author, 'fifquality'] += weight[record['author'][author]] * fif_dict[record['journal']]
                    author_output.loc[author, 'zifquality'] += weight[record['author'][author]] * zif_dict[record['journal']]
                    #print('author: ',author,record['author'][author],weight[record['author'][author]])

    #author_wmatix.to_csv(os.path.join(r'D:\data\cnki\process', 'author_matrix.csv'))
    new_author_wmatrix = pd.DataFrame(author_wmatix.values)
    print('heeeel',new_author_wmatrix.values)
    #new_author_wmatrix.columns = [str(i) for i in range(num_of_active_authors)]
    #new_author_wmatrix.indexes = [str(i) for i in range(num_of_active_authors)]
    #print('new',new_author_wmatrix)
    new_author_wmatrix.to_stata(os.path.join(r'D:\data\cnki\regdata', 'author_matrix7.dta'))
    author_output.to_excel(os.path.join(r'D:\data\cnki\regdata', 'author_output7.xlsx'))

if DEA:
    i = 0
    for journal in journals:
        for year in period:
            records = con.find({'journal': journal, 'year': year},projection={'_id':0,'author':1,'address':1,'journal':1,'year':1,})
            process_dataframe = pd.DataFrame.from_records(list(records))
            process_dataframe['numberofauthor'] = process_dataframe['author'].apply(len)
            print(i,journal,year)
            if i < 1:
                all_dataframe = process_dataframe
            else:
                all_dataframe = pd.concat([all_dataframe,process_dataframe])
            i += 1

    F8 = open(os.path.join(r'D:\data\cnki\process', 'allrecords.pkl'), 'wb')
    pickle.dump(all_dataframe, F8)
    F8.close()

if DEA2:
    F9 = open(os.path.join(r'D:\data\cnki\process', 'allrecords.pkl'), 'rb')
    all_dataframe = pickle.load(F9)

    print(all_dataframe)
    grouped = all_dataframe.loc[:,['author','year','numberofauthor','journal']].groupby('journal')
    time_coauthor = grouped.aggregate(np.mean)
    print(time_coauthor)
    time_coauthor.to_excel(os.path.join(r'D:\data\cnki\process', 'numberofcoauthor.xlsx'))