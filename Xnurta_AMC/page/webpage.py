#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
selenium基类
本文件存放了selenium基类的封装方法
"""
import os
# import numpy as np
import random
import sys
import time
from common.readelement import Element
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# import pyperclip
# import win32api
# import win32con
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, NoSuchWindowException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config.conf import cm
from utils.logger import log
from utils.times import sleep
from selenium.webdriver.support.ui import Select

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))

USERS = [
    {"username": "leo.sui@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui2@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui3@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui4@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui5@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui6@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui7@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui8@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui9@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui10@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui11@sparkxmarketing.com", "password": "123456A"},
    {"username": "leo.sui12@sparkxmarketing.com", "password": "123456A"}
]
elementUniqueReach = Element('UniqueReach')
elementcommon = Element('common')
elementSearchTermAnalysis = Element('SearchTermAnalysis')
elementlogin = Element('登录')

class WebPage(object):
    """
    selenium基类
    鼠标、屏幕操作、元素定位、获取等
    """
    waitTime = 5
    def __init__(self, driver):
        # 设置调用的浏览器和超时时长
        # self.driver = webdriver.Chrome()
        self.driver = driver
        self.driver.implicitly_wait(20)  # 设置隐式等待时间为20秒

        self.timeout = 20
        self.wait = WebDriverWait(self.driver, self.timeout)

    def get_url(self, url):
        """打开网址并验证"""
        # 设置页面超时时间
        self.driver.set_page_load_timeout(10)
        try:
            self.driver.get(url)
        except TimeoutException:
            print('！！！！！！time out after 3 seconds when loading page！！！！！！')
            self.driver.execute_script("window.stop()")

    @staticmethod
    def element_locator(func, locator):
        """
        元素定位器
        :param func:
        :param locator: [name,value].name:元素的类型css、xpath等在conf.py中定义.value:元素的值
        :return:
        """
        name, value = locator
        return func(cm.LOCATE_MODE[name], value)

    def find_element(self, locator):
        """
        寻找单个元素
        :param locator: [name,value].name:元素的类型css、xpath等在conf.py中定义.value:元素的值
        :return:
        """
        # presence_of_element_located((By.ID,"acdid")) 显式等待
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)

    def get_attrib(self, locator, value):
        """
         获取元素属性
         :param value:
         :param locator: [name,value].name:元素的类型css、xpath等在conf.py中定义.value:元素的值
         :return:需要获取的属性的名称
         """
        log.info("获取属性")
        ele = self.find_element(locator)
        sleep(0.5)
        return ele.get_attribute(value)
        # js:'document.querySelector("#质检表_返工单号").value'
        # self.driver.execute_script(js)

    def find_elements(self, locator):
        """
         查找多个相同的元素
         :param locator: [name,value].name:元素的类型css、xpath等在conf.py中定义.value:元素的值
         :return:
         """
        return WebPage.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def find_element_drag(self, locator):
        # 滚动到目标位置
        target = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)  # 拖动到可见的元素去

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        log.info("相同元素：{}".format((locator, number)))
        return number

    def input_text(self, locator, txt, if_enter=False, clear_type=False):

        """输入(输入前先清空)"""
        sleep(1)
        ele = self.find_element(locator)
        if not clear_type:
            ele.clear()
            sleep(1)
        if clear_type:
            ele.send_keys(Keys.CONTROL, "a")  # 相当于ctrl + a快捷键全选
            # ele.send_keys(Keys.DELETE)  # 快捷键删除
        ele.send_keys(txt)
        sleep(0.5)
        if if_enter:
            ele.send_keys(Keys.RETURN)
        log.info("输入文本：{}".format(txt))

    def input_enter(self, locator, value=Keys.ENTER):
        """回车、tab等键入"""

        ele = self.find_element(locator)
        ele.send_keys(value)

    def is_click(self, locator):
        """点击"""

        self.find_element(locator).click()
        sleep(1)
        log.info("点击元素：{}".format(locator))

    def element_text(self, locator, num='single'):
        """获取当前的text"""
        if num == 'single':
            _text = self.find_element(locator).text
        else:
            _text = self.find_elements(locator)[int(num)].text
        log.info("获取文本：{}".format(_text))
        return _text

    def hold_on(self, locator):
        # 定位到要悬停的元素
        move = self.find_element(locator)
        # 对定位到的元素执行悬停操作
        ActionChains(self.driver).move_to_element(move).perform()
        sleep()
        # log.info("悬停元素：{}".format(locator))

    def screen_scoll(self):
        self.driver.execute_script('window.scrollBy(0, 300)')
        sleep(1)

    def executeJs(self, js, *target):
        """
        :param js: JS语句
        :param target:
        :return:
        """
        self.driver.execute_script(js, *target)

    @property
    def get_source(self):
        """获取页面源代码"""
        return self.driver.page_source

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)

    def focus(self):
        """滚动到底部"""
        self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    def alert_exists(self):
        """判断弹框是否出现，并返回弹框的文字"""
        alert = EC.alert_is_present()(self.driver)
        if alert:
            text = alert.text
            log.info("Alert弹窗提示为：%s" % text)
            alert.accept()
            return text
        else:
            log.info("没有Alert弹窗提示!")


    def get_title(self):
        print("Switch to window: " + self.driver.title + " successfully!")
        return self.driver.title

    def switch_tab(self, *windowTitle):
        """

        :param windowTitle: 可变参数，不输入窗口标题则定位到最后一个窗口，输入窗口标题名称则定位到该窗口window('简历填写')
        :return:
        """
        # driver当前页面的所有句柄，默认切换到最后一个
        handles = self.driver.window_handles
        if windowTitle != ():
            for s in handles:
                print(s.title)
                try:
                    self.driver.switch_to.window(s)
                    if self.driver.title == windowTitle[0]:
                        print("Switch to window: " + windowTitle[0] + " successfully!")
                        break
                    else:
                        continue
                except NoSuchWindowException:
                    print("Window: " + windowTitle[0] + " not found!")
        else:
            self.driver.switch_to.window(handles[-1])
            print("Switch to window: " + self.driver.title + " successfully!")

        # 通过Title来切换窗口

    def switchToWindowByTitle(self, windowTitle):
        """
        :param windowTitle:窗口的页面标题
        :用于进行某些操作新开页面后定位到新开页面的元素，比如候选库安排测评
        """
        currentHandle = self.driver.current_window_handle
        handles = self.driver.window_handles
        for s in handles:
            if s == currentHandle:
                continue
            else:
                try:
                    self.driver.switch_to.window(s)
                    if self.driver.title == windowTitle:
                        print("Switch to window: " + windowTitle + " successfully!")
                        break
                    else:
                        continue
                except NoSuchWindowException:
                    print("Window: " + windowTitle[0] + " not found!")
        else:
            raise ("Window: " + windowTitle + " not found!")

    def close(self):
        # driver关闭当前页面
        self.driver.close()

    def find_elements(self, args):
        """
        查找元素，找不到就抛出异常
        :param args: 要定位的元素
        :return:
        """
        way = args[0].upper()
        value = args[1]
        try:
            if way == "ID":
                return WebDriverWait(self.driver, self.waitTime).until(
                    lambda driver: driver.find_elements(by=By.ID, value=value))
            elif way == "NAME":
                return WebDriverWait(self.driver, self.waitTime).until(
                    lambda driver: driver.find_elements(by=By.NAME, value=value))
            elif way == "CLASS_NAME":
                value1 = value.split(":")
                viewList = WebDriverWait(self.driver, self.waitTime).until(
                    lambda driver: driver.find_elements(by=By.CLASS_NAME, value=value1[0]))
                return viewList[value1[1]]
            elif way == "XPATH":
                return WebDriverWait(self.driver, self.waitTime).until(
                    lambda driver: driver.find_elements(by=By.XPATH, value=value))
            elif way == "CSS_SELECTOR":
                return WebDriverWait(self.driver, self.waitTime).until(
                    lambda driver: driver.find_elements(by=By.CSS_SELECTOR, value=value))
            elif way == "PARTIAL_LINK_TEXT":
                return WebDriverWait(self.driver, self.waitTime).until(
                    lambda driver: driver.find_elements(by=By.PARTIAL_LINK_TEXT, value=value))
            elif way == "TAG_NAME":
                return WebDriverWait(self.driver, self.waitTime).until(
                    lambda driver: driver.find_elements(by=By.TAG_NAME, value=value))
            elif way == "LINK_TEXT":
                return WebDriverWait(self.driver, self.waitTime).until(
                    lambda driver: driver.find_elements(by=By.LINK_TEXT, value=value))
            else:
                return False
        except TimeoutException:
            # logger.error("元素超时未找到：" + args[1])
            raise TimeoutException(msg="元素超时未找到：" + args[1])
        except ElementNotInteractableException:
            # logger.error("元素不可见：" + args[1])
            raise ElementNotInteractableException(msg="元素不可见：" + args[1])

    def send_keyword(self, way):
        if way == 'UP':
            ActionChains(self.driver).send_keys(Keys.ARROW_UP)
        elif way == 'DOWN':
            ActionChains(self.driver).send_keys(Keys.ARROW_DOWN)
        elif way == 'RIGHT':
            ActionChains(self.driver).send_keys(Keys.ARROW_RIGHT)
        elif way == 'LEFT':
            ActionChains(self.driver).send_keys(Keys.ARROW_LEFT)
        elif way == 'ENTER':
            ActionChains(self.driver).send_keys(Keys.ENTER)
        elif way == 'F5':
            ActionChains(self.driver).send_keys(Keys.F5)
        elif way == 'BACK_SPACE':
            ActionChains(self.driver).send_keys(Keys.BACK_SPACE)

    def web_swipe(self, direction):
        """
        web页面滑动，
        :Args: UP:滑动到最底部
        :Args DOWN:滑动到最上部
        """
        driver = self.driver
        try:
            if direction == "UP":
                js = "window.scrollTo(0,document.body.scrollHeight)"
                driver.execute_script(js)
            elif direction == "DOWN":
                js = "window.scrollTo(0,0)"
                driver.execute_script(js)
        except Exception as e:
            raise e

    def drag_and_drop(self, args, args1):
        """寻找元素进行拖拽
        :Args: way:string
        :Args value:string
        """
        web_element_source = self.find_elements(args)  # 源元素
        web_element_target = self.find_elements(args1)  # 目标元素
        ActionChains(self.driver).drag_and_drop(web_element_source, web_element_target).perform()

    def frame(self, name=False, ifxpath=False):
        """
        driver定位至frame/iframe
        :param name:
        :return:
        """
        # driver定位至frame/iframe
        driver = self.driver
        if ifxpath:
            iframe = driver.find_element_by_xpath(name)
            driver.switch_to.frame(iframe)
        else:
            driver.switch_to.frame(name)
        # driver.switch_to.default_content()   切换回主窗口

    def xpath_to_frame(self, xpath):
        """
        driver定位至frame/iframe
        :param name:
        :return:
        """
        # driver定位至frame/iframe
        driver = self.driver
        iframe = driver.find_element_by_xpath(xpath)
        driver.switch_to.frame(iframe)

    #     # driver.switch_to.default_content()   切换回主窗口

    def 下拉框点击(self, ID, num):
        nums = self.driver.find_element_by_id(ID)
        Select(nums).select_by_index(num)


    def is_element_exsist(self, locator):
        '''
        判断元素是否存在,存在返回True,不存返回False
        :param locator: locator为元组类型，如("id", "yoyo")
        :return: bool值，True or False
        '''

        try:
            self.find_element(locator)
            return True
        except:
            print("元素找不到!")
            return False

    def is_frame_exsist(self, name):
        '''
        判断元素是否存在,存在返回True,不存返回False
        :param locator: locator为元组类型，如("id", "yoyo")
        :return: bool值，True or False
        '''

        try:
            driver = self.driver
            driver.switch_to.frame(name)
            return True
        except:
            print("frame找不到!")
            return False

    def quit_browser(self):
        driver = self.driver
        driver.quit()


    def waitload(self,element=elementlogin['登录']):
        """
        等待登录成功
        """
        try:
            # 等待直到某个登录成功的元素出现
            WebDriverWait(self.driver, 3).until(
                EC.presence_of_element_located((By.XPATH, element[1]))
            )
            log.info("页面加载完成")
        except TimeoutException:
            log.error("页面加载超时")
            raise

    def get_user_by_worker_id(self):
        """
        根据 worker_id 选择用户
        :return: 用户信息字典
        """
        worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")  # 格式为 "gw0", "gw1" 等
        user_index = int(worker_id.replace("gw", "")) if worker_id != "master" else 0
        # 根据 worker_id 选择用户（如果用户池不足，可以取模循环使用）
        return USERS[user_index % len(USERS)]

    def filedown(self, file_name):
        flag = 1
        zip_path = 'C:\\Users\\SparkX\\Downloads\\'
        file_names = os.listdir(zip_path)
        print(file_names)
        # 打印所有文件名
        for name in file_names:
            if file_name in name:
                flag = 0
        return flag

    def delfile(self):
        dir = 'C:\\Users\\SparkX\\Downloads\\'
        for root, dirs, files in os.walk(dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))

    def model_name(self,prefix='autotestmyModel', num_digits=6):
        """
        生成一个以指定前缀开头，后接指定数量随机数字的字符串。

        :param prefix: 字符串前缀（例如 "autotestmyModel"）
        :param num_digits: 随机数字的数量（默认为 6）
        :return: 生成的字符串
        """
        # 生成指定数量的随机数字
        random_digits = ''.join(random.choices('0123456789', k=num_digits))

        # 拼接前缀和随机数字
        return f"{prefix}{random_digits}"

    # # var ctx = canvas.getContext('2d');
    # def get_canvas(self):
    #     # 找到 Canvas 元素
    #     canvas = self.find_element(elementSearchTermAnalysis['画板'])
    #     # 将像素数据转换为图像
    #     width = canvas.size['width']
    #     height = canvas.size['height']
    #     # 获取 Canvas 的像素数据
    #     image_data = self.driver.execute_script("""
    #         var canvas = arguments[0];
    #         var ctx = canvas.getContext('2d');
    #         return ctx.getImageData(0, 0, canvas.width, canvas.height).data;
    #     """, canvas)
    #
    #
    #     image_array = np.array(image_data, dtype=np.uint8).reshape((height, width, 4))  # RGBA 数据
    #     image_rgb = cv2.cvtColor(image_array, cv2.COLOR_RGBA2RGB)  # 转换为 RGB 格式
    #
    #     # 使用 OpenCV 检测圆形
    #     gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)  # 转换为灰度图
    #     gray = cv2.medianBlur(gray, 5)  # 中值滤波，去除噪声
    #
    #     # 霍夫圆变换检测圆形
    #     circles = cv2.HoughCircles(
    #         gray,
    #         cv2.HOUGH_GRADIENT,
    #         dp=1,  # 分辨率比例
    #         minDist=20,  # 圆之间的最小距离
    #         param1=50,  # Canny 边缘检测的高阈值
    #         param2=30,  # 圆心检测阈值
    #         minRadius=10,  # 最小半径
    #         maxRadius=100  # 最大半径
    #     )
    #
    #     # 绘制检测到的圆形
    #     if circles is not None:
    #         circles = np.uint16(np.around(circles))
    #         for i in circles[0, :]:
    #             # 绘制圆形
    #             cv2.circle(image_rgb, (i[0], i[1]), i[2], (0, 255, 0), 2)  # 画圆
    #             cv2.circle(image_rgb, (i[0], i[1]), 2, (0, 0, 255), 3)  # 画圆心
    #
    #         # 保存检测结果
    #         cv2.imwrite("detected_circles.png", image_rgb)
    #
    #         # 输出圆形个数
    #         print(f"检测到的圆形个数: {len(circles[0])}")
    #     else:
    #         print("未检测到圆形")


