#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import time

import allure
from common.readelement import Element
from page.webpage import WebPage
from page_object.通用 import Common


sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))

# 获取element.yaml
elementUniqueReach = Element('UniqueReach')
elementSearchTermAnalysis = Element('SearchTermAnalysis')
elementcommon = Element('common')
elementCustomerLifetimeValue = Element('CustomerLifetimeValue')



class UniqueReach(Common):
    """封装页面UniqueReach相关各个操作。使用方法：UniqueReach(drivers)"""

    @allure.step("顶部筛选-广告账户")
    def AdsAccountSearch(self, Account):
        # 点击广告账户筛选
        self.is_click(elementUniqueReach['顶部筛选-广告账户'])
        time.sleep(1)

        # 定义广告账户操作逻辑
        def select_dps_and_sa():
            self.is_click(elementUniqueReach['广告账户_DPS广告主全选'])
            time.sleep(1)
            self.is_click(elementUniqueReach['广告账户_sa广告主全选'])
            time.sleep(1)

        def select_dps():
            self.is_click(elementUniqueReach['广告账户_DPS广告主全选'])
            time.sleep(1)

        def select_sa():
            self.is_click(elementUniqueReach['广告账户_sa广告主全选'])
            time.sleep(1)

        def select_secondary(index,element=elementUniqueReach['广告账户_二级一']):
            self.find_elements(element)[index].click()
            time.sleep(1)

        # 根据 Account 的值执行不同的操作
        if isinstance(Account, tuple):
            if set(Account) == {'DE', 'UK', '9L', 'CN'}:
                select_dps_and_sa()
            elif set(Account) == {'DE', 'UK', '9L'} or set(Account) == {'DE', 'UK', 'CN'}:
                select_dps()
                if '9L' in Account:
                    select_secondary(3)
                else:
                    select_secondary(3)
            elif set(Account) == {'9L', 'CN', 'DE'} or set(Account) == {'9L', 'CN', 'UK'}:
                select_dps()
                if 'DE' in Account:
                    select_secondary(3)
                else:
                    select_secondary(3)
            elif set(Account) == {'DE', 'UK'}:
                select_dps()
            elif set(Account) == {'9L', 'CN'}:
                select_sa()
        elif isinstance(Account, str):
            if Account == 'DE' or Account == 'UK':
                self.is_click(elementUniqueReach['广告账户_DPS广告主'])
                time.sleep(1)
                if Account == 'DE':
                    select_secondary(3)
                else:
                    select_secondary(3,element=elementUniqueReach['广告账户_二级二'])
            elif Account == '9L' or Account == 'CN':
                self.is_click(elementUniqueReach['广告账户_sa'])
                time.sleep(1)
                if Account == '9L':
                    select_secondary(3)
                else:
                    select_secondary(3,element=elementUniqueReach['广告账户_二级二'])

        # 获取广告触发分析卡片值
        value = [element.text for index, element in
                 enumerate(self.find_elements(elementUniqueReach['广告触发分析卡片值'])) if index % 2 == 1]

        # 定义期望值
        expected_values = {
            'UK': ['3,636,796', '3,026,270', '83.20%', '$1.00', '$0.96'],
            'CN': ['0', '--', '--', '$0.00', '--'],
            ('9L', 'CN'): ['0', '--', '--', '$0.00', '--'],
            ('9L', 'CN', 'DE', 'UK'): ['8,974,948', '7,085,718', '78.90%', '$1.02', '$0.88']
        }

        # 断言
        if Account in expected_values:
            assert value == expected_values[Account], f"断言失败: 期望 {expected_values[Account]}，实际 {value}"
        else:
            raise ValueError(f"未知的 Account 值: {Account}")


    @allure.step("顶部筛选-广告")
    def AdsSearch(self, Account):
        # 定义广告类型选择的映射关系
        AD_TYPE_MAPPING = {
            'DPS': elementUniqueReach['顶部筛选-广告_广告类型DSP'],
            'SP': elementUniqueReach['顶部筛选-广告_广告类型SP'],
            'SB': elementUniqueReach['顶部筛选-广告_广告类型SB'],
            'SD': elementUniqueReach['顶部筛选-广告_广告类型SD']
        }

        # 定义期望值
        EXPECTED_VALUES = {
            'DPS': ['8,974,948', '7,085,718', '78.90%', '$1.02', '$0.88'],
            'SP': ['3,929,519', '1,969,334', '50.10%', '$18.35', '$0.00'],
            'SB': ['454,909', '373,227', '82.00%', '$8.25', '$0.00'],
            'SD': ['739,467', '592,998', '80.20%', '$5.41', '$0.90'],
            'Baleaf-DE_Bonus Order_Awareness_CPDPV(24/Dec)': ['5,320,174', '4,198,578', '78.90%', '$0.98', '$0.82']
        }

        # 点击广告账户筛选
        self.is_click(elementUniqueReach['顶部筛选-广告'])
        time.sleep(1)

        # 根据 Account 的值执行不同的操作
        if Account in AD_TYPE_MAPPING:
            self.is_click(AD_TYPE_MAPPING[Account])
        else:
            self.is_click(elementUniqueReach['顶部筛选-广告_广告活动'])
            time.sleep(1)
            self.input_text(elementUniqueReach['顶部筛选-广告_广告活动_搜索'], Account, if_enter=True)
            time.sleep(1)
            self.is_click(elementUniqueReach['顶部筛选-广告_广告活动_搜索选择'])
            time.sleep(1)

        # 获取广告触发分析卡片值
        value = [element.text for index, element in
                 enumerate(self.find_elements(elementUniqueReach['广告触发分析卡片值'])) if index % 2 == 1]

        # 断言
        if Account in EXPECTED_VALUES:
            assert value == EXPECTED_VALUES[Account], f"断言失败: 期望 {EXPECTED_VALUES[Account]}，实际 {value}"
        else:
            raise ValueError(f"未知的 Account 值: {Account}")


    @allure.step("广告触达模型-顶部筛选-广告-广告活动下的店铺搜索")
    def AdsTypeSearch(self, Account):
        # 定义广告活动店铺选择操作
        def select_shop(shop_type):
            self.is_click(elementUniqueReach['顶部筛选-广告_广告活动_店铺选择'])
            time.sleep(1)
            if shop_type == 'DSP':
                self.is_click(elementUniqueReach['顶部筛选-广告_广告活动_店铺选择_DSP'])
            elif shop_type == 'SA':
                self.is_click(elementUniqueReach['顶部筛选-广告_广告活动_店铺选择_SA'])
            elif shop_type == 'DE':
                self.is_click(elementUniqueReach['顶部筛选-广告_广告活动_店铺选择_DSP下级'])
                time.sleep(1)
                self.is_click(elementUniqueReach['顶部筛选-广告_广告活动_店铺选择_DSP下级_DE'])
            time.sleep(1)

        # 定义断言逻辑
        def assert_shop_conditions(shop_type):
            if shop_type == 'DSP':
                assert len(self.find_elements(
                    elementUniqueReach['顶部筛选-广告_广告活动_店铺选择_店铺'])) == 2, "DSP 店铺数量不符合预期"
            elif shop_type == 'SA':
                assert not self.is_element_exsist(
                    elementUniqueReach['顶部筛选-广告_广告活动_店铺选择_店铺']), "SA 店铺存在，但预期不存在"
            elif shop_type == 'DE':
                assert len(
                    self.find_elements(elementUniqueReach['顶部筛选-广告_广告活动_店铺选择_店铺'])) == 1, "DE 店铺数量不符合预期"
                assert self.element_text(
                    elementUniqueReach['顶部筛选-广告_广告活动_店铺选择_店铺']) == 'Baleaf_DE', "DE 店铺名称不符合预期"

        # 点击广告账户筛选
        self.is_click(elementUniqueReach['顶部筛选-广告'])
        time.sleep(1)
        self.is_click(elementUniqueReach['顶部筛选-广告_广告活动'])
        time.sleep(1)

        # 根据 Account 的值执行不同的操作
        select_shop(Account)

        # 加载数据
        self.is_click(elementUniqueReach['顶部筛选-广告_广告活动'])
        time.sleep(1)

        # 断言店铺条件
        assert_shop_conditions(Account)

    @allure.step("卡片编辑")
    def EditCard(self, EditType='add'):
        self.is_click(elementUniqueReach['广告触发分析卡片编辑'])
        # 断言下已选指标
        assert len(self.find_elements(elementUniqueReach['广告触发分析卡片编辑_已选指标']))==6
        value=[i.text for i in self.find_elements(elementUniqueReach['广告触发分析卡片编辑_已选指标'])]
        print(value)
        if EditType=='del':
            self.is_click(elementcommon['指标删除'])
            time.sleep(1)
            self.is_click(elementcommon['预览'])
        elif EditType=='add':
            self.is_click(elementcommon['指标删除'])
        card_name = [element.text for index, element in
                 enumerate(self.find_elements(elementUniqueReach['广告触发分析卡片值'])) if index % 2 == 0]
        if EditType == 'del':
            assert '广告触达人数（用户）' not in card_name










