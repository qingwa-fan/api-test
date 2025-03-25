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



class CustomerLifetimeValue(Common):
    """封装页面CustomerLifetimeValue相关各个操作。使用方法：CustomerLifetimeValue(drivers)"""

    @allure.step("成本回收定位器")
    def CostRecoveryMarker(self,entrance='overall'):
        if entrance!='overall':
            self.is_click(elementCustomerLifetimeValue['月度细分'])
            time.sleep(1)
            # 数据类型默认开启
            assert len(self.find_elements(elementCustomerLifetimeValue['成本回收定位器断言'])) == 1
        else:
            # 检查元素是否存在，若不存在则继续
            assert not self.is_element_exsist(elementCustomerLifetimeValue['成本回收定位器断言'])
        # 等待并获取提示信息
        self.hold_on(elementCustomerLifetimeValue['成本回收定位器提示'])
        assert '成本回收定位器主要用于标记某个时间段内的用户群体达到成本回收的时间点。您还可以输入预期商品利润率，更精确地计算出广告实际收益以及成本回收的时间点。' in self.element_text(
            elementCustomerLifetimeValue['成本回收定位器提示内容'])
        # 获取总览卡片的值并验证
        if entrance != 'overall':
            # 获客成本
            overview_values = [i.text for i in self.find_elements(elementCustomerLifetimeValue['月度卡片值'])]
            # 除获客成本，其他的值
            overview_value = self.find_elements(elementCustomerLifetimeValue['总览卡片值'])[0].text
            overview_values.insert(0, overview_value)
        else:
            overview_values = [i.text for i in self.find_elements(elementCustomerLifetimeValue['总览卡片值'])]
        expected_values = ['5.77', '7.19%', '184,177', '0', '1', '0']
        assert overview_values == expected_values, f"总览卡片值不匹配，预期: {expected_values}, 实际: {overview_values}"
        # 获取总览卡片的名称并验证
        if entrance != 'overall':
            # 获客成本
            overview_names = [i.text for i in self.find_elements(elementCustomerLifetimeValue['月度卡片名'])]
            # 除获客成本，其他的值
            overview_name = self.find_elements(elementCustomerLifetimeValue['总览卡片名'])[0].text
            overview_names[0]=overview_name
        else:
            overview_names = [i.text for i in self.find_elements(elementCustomerLifetimeValue['总览卡片名'])]
        expected_names = ['获客成本', '复购率', '购买人数（用户）', '顾客终身价值', '销售额', 'ROAS']
        assert overview_names == expected_names, f"总览卡片名称不匹配，预期: {expected_names}, 实际: {overview_names}"
        # 获取成本回收定位器开启内容并验证
        if entrance != 'overall':
            cost_recovery_value = self.find_elements(elementCustomerLifetimeValue['成本回收定位器开启内容二'])[0].text
            cost_recovery_values = [i.text for i in
                                    self.find_elements(elementCustomerLifetimeValue['月度成本回收定位器开启内容二'])]
            cost_recovery_values.insert(0, cost_recovery_value)
        else:
            cost_recovery_values = [i.text for i in
                                self.find_elements(elementCustomerLifetimeValue['成本回收定位器开启内容'])]
        expected_cost_recovery_values = ['', '', '', '', '', '']
        assert cost_recovery_values == expected_cost_recovery_values, f"成本回收定位器开启内容不匹配，预期: {expected_cost_recovery_values}, 实际: {cost_recovery_values}"
        # 点击成本回收定位器并等待
        self.is_click(elementCustomerLifetimeValue['成本回收定位器'])
        time.sleep(2)
        if entrance != 'overall':
            cost_recovery_values_after_click = [i.text for i in
                                    self.find_elements(elementCustomerLifetimeValue['月度卡片值'])]
            expected_cost_recovery_values_after_click = ['7.19%', '184,177', '0', '1', '0']
        else:
            cost_recovery_values_after_click = [i.text for i in
                                                self.find_elements(
                                                    elementCustomerLifetimeValue['成本回收定位器开启内容'])]


            expected_cost_recovery_values_after_click = ['', '', '', '0', '1', '0']
        assert cost_recovery_values_after_click == expected_cost_recovery_values_after_click, f"点击后成本回收定位器开启内容不匹配，预期: {expected_cost_recovery_values_after_click}, 实际: {cost_recovery_values_after_click}"

    @allure.step("利润率")
    def OperatingMargin(self,value,entrance='overall'):
        if entrance!='overall':
            self.is_click(elementCustomerLifetimeValue['月度细分'])
            time.sleep(1)
        assert self.is_element_exsist(elementCustomerLifetimeValue['利润率断言'])
        self.is_click(elementCustomerLifetimeValue['成本回收定位器'])
        time.sleep(2)
        self.input_text(elementCustomerLifetimeValue['成本回收定位器值'],value,if_enter=True, clear_type=True)
        # 销售额
        if entrance!='overall':
            value1 = self.find_elements(elementCustomerLifetimeValue['总览卡片值'])[4].text
            value2 = self.find_elements(elementCustomerLifetimeValue['月度卡片值'])[3].text
        else:
            value1=self.find_elements(elementCustomerLifetimeValue['成本回收定位器开启内容'])[4].text
            value2=self.find_elements(elementCustomerLifetimeValue['总览卡片值'])[4].text
        assert value2=='1'
        assert float(value1)==float(value) / 100 * float(value2)

        if entrance != 'overall':
            overview_names = [i.text for i in self.find_elements(elementCustomerLifetimeValue['月度成本回收定位器开启内容二'])]
        else:
            overview_names = [i.text for i in self.find_elements(elementCustomerLifetimeValue['成本回收定位器开启内容二'])]
        expected_name = 'OM: '+value+'%'
        expected_names=['', '', '', expected_name, expected_name, expected_name]
        assert overview_names == overview_names, f"总览卡片名称不匹配，预期: {expected_names}, 实际: {overview_names}"
        # 获取成本回收定位器开启内容并验证

    def Accumulative(self,card='RPR'):
        accumulative_values = []
        no_accumulative_values = []
        self.is_click(elementCustomerLifetimeValue['月度细分'])
        mapping={
            'RPR':0,
            'Purchase_UV': 1,
        }
        self.find_elements(elementCustomerLifetimeValue['月度卡片'])[mapping[card]].click()
        time.sleep(1)

        # 遍历每行,获取累计时参数
        num = len(self.find_elements(elementCustomerLifetimeValue['月度细分表格行']))
        for i in range(0, num - 1):
            element = elementCustomerLifetimeValue['月度细分表格行'][1] + '[' + str(i + 2) + ']/div[2]/div'
            m_element = (elementcommon['我的AMC模型列表值'][0], element)
            # 从第三个首次购买当月，才开始累计计算
            value = [j.text for j in self.find_elements(m_element)]
            accumulative_values.append(value)
        if card=='RPR':
            expect_accumulative_values=[['3.76', '0%', '4.61%', '5.67%', '5.67%', '5.67%', '5.67%', '5.67%', '5.67%', '5.67%', '5.67%', '5.67%', '8.47%', '8.47%'], ['3.48', '0%', '3.89%', '5.4%', '5.4%', '5.4%', '5.4%', '5.4%', '5.4%', '5.4%', '5.4%', '5.4%', '5.4%'], ['4.07', '0%', '3.94%', '4.73%', '4.73%', '4.73%', '4.73%', '4.73%', '4.73%', '4.73%', '4.73%', '4.73%'], ['4.72', '0%', '3.47%', '5.37%', '5.37%', '6.5%', '6.5%', '6.5%', '6.5%', '6.5%', '6.5%'], ['5.03', '0%', '3.5%', '5.71%', '5.71%', '5.71%', '5.71%', '5.71%', '5.71%', '5.71%'], ['4.98', '0%', '4.35%', '4.42%', '4.42%', '4.42%', '4.42%', '4.42%', '4.42%'], ['6.4', '0%', '3.26%', '6.16%', '6.16%', '6.16%', '6.16%', '6.16%'], ['6.46', '0%', '4.49%', '4.49%', '4.49%', '4.49%', '4.49%'], ['7.17', '0%', '4.33%', '4.33%', '4.33%', '4.33%'], ['8.04', '0%', '4.04%', '5.36%', '5.36%'], ['6.46', '0%', '2.97%', '4.17%'], ['6.08', '0%', '3.11%'], ['5.77', '0%', '3.78%', '5.07%', '5.19%', '5.28%', '5.41%', '5.56%', '5.38%', '5.67%', '5.65%', '5.28%', '7.25%', '8.47%']]
        else:
            expect_accumulative_values =[['3.76', '11,992', '553', '680', '680', '680', '680', '680', '680', '680', '680', '680', '1,016', '1,016'], ['3.48', '7,890', '307', '426', '426', '426', '426', '426', '426', '426', '426', '426', '426'], ['4.07', '10,293', '406', '487', '487', '487', '487', '487', '487', '487', '487', '487'], ['4.72', '13,098', '455', '704', '704', '851', '851', '851', '851', '851', '851'], ['5.03', '17,114', '599', '978', '978', '978', '978', '978', '978', '978'], ['4.98', '17,661', '769', '780', '780', '780', '780', '780', '780'], ['6.4', '23,716', '772', '1,460', '1,460', '1,460', '1,460', '1,460'], ['6.46', '17,597', '790', '790', '790', '790', '790'], ['7.17', '16,311', '706', '706', '706', '706'], ['8.04', '14,091', '569', '755', '755'], ['6.46', '19,775', '588', '824'], ['6.08', '14,639', '456'], ['5.77', '7,674.04', '580.83', '780.91', '776.6', '795.33', '806.5', '808.86', '700.33', '684.4', '611', '531', '721', '1,016']]
        assert accumulative_values==expect_accumulative_values

        # 关闭数据累计
        self.is_click(elementCustomerLifetimeValue['成本回收定位器断言'])

        # 遍历每行,获取非累计时参数
        num=len(self.find_elements(elementCustomerLifetimeValue['月度细分表格行']))
        for i in range(0,num-1):
            element = elementCustomerLifetimeValue['月度细分表格行'][1]+'['+str(i+2)+']/div[2]/div'
            m_element = (elementcommon['我的AMC模型列表值'][0], element)
            value = [j.text for j in self.find_elements(m_element)]
            no_accumulative_values.append(value)
        if card == 'RPR':
            expect_accumulative_values=[['3.76', '0%', '4.61%', '1.21%', '0%', '0%', '0%', '0%', '0%', '0%', '0%', '0%', '0.89%', '0%'], ['3.48', '0%', '3.87%', '1.5%', '0%', '0%', '0%', '0%', '0%', '0%', '0%', '0%', '0%'], ['4.07', '0%', '3.92%', '1.3%', '0%', '0%', '0%', '0%', '0%', '0%', '0%', '0%'], ['4.72', '0%', '3.45%', '1.83%', '0%', '0.79%', '0%', '0%', '0%', '0%', '0%'], ['5.03', '0%', '3.48%', '1.5%', '0%', '0%', '0%', '0%', '0%', '0%'], ['4.98', '0%', '4.34%', '1.42%', '0%', '0%', '0%', '0%', '0%'], ['6.4', '0%', '3.23%', '1.55%', '0%', '0%', '0%', '0%'], ['6.46', '0%', '4.48%', '0%', '0%', '0%', '0%'], ['7.17', '0%', '4.32%', '0%', '0%', '0%'], ['8.04', '0%', '4.04%', '1.78%', '0%'], ['6.46', '0%', '2.97%', '1.42%'], ['6.08', '0%', '3.11%'], ['5.77', '0%', '3.64%', '1.19%', '0%', '0.08%', '0%', '0%', '0%', '0%', '0%', '0%', '0.54%', '0%']]
        else:
            expect_accumulative_values =[['3.76', '11,992', '553', '145', '0', '0', '0', '0', '0', '0', '0', '0', '107', '0'], ['3.48', '7,890', '305', '118', '0', '0', '0', '0', '0', '0', '0', '0', '0'], ['4.07', '10,293', '404', '134', '0', '0', '0', '0', '0', '0', '0', '0'], ['4.72', '13,098', '452', '240', '0', '104', '0', '0', '0', '0', '0'], ['5.03', '17,114', '596', '257', '0', '0', '0', '0', '0', '0'], ['4.98', '17,661', '767', '250', '0', '0', '0', '0', '0'], ['6.4', '23,716', '765', '368', '0', '0', '0', '0'], ['6.46', '17,597', '789', '0', '0', '0', '0'], ['7.17', '16,311', '705', '0', '0', '0'], ['8.04', '14,091', '569', '251', '0'], ['6.46', '19,775', '588', '281'], ['6.08', '14,639', '456'], ['5.77', '7,674.04', '579.08', '227.11', '0', '104', '0', '0', '0', '0', '0', '0', '107', '0']]
        assert no_accumulative_values==expect_accumulative_values






