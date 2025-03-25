#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import logging
import os
import sys
import time

import allure
import pytest
from utils.logger import log

from page.webpage import WebPage
from common.readelement import Element
from common.readconfig import ini
from config.conf import cm
from page_object.通用 import Common

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))

# 获取element.yaml
elementUniqueReach = Element('UniqueReach')
elementcommon = Element('common')
elementSearchTermAnalysis = Element('SearchTermAnalysis')
elementlogin = Element('登录')

# 用户池


class LoginObject(Common):
    """封装页面登录操作。使用方法：LoginObject(drivers)"""
    def logintest(self, username, passwd, url=ini.url):
        """
        登录，如果有更新提示关闭提示
        :param url: 网站
        :param username: 用户名
        :param passwd: 密码
        :return:
        """
        logging.info(f'登录网站: {url}')

        with allure.step(f"登录网站: {url}"):
            self.get_url(url)

        with allure.step("输入用户名密码"):
            if username:
                self.input_text(elementlogin['账号'], username)
            if passwd:
                self.input_text(elementlogin['密码'], passwd)
            allure.attach(f"输入: 用户名：{username}, 密码：{passwd}", name="用户名/密码")

        self.is_click(elementlogin['登录'])
        time.sleep(1)
        with allure.step("登录提示校验"):
            self._check_login_prompt(username, passwd)

        if username and passwd:
            if username == "leo.sui@sparkxmarketing.com" and passwd == "123456A":
                log.info('登录成功，等待加载数据')
                time.sleep(10)
            else:
                allure.attach('用户名或密码错误', name="提示")
                assert self.is_element_exsist(elementlogin['用户名密码为空错误'])

    def _check_login_prompt(self, username, passwd):
        """
        检查登录提示信息
        :param username: 用户名
        :param passwd: 密码
        """
        if not username and not passwd:
            allure.attach('请输入邮箱/手机号', name="提示")
            allure.attach('提示：请输入密码', name="提示")
            var = self.find_elements(elementlogin['用户名密码为空提示'])[0].text
            print('----------------')
            print(var)
            print('----------------')
            assert "请输入邮箱/手机号" in self.element_text(elementlogin['用户名密码为空提示'], num='0')
            assert "请输入密码" in self.element_text(elementlogin['用户名密码为空提示'], num='1')
        elif not username:
            allure.attach('提示：请输入邮箱/手机号', name="提示")
            assert "请输入邮箱/手机号" in self.element_text(elementlogin['用户名密码为空提示'])
        elif not passwd:
            allure.attach('提示：请输入密码', name="提示")
            assert "请输入密码" in self.element_text(elementlogin['用户名密码为空提示'])

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    @allure.step("登录")
    def login(self, url=ini.url):
        """
        登录网站
        :param url: 网站地址
        """
        # 获取当前 worker_id 并选择用户
        user = self.get_user_by_worker_id()
        # # 访问网站
        self.get_url(url)
        # 输入用户名和密码
        self.input_text(elementlogin['账号'], user["username"])
        self.input_text(elementlogin['密码'], user["password"])

        # 点击登录按钮
        self.is_click(elementlogin['登录'])
        time.sleep(5)
        # 等待登录完成（使用显式等待）
        self.waitload(elementcommon['店铺'])










