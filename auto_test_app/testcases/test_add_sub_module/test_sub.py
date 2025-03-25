# encoding: utf-8
# @author: Jeffrey
# @file: test_sub.py
# @time: 2021/11/18 13:07
# @desc:

import allure
from appium.webdriver.webdriver import By

@allure.epic('安卓计算机项目')
@allure.feature('V1.0版本')
class TestSub():
    @allure.story('减法运算')
    @allure.title('[case01] 验证计算机能否正常完成减法功能')
    def test_cases01(self,start_app,close_app):
        with allure.step('1、启动安卓系统中的计算机app'):
            driver = start_app
        with allure.step('2、依次按下6、-、2、='):
            driver.find_element(By.XPATH,'//android.widget.Button[@resource-id="com.sky.jisuanji:id/btn6"]').click()
            driver.find_element(By.XPATH, '//android.widget.Button[@resource-id="com.sky.jisuanji:id/jian"]').click()
            driver.find_element(By.XPATH, '//android.widget.Button[@resource-id="com.sky.jisuanji:id/btn2"]').click()
            driver.find_element(By.XPATH, '//android.widget.Button[@resource-id="com.sky.jisuanji:id/denyu"]').click()
            actual_result = driver.find_element(By.XPATH, '//android.widget.EditText[@resource-id="com.sky.jisuanji:id/text"]').text
        with allure.step('3、验证实际结果是否正确'):
            # 断言 实际结果 == 4.0
            assert actual_result == '4.0'