import os
import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from string import Template
from common.log import Logger
from common.handle_black import *

"""
BasePage 用于存放所有页面类的公共方法
"""
logging = Logger(__name__).get_logger()
class BasePage:

    #BasePage中的构造方法，通过其他页面类继承，同样应用到继承的页面类中
    def __init__(self, driver=None):
        if driver is None:
            # 创建一个driver对象
            driver_path = r"C:\Users\37210\Desktop\测开班_16\WebUiTestFrame\driver_version\chromedriver.exe"
            self.driver = webdriver.Chrome(executable_path=driver_path)
            # 窗口最大化
            self.driver.maximize_window()
            # 打开JcMall商城
            #url = 'https://deyunce:911917@mall.deyunce.com/pc/'
            url = "https://www.zhihu.com/question/530732789/answer/2493415198"
            self.driver.get(url)
            # 设置隐式等待时间
            self.driver.implicitly_wait(10)
            print(f"创建浏览器的driver:{self.driver}")
            logging.info(f"测试的url是：{url}")
        else:
            print(f"复用driver:{driver}")
            self.driver = driver

    # 对单个元素定位的二次封装
    @handle_black
    def find(self, by, locator):   # find(self, by, locator) == run(self, by, locator)
        by_locator = None
        if by == 'id' or by == 'ID':
         by_locator = (By.ID, locator)
        elif by == 'class' or by == 'CLASS':
         by_locator = (By.CLASS_NAME, locator)
        elif by == 'xpath' or by == 'XPATH':
         by_locator = (By.XPATH, locator)
        elif by == 'name' or by == 'NAME':
         by_locator = (By.NAME, locator)
        elif by == 'css_selector' or by == 'CSS_SELECTOR':
         by_locator = (By.CSS_SELECTOR, locator)
        elif by == 'link_text' or by == 'LINK_TEXT':
         by_locator = (By.LINK_TEXT, locator)
        # ele = self.driver.find_element(*by_locator)
        ele = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(by_locator),
                                                  message='页面未找到元素超时')

        return ele


    # 获取多个元素的二次封装
    @handle_black
    def finds(self, by, locator):
        by_locator = None
        if by == 'id' or by == 'ID':
            by_locator = (By.ID, locator)
        elif by == 'class' or by == 'CLASS':
            by_locator = (By.CLASS_NAME, locator)
        elif by == 'xpath' or by == 'XPATH':
            by_locator = (By.XPATH, locator)
        elif by == 'name' or by == 'NAME':
            by_locator = (By.NAME, locator)
        elif by == 'css_selector' or by == 'CSS_SELECTOR':
            by_locator = (By.CSS_SELECTOR, locator)
        elif by == 'link_text' or by == 'LINK_TEXT':
            by_locator = (By.LINK_TEXT, locator)
        eles = self.driver.find_elements(*by_locator)   # 注意：eles 是一个列表
        return eles

    # 查找并点击单个元素
    @handle_black
    def find_and_click(self, by, locator):
        ele = self.find(by, locator)
        ele.click()

    # 查找多个元素并点击某个元素
    @handle_black
    def finds_and_click(self, by, locator, index):
        eles = self.finds(by, locator)
        eles[index].click()

    # 查找单个元素并向元素发送文本
    @handle_black
    def find_and_send(self, by, locator, text):
        ele = self.find(by, locator)
        ele.send_keys(text)

    # 查找多个元素并向其中某一个元素发送文本
    @handle_black
    def finds_and_send(self, by, locator, index, text):
        eles = self.finds(by, locator)
        eles[index].send_keys(text)

    # 查找单个元素并清空元素中的文本
    def find_and_clear(self, by, locator):
        ele = self.find(by, locator)
        ele.clear()

    # 查找多个元素并清空某个元素的文本
    def finds_and_clear(self, by, locator, index):
        eles = self.finds(by, locator)
        eles[index].clear()


    # 通过一个方法 run_steps 读取YAML中的数据，根据 YAML 中的关键字来实现行为驱动
    def run_steps(self, yaml_path, operation, **kwargs):
        """
        1.读取指定的路径的yaml文件-> 读取到一个字典
        2.通过for循环遍历列表中所有包含 action 的字典
        3.对包含 action 字典中的关键字进行判断，调用 action 对应关键字的方法实现元素定位与交互
        :param yaml_path:
        :param operation:
        :return:
        """
        # yaml_path = r"/Users/fujinjie/精创教学/测开班_16/PythonCode/WebUiTestFrame/py_yaml/main_page.yaml"
        with open(yaml_path, "r", encoding="UTF-8") as f:
            datas = yaml.safe_load(f)
        list_steps = datas[operation]  # steps 是一个 list 存储了一个及多个包含 action 的字典
        yaml_steps = yaml.dump(list_steps)  # 把python 数据类型转换成符合yaml语法的字符串
        res_steps_str = Template(yaml_steps).substitute(kwargs)  # 把字典kwargs中的key匹配yaml_steps中含有$符的字符串
        steps = yaml.safe_load(res_steps_str)
        for step in steps:
            sleep_time = step.get('sleep')  # 如果字典中没有这个key，通过get(key)-> None
            if sleep_time:
                time.sleep(sleep_time)
            action = step["action"]    # 字典.get(key) -> 如果 key 不存在返回None、 字典[key] -> 如果 key 不存在直接报错
            if action == "find_and_click":
                try:
                    self.find_and_click(*step["locator"])
                    logging.info(f"定位action是：{action}, 定位的locatro是：{step['locator']}")
                except Exception as e:
                    logging.error(f'{yaml_path}:{action}:{step["locator"]}元素定位异常，错误信息：{e}')
                    raise e
            elif action == "finds_and_click":
                try:
                    self.finds_and_click(*step["locator"], step["index"])
                    logging.info(f"定位action是：{action}, 定位的locatro是：{step['locator']}, 接收的index是：{step['index']}")
                except Exception as e:
                    logging.error(f'{yaml_path}:{action}:{step["locator"]}元素定位异常，错误信息：{e}')
                    raise e
            elif action == "find_and_send":
                try:
                    self.find_and_send(*step["locator"], step["text"])
                    logging.info(f"定位action是：{action}, 定位的locatro是：{step['locator']}, 接收的text是：{step['text']}")
                except Exception as e:
                    logging.error(f'{yaml_path}:{action}:{step["locator"]}元素定位异常，错误信息：{e}')
                    raise e
            elif action == "finds_and_send":
                try:
                    self.finds_and_send(*step["locator"], step['index'], step["text"])
                    logging.info(f"定位action是：{action}, 定位的locatro是：{step['locator']}, 接收的text是：{step['text']}, index是：{step['index']}")
                except Exception as e:
                    logging.error(f'{yaml_path}:{action}:{step["locator"]}元素定位异常，错误信息：{e}')
                    raise e
            elif action == "find_and_clear":
                try:
                    self.find_and_clear(*step["locator"])
                    logging.info(f"定位action是：{action}, 定位的locatro是：{step['locator']}")
                except Exception as e:
                    logging.error(f'{yaml_path}:{action}:{step["locator"]}元素定位异常，错误信息：{e}')
                    raise e
            elif action == "finds_and_clear":
                try:
                    self.finds_and_clear(*step["locator"], step['index'])
                    logging.info(f"定位action是：{action}, 定位的locatro是：{step['locator']}, 获取到的index是：{step['index']}")
                except Exception as e:
                    logging.error(f'{yaml_path}:{action}:{step["locator"]}元素定位异常，错误信息：{e}')
                    raise e
            elif action == "find":
                try:
                    ele = self.find(*step["locator"])
                    logging.info(f"定位action是：{action}, 定位的locatro是：{step['locator']}")
                    return ele
                except Exception as e:
                    logging.error(f'{yaml_path}:{action}:{step["locator"]}元素定位异常，错误信息：{e}')
                    raise e
            elif action == "finds":
                try:
                    eles = self.finds(*step["locator"])
                    logging.info(f"定位action是：{action}, 定位的locatro是：{step['locator']}")
                    return eles
                except Exception as e:
                    logging.error(f'{yaml_path}:{action}:{step["locator"]}元素定位异常，错误信息：{e}')
                    raise e


    # 根据相对路径获取YAML文件的绝对路径
    @classmethod
    def get_path(cls, relative_path):
        '''
        文件的路径拼接，返回一个绝对路径
        :param relative_path: 文件的相对路径
        :return: 文件的绝对路径
        '''
        file_path = os.path.abspath(__file__)  # 获取当前file的绝对路径 file_path = "/Users/fujinjie/精创教学/测开班_16/PythonCode/WebUiTestFrame/py_page/base_page.py"
        dir_path = os.path.split(file_path)[0] # 把获取到的路径进行分割("/Users/fujinjie/精创教学/测开班_16/PythonCode/WebUiTestFrame/py_page/","base_page.py")
        far_path = os.path.dirname(dir_path) # far_path = "/Users/fujinjie/精创教学/测开班_16/PythonCode/WebUiTestFrame"
        path = far_path + relative_path   # "/Users/fujinjie/精创教学/测开班_16/PythonCode/WebUiTestFrame"+"/py_yaml/main_page.yaml"
        return path



if __name__ == '__main__':
    # source_str = "{'action':'find_and_click', 'text': $goods_name}"
    # kw = {"goods_name": "铅笔"}
    # temp_steps = Template(source_str).substitute(kw)
    # print(temp_steps)
    # yaml_path = "/Users/fujinjie/精创教学/测开班_16/PythonCode/WebUiTestFrame/py_yaml/main_page.yaml"
    # BasePage.run_steps(yaml_path,"search_goods_name", goods_name="铅笔")
    pass

