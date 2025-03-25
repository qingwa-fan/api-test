# encoding: utf-8
# @author: Jeffrey
# @file: conftest.py
# @time: 2021/11/18 12:14
# @desc:
import time
import pytest
from appium import webdriver

driver = None
# 启动安卓系统中的计算器app
@pytest.fixture()
def start_app(android_setting):
    global driver
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4723/wd/hub',desired_capabilities=android_setting)
    return driver

# 关闭安卓系统中的计算器app
@pytest.fixture()
def close_app():
    yield driver
    time.sleep(2)
    driver.close_app()