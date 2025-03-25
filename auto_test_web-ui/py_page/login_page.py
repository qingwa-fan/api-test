import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from py_page.base_page import BasePage
from common.log import Logger

logging = Logger(__name__).get_logger()
class LoginPage(BasePage):

    path = BasePage.get_path("/py_yaml/login_page.yaml")

    # 用正确的账号密码登录
    def use_right_account_login(self):
        logging.info("在登录页面用正确的账号密码进行登录")
        self.run_steps(self.path, "use_right_account_login")
        logging.info("登录完成后跳转到首页")
        from py_page.main_page import MainPage
        return MainPage(self.driver)
