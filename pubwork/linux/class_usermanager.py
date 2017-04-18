# coding = UTF-8

"""
=========================================
linux下的用户管理类
=========================================

:Author: glen
:Date: 2017.3.18
:Tags: linux ubuntu user
:abstract: linux下的用户管理类

**类**
==================
UserManager


**简介**
==================
linux下的用户管理类


**使用方法**
==================

"""

import os
import re


class UserManager:
    def __init__(self,file=None):
        self._file = file
        self._users = dict()

    def get_users(self):
        if os.path.isfile(self._file):
            with open(self._file,'r') as f:
                for line in f.readlines():
                    user,passwd = re.split(':',line)
                    self._users[user] = re.sub('\n','',passwd)

    def add_users(self,users):
        user_pwd = ''
        if isinstance(users,(tuple,list)):
            for items in users:
                self._users[items[0]] = items[1]
                user = ':'.join([items[0],items[1]])
                user_pwd = ''.join([user_pwd,user,'\n'])
            with open(self._file, 'a') as f:
                f.write(user_pwd[:-1])
        else:
            print('Unknown Type!')
            raise Exception

    def add_single_user(self,user):
        if isinstance(user,(tuple,list)):
            if user[0] not in self._users:
                user_pwd = ':'.join([user[0],user[1]])
            if os.path.isfile(self._file):
                pass
            else:
                pass

    @property
    def users(self):
        return self._users

if __name__ == '__main__':
    user_manager = UserManager(file='/home/plutoese/download/pwd.txt')
    user_manager.get_users()
    user_manager.add_users([('docker','docker'),('Elise','Elise')])
    print(user_manager._users)



