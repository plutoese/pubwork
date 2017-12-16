# coding=UTF-8

# --------------------------------------------------------------------------------
# models文件
# @introduction: 初始化变量，函数和类
# @dependency: None
# @author: plutoese
# @date: 2017.12.04
# ---------------------------------------------------------------------------------

import os
import shutil
import re
import datetime
from .lib.class_mongodb import MongoDB, MonDatabase, MonCollection
from .lib.class_redis import Redis

# ---------------
#      参数
# ---------------

# 数据库连接
redis_db = Redis()
mongo_db = MongoDB()

# 参数设定
UPLOAD_FOLDER = './static/file/uploads/'
ALLOWED_EXTENSIONS = set(['xls', 'xlsx'])

# 单个用户可管理的数据集的上限
LIMIT_DATASET = 20


# ---------------
#      类
# ---------------

class UserDataSet():
    """ 管理用户数据集

    """
    def __init__(self):
        # 连接用户数据集的MongoDB数据库
        self._mongo_db = MonCollection(mongodb=mongo_db, database='webdata', collection_name='userdataset')

    def update_one(self,filter,update):
        """ 更新用户数据集信息

        :param dict filter: 筛选条件
        :param dict update: 更新信息
        :return: 返回更新的记录
        """
        self._mongo_db.collection.find_one_and_update(filter=filter,update=update)
        return self._mongo_db.collection.find_one(filter=filter)

    def delete_one(self,filter):
        """ 删除一个用户数据集

        :param dict filter: 筛选条件
        :return:
        """
        filepath = self._mongo_db.collection.find_one(filter=filter)['link']
        result = self._mongo_db.collection.delete_one(filter=filter)
        os.remove(filepath)
        if redis_db.exists('_'.join([filter['owner'],'dataset'])) and redis_db._r.hexists('_'.join([filter['owner'],'dataset']), filter['name']):
            redis_db._r.hdel('_'.join([filter['owner'],'dataset']),filter['name'])
        else:
            raise Exception
        if result.deleted_count == 1:
            return True
        return False


# ---------------
#      函数
# ---------------

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_dataset(info_data):
    """ 保存数据集，处理的步骤如下：复制数据集到userfile对应的用户目录下，添加记录到数据库

    :param info_data:
    :return:
    """
    user = info_data['user']

    to_be_copied_file_path = ''.join(['./static', re.split('static', info_data['savedDatasetName'])[-1]])
    file_type = re.split('\.', os.path.basename(to_be_copied_file_path))[-1]
    dataset_name = info_data['newDatasetName']
    destination_path = './static/file/userfile/{}/'.format(user)

    if not os.path.isdir(destination_path):
        os.mkdir(destination_path)

    destination_filepath = ''.join([destination_path, dataset_name, '.', file_type])

    result = util_save_dataset(owner=user, dataset_name=dataset_name, copy_from=to_be_copied_file_path,
                               copy_to=destination_filepath, type=file_type)

    return result


def upload_dataset(owner, copy_from, copy_to):
    dataset_name, type = re.split('\.', os.path.basename(copy_from))

    result = util_save_dataset(owner=owner, dataset_name=dataset_name, copy_from=copy_from,
                               copy_to=copy_to, type=type)

    return result


def util_save_dataset(owner, dataset_name, copy_from=None, copy_to=None, type='xlsx'):

    conn = MonCollection(mongodb=mongo_db, database='webdata', collection_name='userdataset')

    if len(owner) > 0:
        user = owner
    else:
        user = 'anonymous'

    mkey = '_'.join([user, 'dataset'])
    if redis_db.exists(mkey):
        if redis_db._r.hlen(mkey) > LIMIT_DATASET:
            message = '保存的数据集超出{}个'.format(LIMIT_DATASET)
        else:
            message = '数据集已保存'
            redis_db._r.hset(mkey, dataset_name, copy_to)
            conn.collection.insert_one({'name': dataset_name, 'owner': user, 'label': '', 'introduction': '',
                                        'link': copy_to, 'type': type, 'public': False,
                                        'created': datetime.datetime.now()})
            shutil.copyfile(copy_from, copy_to)

            conn.close()
    else:
        message = '数据集已保存'
        redis_db.set(mkey, {dataset_name: copy_to})
        conn.collection.insert_one({'name': dataset_name, 'owner': user, 'label': '', 'introduction': '',
                                    'link': copy_to, 'type': 'xlsx', type: False,
                                    'created': datetime.datetime.now()})
        shutil.copyfile(copy_from, copy_to)
        conn.close()

    result = {'message': message}

    return result





