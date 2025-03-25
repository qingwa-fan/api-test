#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
from page_object.通用 import Common

import allure
import pytest

from page_object.SearchTermAnalysis import SearchTermAnalysis
from utils.logger import log
from utils.mysql import DB

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))))

'''
功能：搜索词分析模型，顶部筛选-搜索词类型-定向
1、test_TestSearchItemTypeProduct 顶部筛选-搜索词类型-定向
2、test_TestSearchIermTypeKey 顶部筛选-搜索词类型-关键词
'''


@allure.description("搜索词分析模型-顶部筛选-搜索词类型")
class TestTopSearch:
    @allure.story('顶搜索词分析模型-部筛选-搜索词类型-定向')
    @pytest.mark.parametrize('search_type', ['Contains','Exact'])
    def test_TestSearchItemTypeProduct(self, drivers,search_type):
        """
        1、搜索类型切换定向
        2、总览快捷搜搜
        3、切换关联搜搜，搜索词搜索定向
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        #切换搜索词类型
        common.SearchTermType()
        #总览模糊搜索
        common.ContainExctSearcg(search_type,entrance='product')
        # 关联搜索模糊搜索
        common.SearchTerm(entrance='product')

    @pytest.mark.parametrize('search_type', ['Contains','Exact'])
    @allure.story('搜索词分析模型-顶部筛选-搜索词类型-关键词')
    def test_TestSearchIermTypeKey(self, drivers,search_type):
        """
        1、总览快捷搜搜
        2、切换关联搜搜，搜索词搜索关键词
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        # 精准搜索
        common.ContainExctSearcg(search_type,entrance='key')
        common.SearchTerm(entrance='key')













# if __name__ == '__main__':
#     # pytest.main(["-s", '--tests-per-worker=4'])
#     pytest.main(['-s', __file__, '--workers=1', '--tests-per-worker=3'])
