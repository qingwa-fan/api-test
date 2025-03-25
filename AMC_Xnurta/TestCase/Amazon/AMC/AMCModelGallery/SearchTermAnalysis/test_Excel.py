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
功能：搜索词分析模型底部excel
步骤：
1、test_DataComparison 数据对比
2、test_Grouped 细分/汇总
3、test_HideShowChart 隐藏/显示图表
4、test_Screen 全屏
5、test_Export 导出
6、test_CustomizeColumns 自定义列
'''


@allure.description("搜索词分析模型底部excel")
class TestExcel:
    @allure.story('搜索词分析模型-数据对比')
    def test_DataComparison(self, drivers):
        """
        1、默认不开窍，开启后显示对比数据
        2、关闭后不显示对比数据
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        common.DataComparison()

    @allure.story('搜索词分析模型-细分/汇总')
    def test_Grouped(self, drivers):
        """
        1、默认汇总，开启细分
        2、关闭细分
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        common.DataComparison()

    @pytest.mark.parametrize('entrance', ['Overall','RelatedSearch'])
    @allure.story('搜索词分析模型-隐藏/显示图表')
    def test_HideShowChart(self, drivers,entrance):
        """
        1、默认开启，开启隐藏
        2、开启显示
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        common.HideShowChart(entrance)

    @pytest.mark.parametrize('entrance', ['Overall','RelatedSearch'])
    @allure.story('搜索词分析模型-全屏/取消全屏')
    def test_Screen(self, drivers,entrance):
        """
        1、默认非全屏，开启全屏
        2、关闭全屏
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        common.Screen(entrance)

    @pytest.mark.parametrize('entrance', ['SearchTermAnalysisOverall','SearchTermAnalysisRelatedSearch'])
    @allure.story('导出')
    def test_Export(self, drivers,entrance):
        """
        1、导出
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        common.Export(entrance)

    @pytest.mark.parametrize('entrance', ['Overall','RelatedSearch'])
    @allure.story('自定义列')
    def test_CustomizeColumns(self, drivers,entrance):
        """
        1、去勾选自定义列
        1、勾选自定义列
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        common.CustomizeColumns(entrance)




    # @allure.story('试下画板')
    # def test_tryGrouped(self, drivers):
    #     """
    #     1、默认汇总，开启细分
    #     2、关闭细分
    #     """
    #     common = SearchTermAnalysis(drivers)
    #     common.ChooseModel(name='SearchTermAnalysis')
    #     common.get_canvas()









# if __name__ == '__main__':
#     # pytest.main(["-s", '--tests-per-worker=4'])
#     pytest.main(['-s', __file__, '--workers=1', '--tests-per-worker=3'])
