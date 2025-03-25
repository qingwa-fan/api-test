import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from py_page.base_page import BasePage
from common.log import Logger

logging = Logger(__name__).get_logger()
class MainPage(BasePage):

    path = BasePage.get_path("/py_yaml/main_page.yaml")

    # 在首页点击【登录】跳转到登录页面
    def goto_login_page(self):
        logging.info("在首页点击【登录】跳转到登录页面")
        self.run_steps(self.path, "goto_login_page")
        from py_page.login_page import LoginPage
        return LoginPage(self.driver)    # 返回登录页面的对象，凡是涉及页面跳转的需要把self.driver,作为参数传入页面对象中


    # 再首页点击【注册】跳转到注册页面
    def goto_register_page(self):
        logging.info("在首页点击【注册】跳转到注册页面")
        self.run_steps(self.path, "goto_register_page")
        from py_page.register_page import RegisterPage
        return RegisterPage(self.driver)

    # 在首页点击第index的商品进入商品详情
    def goto_goods_detail_page(self, index):
        logging.info(f"在首页点击index={index}的商品，进入商品详情")
        self.run_steps(self.path, "goto_goods_detail_page", num=index)
        time.sleep(5)
        from py_page.goods_detail_page import GoodsDetailPage
        return GoodsDetailPage()  # 返回商品详情页面的对象

    # 在首页搜索商品
    def search_goods_name(self, goods):
        logging.info(f"在首页搜索框输入{goods}进行商品搜索")
        eles = self.run_steps(self.path, "search_goods_name", goods_name=goods)
        goods_name_list = [ele.text for ele in eles]
        logging.info(f"获取到的商品名称列表是{goods_name_list}")
        return goods_name_list


    # 获取搜索结果
    # def get_search_goods(self):
    #     time.sleep(3)
    #     eles = self.run_steps(self.path, "get_search_goods")
    #     goods_name_list = [ele.text for ele in eles]
    #     logging.info(f"在首页搜索框输入{goods}进行商品搜索")
    #     return goods_name_list

    # 在首页获取登录的用户名
    def get_login_name(self):
        # 在首页获取登录的用户名
        ele = self.run_steps(self.path, "get_login_name")
        login_name = ele.text
        logging.info(f"获取到的首页登录用户名是：{login_name}")
        return login_name


    def click_mainPage_icon(self):
        self.run_steps(self.path, "click_mainPage_icon")


