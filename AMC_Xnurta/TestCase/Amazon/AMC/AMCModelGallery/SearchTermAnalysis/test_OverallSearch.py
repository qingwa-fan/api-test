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
功能：搜索词饭呢西模型快捷搜索
步骤：
1、test_TestSearchAds 总览-快捷搜索-广告
2、test_TestSearchPlacement 总览-快捷搜索-广告位
3、test_TestSearchTarget 总览-快捷搜索-定向匹配类型/定向
4、test_TestSearchTarget 总览/关联搜索-快捷搜索-搜索关键字,在test_TopSearch实现
'''


@allure.description("搜索词分析模型-总览-快捷搜索")
class TestFastSearch:
    @allure.story('搜索词分析模型-总览-快捷搜索-广告切换不同类型')
    @pytest.mark.parametrize('ads_type', ['SP','SB'])
    def test_TestSearchAds(self, drivers,ads_type):
        """
        1、总览-快捷搜索-广告切换不同类型
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        common.ChangeAds(AdsType=ads_type)

    @allure.story('搜索词分析模型-总览-快捷搜索-广告位切换不同位置')
    @pytest.mark.parametrize('placement_type', ['Top', 'Rest', 'Detail', 'HomePage', 'Off-Amazon'])
    def test_TestSearchPlacement(self, drivers, placement_type):
        """
        1、总览-快捷搜索-广告位切换不同位置
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        common.ChangeParametrize(AdsType=placement_type)

    @allure.story('搜索词分析模型-总览-快捷搜索-定向匹配类型/定向Targeting')
    #搜索词为定向的情况也要覆盖下
    # @pytest.mark.parametrize('match_type', ['auto_close', 'auto_loose', 'auto_substitutes', 'exact', 'broad', 'phrase'])
    @pytest.mark.parametrize('match_type', ['auto_substitutes'])
    def test_TestSearchTarget(self, drivers, match_type):
        """
        1、总览-快捷搜索-定向类型/定向切换不同
        """
        common = SearchTermAnalysis(drivers)
        common.ChooseModel(name='SearchTermAnalysis')
        # 切换细分/汇总类型
        common.ChangeGroupedType()
        common.ChangeMatchType(match_type)
