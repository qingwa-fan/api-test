#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import time
from os import listdir
import zipfile
import pytest
from selenium.webdriver import ActionChains
import allure
from datetime import datetime, timedelta

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver

from common.readconfig import ini
from page.webpage import WebPage
from utils.logger import log

from common.readelement import Element
from utils.times import timestamp
from utils.times import dt_strftime
from config.conf import cm

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))

# 获取element.yaml
elementUniqueReach = Element('UniqueReach')
elementcommon = Element('common')
elementSearchTermAnalysis = Element('SearchTermAnalysis')
elementCustomerLifetimeValue = Element('CustomerLifetimeValue')



class Common(WebPage):
    """封装页面各个操作。使用方法：Element(drivers)."""
    waitTime = 5

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    @allure.step("搜索店铺")
    def ShopSearch(self,name='sparkxeubaleafeu'):
        log.info('搜索进入店铺：'+name)
        with allure.step("搜索进入店铺：" + name):
            time.sleep(3)
            self.find_elements(elementcommon['店铺'])[-1].click()
            time.sleep(1)
            self.find_elements(elementcommon['店铺快速搜索'])[-1].send_keys(name)
            time.sleep(5)
            self.is_click(elementcommon['选择店铺快速搜索数据'])
            time.sleep(1)

    @allure.step("进入AMC模型库")
    def IntoAMC(self):
        log.info('进入AMC模型库')
        with allure.step("进入AMC模型库,点击AMC数据工作室-AMC模型库"):
            self.is_click(elementcommon['AMC数据工作室'])
            self.is_click(elementcommon['AMC模型库'])
            time.sleep(8)

    @allure.step("选择模型")
    def ChooseModel(self, name='UniqueReach'):
        model_mapping = {
            'UniqueReach': {
                'element': elementcommon['AMC模型'],
                'index': 0
            },
            'SearchTermAnalysis': {
                'element': elementcommon['AMC模型二'],
                'index': 2
            },
            'CustomerLifetimeValue': {
                'element': elementcommon['AMC模型'],
                'index': 6
            },
        }

        # 获取模型对应的操作
        model_action = model_mapping.get(name)
        if model_action:
            # 找到元素并点击
            self.find_elements(model_action['element'])[model_action['index']].click()
            time.sleep(3)
        else:
            raise ValueError(f"未知的模型名称: {name}")


    @allure.step("我的模型列表字段获取")
    def AMCListValue(self, row=1):
        value = []
        full_xpath3 = elementcommon['我的AMC模型列表值'][1] + 'tr[' + str(row) + ']/td'
        m_element = (elementcommon['我的AMC模型列表值'][0], full_xpath3)
        for i in self.find_elements(m_element):
            value.append(i.text)
        return value

    @allure.step("我的模型列表操作")
    def AMCListOperate(self, operate='cancel', row=1):
        """
        在 AMC 模型列表中对指定行执行操作。

        :param operate: 操作类型，支持 'cancle', 'concern', 'delete'
        :param row: 行号（从 1 开始）
        """
        # 定义操作类型与 XPath 后缀的映射
        operate_xpath_mapping = {
            'cancel': 'tr[{row}]/td[9]/div/div/span[1]',
            'concern': 'tr[{row}]/td[9]/div/div/button',
            'delete': 'tr[{row}]/td[9]/div/div/span[2]'
        }

        # 获取基础 XPath
        base_xpath = elementcommon['我的AMC模型列表值'][1]
        xpath_suffix = operate_xpath_mapping.get(operate, 'tr[{row}]/td[9]/div/div/span[2]')

        # 拼接完整 XPath
        full_xpath = base_xpath + xpath_suffix.format(row=row)
        m_element = (elementcommon['我的AMC模型列表值'][0], full_xpath)

        # 执行点击操作
        self.is_click(m_element)
        time.sleep(1)
        if operate == 'delete':
            self.is_click(elementcommon['我的AMC模型列表操作取消_确定'])
            time.sleep(1)

    @allure.step("数据对比")
    def DataComparison(self):
        # 默认关闭
        assert not self.is_element_exsist(elementcommon['数据对比状态断言'])
        assert not self.is_element_exsist(elementcommon['数据对比状态断言数据断言'])
        self.is_click(elementcommon['数据对比'])
        time.sleep(1)
        # 存在数据对比数据
        assert self.is_element_exsist(elementcommon['数据对比状态断言数据断言'])
        #关闭数据对比后，不显示对比数据
        self.is_click(elementcommon['数据对比'])
        assert not self.is_element_exsist(elementcommon['数据对比状态断言数据断言'])

    @allure.step("细分/汇总")
    def Grouped(self):
        assert not self.is_element_exsist(elementSearchTermAnalysis['投放类型'])
        self.ChangeGroupedType()
        assert self.is_element_exsist(elementSearchTermAnalysis['投放类型'])

    @allure.step("隐藏/显示图表")
    def HideShowChart(self,entrance='Overall'):
        if entrance=='RelatedSearch':
            self.is_click(elementSearchTermAnalysis['关联搜索'])
            time.sleep(1)
        # 看下当前是不是显示图表，如果是隐藏就点击显示
        if self.is_element_exsist(elementcommon['显示图表']):
            self.is_click(elementcommon['显示图表'])
        self.is_click(elementcommon['隐藏图表'])
        time.sleep(1)
        self.is_click(elementcommon['显示图表'])

    @allure.step("全屏/关闭全屏")
    def Screen(self,entrance='Overall'):
        if entrance=='RelatedSearch':
            self.is_click(elementSearchTermAnalysis['关联搜索'])
            time.sleep(1)
        # 看下当前是不是非全屏，如果不是点击推出全屏
        if self.is_element_exsist(elementcommon['非全屏断言']):
            self.is_click(elementcommon['全屏'])
        # 全屏
        self.is_click(elementcommon['全屏'])
        assert self.is_element_exsist(elementcommon['非全屏断言'])
        # 关闭全屏
        self.is_click(elementcommon['全屏'])
        assert not self.is_element_exsist(elementcommon['非全屏断言'])

    @allure.step("导出")
    def Export(self,entrance):
        # 定义文件名称和关联元素的映射
        FILE_NAME_MAPPING = {
            'SearchTermAnalysisOverall': ('Search_Term_Analysis_sparkxeubaleafeu_', None),
            'SearchTermAnalysisRelatedSearch': (
            'Search_Term_Correlation_sparkxeubaleafeu_', elementSearchTermAnalysis['关联搜索']),
            'CostRecoveryMarkerOverall': ('customer_lifetime_value_trend__', None),
            'CostRecoveryMarkerMonthlyCohort': ('Customer_Lifetime_Value__', elementCustomerLifetimeValue['月度细分']),
        }

        # 获取文件名称和关联元素
        file_name, change_element = FILE_NAME_MAPPING.get(entrance, ('', None))

        # 如果未找到对应的入口，直接返回
        if not file_name:
            raise ValueError(f"Invalid entrance: {entrance}")

        # 如果需要切换元素，则点击切换
        if change_element:
            self.is_click(change_element)
            time.sleep(1)

        # 点击导出按钮
        self.is_click(elementcommon['导出'])
        time.sleep(10)

        # 检查文件是否下载成功
        assert self.filedown(file_name) == 0, "文件下载失败"

        # 删除文件
        self.delfile()


    @allure.step("自定义列")
    def CustomizeColumns(self,entrance='Overall'):
        if entrance=='RelatedSearch':
            self.is_click(elementSearchTermAnalysis['关联搜索'])
            time.sleep(1)
        self.is_click(elementcommon['自定义列'])
        time.sleep(1)
        # 去勾选第一个已选的指标
        columnname=self.element_text(elementcommon['自定义参数已勾选指标名'])
        # 获取去勾选指标的下标，便于恢复
        elements = []
        for i in self.find_elements(elementcommon['自定义参数指标名']):
            elements.append(i.text)
        num = elements.index(columnname)
        self.find_elements(elementcommon['自定义参数指标已选去勾选'])[0].click()
        self.find_elements(elementcommon['确定'])[-1].click()
        # 表格指标中不包含去勾选的
        for i in self.find_elements(elementSearchTermAnalysis['表格指标名']):
            assert columnname != i.text
        self.is_click(elementcommon['自定义列'])
        self.find_elements(elementcommon['自定义指标勾选'])[num].click()
        self.find_elements(elementcommon['确定'])[-1].click()
        time.sleep(1)
        # 表格指标中不包含去勾选的
        columns=[]
        for i in self.find_elements(elementSearchTermAnalysis['表格指标名']):
            columns.append(i.text)
        assert columnname in columns


    def SaveAsMyModel(self,modeltype='搜索词分析'):
        if modeltype=='搜索词分析':
            self.is_click(elementcommon['时间范围'])
        elif modeltype=='顾客终身价值分析':
            self.is_click(elementcommon['时间范围二'])
        # mon=self.element_text(elementcommon['时间范围当前月份'])
        # year=self.element_text(elementcommon['时间范围当前年'])
        self.is_click(elementcommon['保存为我的模型'])
        modelname = self.model_name()
        if modeltype=='广告触达分析':
            self.input_text(elementcommon['保存为我的模型_模型名称二'],modelname)
            time.sleep(1)
            self.is_click(elementcommon['保存为我的模型_确定二'])
        else:
            self.input_text(elementcommon['保存为我的模型_模型名称'],modelname)
            time.sleep(1)
            self.is_click(elementcommon['保存为我的模型_确定'])
        time.sleep(5)
        self.switch_tab()
        value=self.AMCListValue()
        #灯也断言下
        assert value[0]=='预置\n已完成'
        assert value[1]==modelname
        assert value[2]==modeltype
        #模型进入详情也看下配置
        self.AMCListOperate(operate='delete')

    def ComposeModelQuery(self,modeltype='搜索词分析'):
        if modeltype == '搜索词分析':
            self.is_click(elementcommon['时间范围'])
        elif modeltype == '顾客终身价值分析':
            self.is_click(elementcommon['时间范围二'])
        # mon=self.element_text(elementcommon['时间范围当前月份'])
        # year=self.element_text(elementcommon['时间范围当前年'])
        # 点击定义模型条件
        self.is_click(elementcommon['定义模型条件'])
        modelname = self.model_name()
        #输入模型名称
        self.input_text(elementcommon['定义模型条件模型名称'],modelname)
        time.sleep(1)
        #点击另存为新模板
        self.is_click(elementcommon['定义模型条件另存为新模型'])
        time.sleep(1)
        #时间范围做了校验180-390
        if modeltype == '顾客终身价值分析':
            assert '选择时间不得少于180天，不得超过390' in self.element_text(elementCustomerLifetimeValue['自定义模型_时间范围提示'])
            time.sleep(1)
            # 获取当前时间
            current_time = datetime.now()
            # 计算180天前的时间
            time_before_180_days = current_time - timedelta(days=180)
            # 计算179天前的时间
            time_before_179_days = current_time - timedelta(days=179)
            # 计算391天前的时间
            time_before_391_days = current_time - timedelta(days=391)
            # 计算390天前的时间
            time_before_391_days = current_time - timedelta(days=390)
            # 格式化时间
            time_before_180_days_str = time_before_180_days.strftime('%Y-%m-%d')
            time_before_179_days_str = time_before_179_days.strftime('%Y-%m-%d')
            time_before_391_days_str = time_before_391_days.strftime('%Y-%m-%d')
            self.input_text(elementCustomerLifetimeValue['自定义模型_时间范围_开始时间'],txt=time_before_179_days_str,clear_type=True, if_enter=True)
            self.is_click(elementcommon['定义模型条件另存为新模型'])
            assert '选择时间不得少于180天，不得超过390' in self.element_text(elementCustomerLifetimeValue['自定义模型_时间范围提示'])

            self.input_text(elementCustomerLifetimeValue['自定义模型_时间范围_开始时间'], txt=time_before_391_days_str,
                            clear_type=True, if_enter=True)
            self.is_click(elementcommon['定义模型条件另存为新模型'])
            #选不到所有不提示
            self.is_click(elementcommon['定义模型条件另存为新模型_取消'])

            self.input_text(elementCustomerLifetimeValue['自定义模型_时间范围_开始时间'], txt=time_before_180_days_str,
                            clear_type=True, if_enter=True)
            self.is_click(elementcommon['定义模型条件另存为新模型'])
        # 点击另存为新模板
        self.is_click(elementcommon['定义模型条件另存为新模型_确定'])
        time.sleep(10)
        self.switch_tab()
        value=self.AMCListValue()
        #灯也断言下
        assert value[0]=='即刻\n待查询'
        assert value[1]==modelname
        assert value[2]==modeltype
        #模型进入详情也看下配置
        self.AMCListOperate(operate='delete')







if __name__ == '__main__':
    AMCListValue()






