# coding = UTF-8

import os
import re
import shutil
import pandas as pd
import random

# 0. 设置主目录
BASE_PATH = r'D:\data\English'
is_Vocabulary = False
is_Toefl = False
is_Ielts = False
is_Englis7000 = False
is_NewConcept = False
is_Random = True

# 1. 导入所有的word，组成all_word_dict,{'word':'path'}
all_words = dict()
for line in open(os.path.join(BASE_PATH,'American/content.txt')):
    all_words[re.split('\.',(re.split('\\\\',line)[-1]))[0]] = os.path.join(BASE_PATH,'American',re.split('\\\\',line)[-2])

# 2. 导入单词本
if is_Vocabulary:
    word_data = pd.read_excel(r'D:\data\English\words.xlsx', header=None)

    words = []
    for col in word_data.columns:
        words.extend(list(word_data[col]))

    for word in words:
        if all_words.get(word) is not None:
            shutil.copy2(os.path.join(all_words[word], ''.join([word,'.mp3'])), os.path.join(BASE_PATH, 'pro/Vocabulary'))
        else:
            print(word)

if is_Toefl:
    toefl_word = list(pd.read_excel(r'D:\data\English\toefl.xls', header=0).iloc[:,0])

    for word in toefl_word:
        if all_words.get(word) is not None:
            shutil.copy2(os.path.join(all_words[word], ''.join([word,'.mp3'])), os.path.join(BASE_PATH, 'pro/Toefl'))
        else:
            print(word)

if is_Ielts:
    ielts_word = list(pd.read_excel(r'D:\data\English\ielts.xlsx', header=None).iloc[:,0])
    ielts_word = [re.sub('\s+','',word) for word in ielts_word]

    for word in ielts_word:
        if all_words.get(word) is not None:
            shutil.copy2(os.path.join(all_words[word], ''.join([word,'.mp3'])), os.path.join(BASE_PATH, 'pro/Ielts'))
        else:
            print(word)

if is_Englis7000:
    English7000_word = list(pd.read_excel(r'D:\data\English\English7000.xlsx', header=None).iloc[:, 0])
    #ielts_word = [re.sub('\s+', '', word) for word in English7000_word]

    for word in English7000_word:
        if all_words.get(word) is not None:
            shutil.copy2(os.path.join(all_words[word], ''.join([word, '.mp3'])), os.path.join(BASE_PATH, 'pro/English7000'))
        else:
            print(word)

if is_NewConcept:
    Newconcept_words = []
    for line in open(os.path.join(BASE_PATH, 'Newconcept4new.txt'),encoding='UTF-8'):
        Newconcept_words.append(re.split('\s+',line)[0])
    #for line in open(os.path.join(BASE_PATH, 'Newconcept3.txt')):
    #    Newconcept_words.append(re.split('\s+',line)[0])
    #for line in open(os.path.join(BASE_PATH, 'Newconcept4.txt')):
    #    Newconcept_words.append(re.split('\s+',line)[0])
    for word in Newconcept_words:
        if all_words.get(word) is not None:
            shutil.copy2(os.path.join(all_words[word], ''.join([word, '.mp3'])), os.path.join(BASE_PATH, 'pro/Newconcept4'))
        else:
            print(word)

if is_Random:
    Number = 40
    word_pool = [os.path.join(BASE_PATH,r'pro\Newconcept',efile) for efile in os.listdir(os.path.join(BASE_PATH,'pro/Newconcept'))]

    i = 0
    while word_pool:
        mpath = os.path.join(BASE_PATH, r'pro\random', str(i))
        if len(word_pool) >= Number:
            for word_file in random.sample(word_pool,Number):
                if not os.path.exists(mpath):
                    os.mkdir(mpath)
                shutil.copy2(word_file,mpath)
                word_pool.pop(word_pool.index(word_file))
        else:
            print('hhhh',word_pool)
            print(mpath)
            if not os.path.exists(mpath):
                os.mkdir(mpath)
            for word_file in word_pool:
                print('ppp',word_file)
                shutil.copy2(word_file, mpath)
            word_pool.clear()
        i += 1


'''
# 导入单词
word_data = pd.read_excel(r'D:\data\English\words.xlsx',header=None)

words = []
for col in word_data.columns:
    words.extend(list(word_data[col]))

print(len(words))

# search and copy
print(os.listdir(r'D:\data\English\American'))

all_words = dict()
for line in open(r'D:\data\English\American\content.txt'):
    all_words[re.split('\.',(re.split('\\\\',line)[-1]))[0]] = re.split('\\\\',line)[-2]
print(all_words)'''
