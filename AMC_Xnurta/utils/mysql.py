import logging
import os
import sys
from symtable import Class

from common.readconfig import ini
from contextlib import contextmanager
import pymysql.cursors
from config.conf import cm

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))

# class DB:
#     # 初始化数据库连接
#     def __init__(self):
#         self.db = pymysql.connect()
#
#     def search_db(self,sql):
#         cursor = self.db.cursor()
#         query = sql
#         cursor.execute(query)
#         results = cursor.fetchall()
#         logging.info(sql+'查询结果：')
#         logging.info(results)
#         assert len(results) > 0, "No data found in the table"
#         cursor.close()



class DB:
    def __init__(self, host=ini.HOST, user=ini.SqlUser, password=ini.SqlPaw, database=ini.database, port=int(ini.port),charset='utf8mb4'):
        """
        初始化数据库连接
        :param host: 数据库主机地址
        :param user: 数据库用户名
        :param password: 数据库密码
        :param database: 数据库名称
        :param port: 数据库端口
        :param charset: 数据库字符集
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        self.connection = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.database,
            port=self.port,
            charset=self.charset
        )

    def close(self):
        """关闭数据库连接"""
        if self.connection:
            self.connection.close()
            self.connection = None

    @contextmanager
    def cursor(self):
        """
        创建一个数据库游标，确保游标在使用后正确关闭
        """
        if not self.connection:
            self.connect()
        cursor = self.connection.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def search_db(self, sql):
        """
        执行 SQL 查询并返回结果
        :param sql: SQL 查询语句
        :return: 查询结果
        """
        with self.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
            logging.info(f"SQL 查询: {sql}")
            logging.info(f"查询结果: {results}")
            assert len(results) > 0, "未查询到数据"
            return results

if __name__ == '__main__':
    search_db("select descr from amc_model_template where name='Unique Reach';")