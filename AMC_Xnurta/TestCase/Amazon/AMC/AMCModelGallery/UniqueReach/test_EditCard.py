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
功能：广告触达模型，卡片编辑
1、
'''


@allure.description("广告触达模型，卡片编辑")
class TestTopSearch:
    @allure.story('广告触达模型，卡片编辑')
    # @pytest.mark.parametrize('EditType', ['add','del',‘modify’,'change])
    @pytest.mark.parametrize('EditType', ['add'])
    def test_EditCard(self, drivers,EditType):
        """
        1、广告触达模型-顶部筛选-广告账户
        """
        common = UniqueReach(drivers)
        common.ChooseModel()
        common.EditCard(EditType)











# if __name__ == '__main__':
#     # pytest.main(["-s", '--tests-per-worker=4'])
#     pytest.main(['-s', __file__, '--workers=1', '--tests-per-worker=3'])
