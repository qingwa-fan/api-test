import os
import sys
import time

import allure
import pytest
from page_object.通用 import Common

from page_object.UniqueReach import UniqueReach
from page_object.登录 import LoginObject

from utils.logger import log

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))))

class TestLogin:
    @allure.description("登录功能测试，用户名/密码为空和错误")
    @pytest.mark.parametrize("user,passwd",[('', "123456A"),
                                            ("leo.sui@sparkxmarketing.com",''),
                                            ('', ''),
                                            ("leo.sui@sparkxmarketing.com","123456A1")])
    def test_AccountLogon(self,drivers, user, passwd):
        common = LoginObject(drivers)
        common.logintest(username=user, passwd=passwd)
        time.sleep(30)


