#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
from page_object.通用 import Common

import allure
import pytest

from page_object.UniqueReach import UniqueReach
from utils.logger import log
from utils.mysql import DB

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))))

'''
功能：广告触达模型，顶部筛选
1、test_AdsAccountSearch 广告触达模型，顶部筛选-广告账户
2、test_AdsSearch 广告触达模型-顶部筛选-广告
3、广告触达模型-顶部筛选-广告-广告活动下的店铺搜索
'''


@allure.description("广告触达模型-顶部筛选")
class TestTopSearch:
    @allure.story('广告触达模型-顶部筛选-广告账户')
    @pytest.mark.parametrize('Account', ['UK','CN',('9L','CN'),('9L','CN','DE','UK')])
    def test_AdsAccountSearch(self, drivers,Account):
        """
        1、广告触达模型-顶部筛选-广告账户
        """
        common = UniqueReach(drivers)
        common.ChooseModel()
        common.AdsAccountSearch(Account)

    @allure.story('广告触达模型-顶部筛选-广告')
    @pytest.mark.parametrize('Account', ['DPS', 'SP', 'SB', 'SD','Baleaf-DE_Bonus Order_Awareness_CPDPV(24/Dec)'])
    def test_AdsSearch(self, drivers, Account):
        """
        1、广告触达模型-顶部筛选-广告
        """
        common = UniqueReach(drivers)
        common.ChooseModel()
        common.AdsSearch(Account)

    @allure.story('广告触达模型-顶部筛选-广告-广告活动下的店铺搜索')
    @pytest.mark.parametrize('Account', ['DPS', 'SA', 'DE'])
    def test_AdsTypeSearch(self, drivers, Account):
        """
        1、广告触达模型-顶部筛选-广告-广告活动下的店铺搜索
        """
        common = UniqueReach(drivers)
        common.ChooseModel()
        common.AdsTypeSearch(Account)









# if __name__ == '__main__':
#     # pytest.main(["-s", '--tests-per-worker=4'])
#     pytest.main(['-s', __file__, '--workers=1', '--tests-per-worker=3'])
