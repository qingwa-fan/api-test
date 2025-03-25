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
功能：广告触达分析模型创建模型
1、test_SaveAsMyModel  保存为我的模型
2、test_ComposeModelQuery  自定义模型
'''


@allure.description("广告触达分析模型创建模型")
class TestCreateModel:
    @allure.story('广告触达分析模型-保存为我的模型')
    def test_SaveAsMyModel(self, drivers):
        """
        1、保存为我的模型
        """
        common = UniqueReach(drivers)
        common.ChooseModel()
        common.SaveAsMyModel(modeltype='广告触达分析')

    @allure.story('广告触达分析模型-定义模型条件')
    def test_ComposeModelQuery(self, drivers):
        """
        1、定义模型条件
        """
        common = UniqueReach(drivers)
        common.ChooseModel()
        common.ComposeModelQuery(modeltype='广告触达分析')















# if __name__ == '__main__':
#     # pytest.main(["-s", '--tests-per-worker=4'])
#     pytest.main(['-s', __file__, '--workers=1', '--tests-per-worker=3'])
