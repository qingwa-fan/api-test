#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import base64
import time
from utils.logger import log

from common.readconfig import ini
import pytest

from py.xml import html
from selenium import webdriver
from page_object.通用 import Common
from page_object.登录 import LoginObject

from common.readelement import Element
from config.conf import ConfigManager
from utils.times import timestamp
from utils.times import dt_strftime
import os
import allure
driver = None

@allure.story("登录系统")
# 每个函数或方法都会调用
@pytest.fixture(autouse=True)
def login(drivers,request):
    """登录"""
    common = Common(drivers)
    login = LoginObject(drivers)
    login.login()
    common.IntoAMC()
    common.ShopSearch()




