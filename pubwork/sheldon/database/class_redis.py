# coding=UTF-8

"""
=========================================
Redis数据库类
=========================================

:Author: glen
:Date: 2017.9.3
:Tags: redis database
:abstract: 连接redis数据库，并进行基本操作。

**类**
==================
Redis
    连接Redis数据库

**使用方法**
==================


**示范代码**
==================
::

"""

import redis


class Redis:
    """ 连接Redis数据库

    :param str host: 数据库主机，默认是'localhost'
    :param int port: 数据库端口，默认是6379
    :param str password: 数据库登录密码
    :return: 无返回值
    """
    def __init__(self, host='106.14.237.43', port=6379, password='z1Yh2900'):
        self._r = redis.Redis(host=host, port=port, password=password)

    def __len__(self):
        return self._r.dbsize()

    def set(self,name,value):
        if isinstance(value,str):
            self._r.set(name=name, value=value)
        elif isinstance(value,(tuple,list)):
            for item in value:
                self._r.rpush(name, item)
        elif isinstance(value,set):
            for item in value:
                self._r.sadd(name, item)
        elif isinstance(value,dict):
            for key,kvalue in value.items():
                self._r.hmset(name,{key:kvalue})
        else:
            pass

    def get(self,name):
        if bytes.decode(db.type(name)) == 'str':
            return self._r.get(name=name)
        elif bytes.decode(db.type(name)) == 'list':
            return [bytes.decode(item) for item in self._r.lrange(name=name,start=0,end=self._r.llen(name=name))]
        elif bytes.decode(db.type(name)) == 'set':
            return {bytes.decode(item) for item in self._r.smembers(name=name)}
        elif bytes.decode(db.type(name)) == 'hash':
            return {bytes.decode(key):bytes.decode(self._r.hgetall(name)[key]) for key in self._r.hgetall(name)}
        else:
            pass

    def clear_all(self):
        self._r.flushdb()

    def type(self,name):
        return self._r.type(name=name)

if __name__ == '__main__':
    db = Redis()
    print(len(db))
    db.clear_all()

    db.set('car',['hello','world'])
    print(db.get('car'))

    db.set('check',{'not','good'})
    print(db.get('check'))

    db.set('mdic',{'name':'Alice','age':24})
    print(db.get('mdic'))


