#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
from page_object.通用 import Common

import allure
import pytest

from page_object.CustomerLifetimeValue import CustomerLifetimeValue
from utils.logger import log
from utils.mysql import DB

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))))

'''
顾客终身价值-总览
1、test_CostRecoveryMarker 成本回收定位器
2、test_OperatingMargin  利润率
3、test_Export 导出
'''


@allure.description("顾客终身价值分析-总览")
class TestOverAll:
    @allure.story('顾客终身价值分析模型-总览-成本回收定位器')
    def test_CostRecoveryMarker(self, drivers):
        """
        1、成本回收定位器
        """
        common = CustomerLifetimeValue(drivers)
        common.ChooseModel(name='CustomerLifetimeValue')
        common.CostRecoveryMarker()

    @pytest.mark.parametrize('value', ['1','50','99'])
    @allure.story('顾客终身价值分析模型-总览-利润率')
    def test_OperatingMargin(self, drivers,value):
        """
        1、利润率
        """
        common = CustomerLifetimeValue(drivers)
        common.ChooseModel(name='CustomerLifetimeValue')
        common.OperatingMargin(value)


    @pytest.mark.parametrize('entrance', ['CostRecoveryMarkerOverall','CostRecoveryMarkerMonthlyCohort'])
    @allure.story('顾客终身价值分析模型-总览-导出')
    def test_Export(self, drivers,entrance):
        """
        1、导出
        """
        common = CustomerLifetimeValue(drivers)
        common.ChooseModel(name='CustomerLifetimeValue')
        common.Export(entrance)












# if __name__ == '__main__':
#     # pytest.main(["-s", '--tests-per-worker=4'])
#     pytest.main(['-s', __file__, '--workers=1', '--tests-per-worker=3'])
