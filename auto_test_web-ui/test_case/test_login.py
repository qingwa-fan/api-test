from py_page.main_page import MainPage
from common.log import Logger
from common.screen_short import getScreenShot
import allure
import random
from dbDatas.register_login_datas import RegisterLoginDatas
import time

logging = Logger(__name__).get_logger()
@allure.feature("测试登录模块")
class TestLogin:   # 测试类相当于一个测试集合（测试套件）

    # 测试用正确的账号密码进行登录
    @allure.title("测试用账号密码进行登录")
    @allure.story("用正确的账号密码进行登录")
    @allure.description("在JcMall商城用正确的账号密码进行登录，验证登录过程")
    def test_use_right_account_login(self, base_driver):   # base_driver = driver 是yield 后面的 driver
        # 在测试用例中 MainPage() 会创建一个 driver 对象（打开一个浏览器），在涉及页面跳转的需要复用这个 driver 对象
        logging.info("****************正在执行：test_use_right_account_login***************")
        with allure.step("进入jcmall商城首页-在首页点击【登录】-在登录页面用正确的账号密码进行登录-在首页验证登录的用户名"):
            login_name = MainPage(base_driver).goto_login_page().use_right_account_login().get_login_name()
        logging.info(f"获取到的结果是：{login_name}, 期望的结果是：思源")
        try:
            assert login_name == "思源1"
        except AssertionError as e:
            getScreenShot(__name__)
            logging.info("*******测试用例：test_use_right_account_login 断言失败为通过************")
            raise e


    def test_logout(self, base_driver_new):
        print("执行退出登录的测试")
        print(f"传入的driver对象是：{base_driver_new}")


    def test_rigister_user(self, base_driver):
        """
        判断用户是否注册成功：
        1.UI页面注册后是否有特定的元素出现提示用户注册成；
        2.注册完成后数据库查验是否增加新数据；(从数据库用户表中根据tel获取用户信息)
        """
        # 通过随机数生成新号码
        register_tel = "199" + str(random.randint(0,99999999))
        # 判断生成的新号码是否已存在于数据库，如果已经存在，再次生成新号码
        db = RegisterLoginDatas()
        has_register_mobiles = db.get_all_user_mobiles()
        while (register_tel in has_register_mobiles):
            register_tel = "199" + str(random.randint(0, 99999999))
        register_text = MainPage(base_driver).goto_register_page().user_register(mobile=register_tel, password='111111.').get_register_tosta_text()
        assert register_text == "注册成功"
        # 注册完成再次获取数据用户手机号码
        register_mobiles = db.get_all_user_mobiles()
        assert register_tel in register_mobiles
