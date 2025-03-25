#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import configparser
from config.conf import cm
HOME = 'HOME'
DATABASE = 'DATABASE'

# HOST
URL = 'URL'
USER = 'USER'
PASSWD = 'PASSWD'
# DATABASE
DATA = 'DATA HOST'
SqlUser = 'DATA USER'
SqlPaw = 'DATA PASSWD'
port = 'DATA PORT'
database = 'DATABASE'

'''
读取配置文件
url、code、user、passwd：获取网站地址、企业名称、用户名、密码

'''


class ReadConfig(object):
    """配置文件"""

    def __init__(self):
        # 读取config下config.ini文件
        self.config = configparser.RawConfigParser()
        self.config.read(cm.ini_file, encoding='utf-8')

    def _get(self, section, option):
        """获取config.ini中section下option对应的值。
        section=HOST,option='CODE:获取【HOTS】下CODE对应的值'"""
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """更新config.ini下的值"""
        self.config.set(section, option, value)
        with open(cm.ini_file, 'w') as f:
            self.config.write(f)

    # HOST
    @property
    def url(self):
        return self._get(HOME, URL)


    @property
    def user(self):
        return self._get(HOME, USER)

    @property
    def passwd(self):
        return self._get(HOME, PASSWD)

    # DATABASE
    @property
    def HOST(self):
        return self._get(DATABASE, DATA)


    @property
    def SqlUser(self):
        return self._get(DATABASE, SqlUser)

    @property
    def SqlPaw(self):
        return self._get(DATABASE, SqlPaw)

    @property
    def database(self):
        return self._get(DATABASE, database)

    @property
    def port(self):
        return self._get(DATABASE, port)

ini = ReadConfig()

if __name__ == '__main__':
    print(ini.url, ini.user, ini.passwd)
