#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
from utils.times import dt_strftime
from selenium.webdriver.common.by import By

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))


class ConfigManager(object):
    """
    定义项目、报告文件目录。元素定位类型、邮件信息、收件人等
    """
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 页面元素目录
    ELEMENT_PATH = os.path.join(BASE_DIR, 'page_element')

    # 报告文件
    REPORT_FILE = os.path.join(BASE_DIR, 'report.html')

    # common
    COMMON_DIR = os.path.join(BASE_DIR, 'common')

    # 元素定位的类型
    LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME,
        'LINK_TEXT': By.LINK_TEXT
    }


    # 收件人
    ADDRESSEE = [
        '1421888657@qq.com',
    ]

    @property  # 创建只读属性
    def log_file(self):
        """日志目录，没有日志文件时创建一个logs文件。XXX.log，XXX：时间"""
        log_dir = os.path.join(self.BASE_DIR, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime()))

    @property
    def ini_file(self):
        """配置文件"""
        ini_file = os.path.join(self.BASE_DIR, 'config', 'config.ini')
        if not os.path.exists(ini_file):
            raise FileNotFoundError("配置文件%s不存在！" % ini_file)
        return ini_file

    def file_dir(self, *args):
        file_dir = os.path.join(self.BASE_DIR)
        for i in args:
            file_dir = os.path.join(file_dir, i)
        return file_dir


# cm：ConfigManager实例化对象
cm = ConfigManager()

if __name__ == '__main__':
    print(cm.file_dir('common', '图片上传.png'))
