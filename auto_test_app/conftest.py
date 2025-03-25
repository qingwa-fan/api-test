# encoding: utf-8
# @author: Jeffrey
# @file: conftest.py
# @time: 2021/11/18 12:14
# @desc:
import pytest

# 配置app的各种连接信息
@pytest.fixture(scope='session')
def android_setting():
    des = {
        'automationName': 'appium',
        'platformName': 'Android',
        'platformVersion': '6.0.1',  # 填写android虚拟机/真机的系统版本号
        'deviceName': 'MuMu',  # 填写安卓虚拟机/真机的设备名称
        'appPackage': 'com.sky.jisuanji',  # 填写被测app包名
        'appActivity': '.JisuanjizixieActivity',  # 填写被测app的入口
        'udid': '127.0.0.1:7555',  # 填写通过命令行 adb devices 查看到的udid
        'noReset': True,  # 是否重置APP
        'noSign': True,  # 是否不签名
        'unicodeKeyboard': True,  # 是否支持中文输入
        'resetKeyboard': True,  # 是否支持重置键盘
        'newCommandTimeout': 30  # 30秒没发送新命令就断开连接
    }
    return des