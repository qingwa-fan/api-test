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



class SearchTermAnalysis(Common):
    """封装页面SearchTermAnalysis相关各个操作。使用方法：SearchTermAnalysis(drivers)"""

    @allure.step("搜索词类型切换")
    def SearchTermType(self):
        self.is_click(elementSearchTermAnalysis['顶部筛选_搜索词类型'])
        self.is_click(elementSearchTermAnalysis['顶部筛选_搜索词类型_切换选项商品定向'])

    @allure.step("总览/关联搜索里面-模糊/精确搜索，需先进入总览/关联搜索")
    def ContainExctSearcg(self,search_type='Contains',entrance='key'):
        searchType_key_mapping = {
            'Contains': (''' women'women',women';women'--women\\''','''missluck women'women',women';women'--women\\'''),
            'Exact': ('''missluck women'women',women';women'--women\\''','''missluck women'women',women';women'--women\\''')
        }
        searchType_product_mapping = {
            'Contains':  'B08NVFYFX',
            'Exact': 'B08NVFYFXQ',
        }
        if search_type=='Exact':
            if entrance=='key':
                self.is_click(elementSearchTermAnalysis['定向模糊/精确搜索类型'])
            else:
                self.is_click(elementSearchTermAnalysis['定向模糊/精确搜索类型'])
            self.is_click(elementSearchTermAnalysis['模糊/精确搜索类型_精准'])
            time.sleep(1)
        if entrance=='key':
            self.input_text(elementSearchTermAnalysis['模糊/精确搜索'],searchType_key_mapping[search_type][0])
        else:
            self.input_text(elementSearchTermAnalysis['模糊/精确搜索'],searchType_product_mapping[search_type])
        self.input_enter(elementSearchTermAnalysis['模糊/精确搜索'])
        time.sleep(1)
        if entrance == 'key':
            assert self.element_text(elementSearchTermAnalysis['总览模糊/精确搜索结果-搜索词结果'])==searchType_key_mapping[search_type][1]
        else:
            assert self.element_text(elementSearchTermAnalysis['总览模糊/精确搜索结果-搜索词结果'])==searchType_product_mapping['Exact']
        # 删除已经输入的
        self.hold_on(elementSearchTermAnalysis['模糊/精确搜索'])
        time.sleep(1)
        self.is_click(elementSearchTermAnalysis['搜索词删除'])


    @allure.step("关联搜索-搜索词搜索")
    def SearchTerm(self,entrance):
        entrance_mapping = {
            'key': ('''women\\'s swim ''', '''fleece lined leggings women'''),
            'product': ('''B0BK16S2Z''', '''waterproof trousers womens'''),
        }
        # 点击关联搜索
        self.is_click(elementSearchTermAnalysis['关联搜索'])
        self.waitload(elementSearchTermAnalysis['搜索词输入'])
        time.sleep(1)
        # 点击搜索词出现搜索词弹窗
        self.is_click(elementSearchTermAnalysis['搜索词'])
        # 搜索词搜索B08NVFYFXQ
        self.input_text(elementSearchTermAnalysis['模糊/精确搜索'],entrance_mapping[entrance][0])
        self.input_enter(elementSearchTermAnalysis['搜索词输入'])
        # 勾选搜索结果第一个
        self.is_click(elementSearchTermAnalysis['搜索词输入选择'])
        # 点击其他地方加载搜索数据
        self.is_click(elementSearchTermAnalysis['目录_关联搜索'])
        # 表格里第一个时词云图第一名
        self.input_text(elementSearchTermAnalysis['模糊/精确搜索'], entrance_mapping[entrance][1])

    @allure.step("快捷搜索-广告")
    def ChangeAds(self, AdsType='SP'):
        self.is_click(elementSearchTermAnalysis['快捷搜搜广告'])
        if AdsType=='SP':
            self.is_click(elementSearchTermAnalysis['快捷搜搜广告SP'])
        else:
            self.is_click(elementSearchTermAnalysis['快捷搜搜广告SB'])
        for i in self.find_elements(elementSearchTermAnalysis['表格第三列']):
            if AdsType == 'SP':
                assert i.text == '商品推广'
            else:
                assert i.text == '品牌推广'

    @allure.step("快捷搜索-广告位")
    def ChangeParametrize(self, AdsType='Top'):
        self.is_click(elementSearchTermAnalysis['快捷搜搜广告位'])
        ads_type_mapping = {
            'Top': '下拉框第一个',
            'Rest': '下拉框第二个',
            'Detail': '下拉框第三个',
            'HomePage': '下拉框第四个',
            'Off-Amazon': '下拉框第五个'
        }

        if AdsType in ads_type_mapping:
            self.is_click(elementSearchTermAnalysis[ads_type_mapping[AdsType]])
            time.sleep(1)
        if self.is_element_exsist(elementSearchTermAnalysis['表格第四列']):
            for i in self.find_elements(elementSearchTermAnalysis['表格第四列']):
                ads_type_search_mapping = {
                    'Top': '搜索结果顶部（首页）',
                    'Rest': '搜索结果的其余位置',
                    'Detail': '商品页面',
                    'HomePage': '亚马逊主页',
                    'Off-Amazon': '亚马逊站外'
                }
                print('---------')
                print(ads_type_search_mapping[AdsType])
                if AdsType in ads_type_search_mapping:
                    assert i.text == ads_type_search_mapping[AdsType]

    @allure.step("表格细分/汇总切换")
    def ChangeGroupedType(self):
        self.waitload(elementSearchTermAnalysis['细分汇总'])
        time.sleep(2)
        elements = self.find_elements(elementSearchTermAnalysis['细分汇总'])
        active_index = None
        # 当前类型的索引，当前的class值：active
        for index, element in enumerate(elements):
            if 'active' in element.get_attribute('class'):
                active_index = index
                break
        # 根据 active 元素的索引点击另一个元素
        if active_index is not None:
            if active_index == 0:
                elements[1].click()
            else:
                elements[0].click()


    @allure.step("快捷搜搜-定向匹配类型")
    def ChangeMatchType(self,matchtype):
        matchtype_mapping = {
            'auto_close': '下拉框第一个',
            'auto_loose': '下拉框第二个',
            'auto_substitutes': '下拉框第三个',
            'exact': '下拉框第四个',
            'broad': '下拉框第五个',
            'phrase': '下拉框第六个',
        }
        matchtype_search_mapping = {
            'auto_close': 'close-match',
            'auto_loose': 'loose-match',
            'auto_substitutes': 'substitutes',
            'exact': 'E',
            'broad': 'B',
            'phrase': 'P',
        }
        # 选择定向类型
        self.is_click(elementSearchTermAnalysis['快捷搜搜定向匹配类型'])
        self.is_click(elementSearchTermAnalysis[matchtype_mapping[matchtype]])
        time.sleep(1)
        # 选择定向
        self.is_click(elementSearchTermAnalysis['快捷搜搜定向'])
        # 自动类型选择定向值
        if 'auto' in matchtype:
            # 自动类型，只有一个选项
            assert len(self.find_elements(elementSearchTermAnalysis['搜索词输入选择']))==2
            assert self.find_elements(elementSearchTermAnalysis['搜索词输入选择'])[1].text == matchtype_search_mapping[matchtype]
        # 非自动类型选择定向值
        else:
            targetingname = self.find_elements(elementSearchTermAnalysis['搜索词输入选择'])[1].text
            if matchtype in ['exact','phrase']:
                # 勾选第一个勾选框
                self.find_elements(elementSearchTermAnalysis['搜索词输入选择'])[0].click()
                # 点击其他地方加载数据
                self.is_click(elementSearchTermAnalysis['快捷搜搜广告位'])
            elif matchtype=='broad':
                # 输入后筛选，勾选第一个框
                self.input_text(elementSearchTermAnalysis['搜索词输入'],targetingname)
                self.input_enter(elementSearchTermAnalysis['搜索词输入'])
                self.find_elements(elementSearchTermAnalysis['搜索词输入选择'])[0].click()
                # 点击其他地方加载数据
                self.is_click(elementSearchTermAnalysis['快捷搜搜广告位'])
        time.sleep(1)
        if self.is_element_exsist(elementSearchTermAnalysis['表格第四列']):
            #断言类型
            if 'auto' in matchtype:
                assert self.is_element_exsist(elementSearchTermAnalysis['表格投放类型自动'])
            else:
                elements = self.find_elements(elementSearchTermAnalysis['表格投放类型非自动'])
                # 从第二个元素开始遍历
                for i in elements[1:]:
                    assert i.text == matchtype_search_mapping[matchtype]
            # 断言定向
            for i in self.element_text(elementSearchTermAnalysis['表格投放类型定向']):
                if 'auto' in matchtype:
                    assert i.text == matchtype_search_mapping[matchtype]
                elif matchtype=='exact':
                    assert i.text == targetingname

    # @allure.step("快捷搜搜-关键字")
    # def ChangeMatchItem(self):
    #     self.input_text(elementSearchTermAnalysis['表格投放类型定向'],'hhh')








