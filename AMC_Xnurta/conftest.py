#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import base64

from selenium.webdriver import DesiredCapabilities

from common.readconfig import ini
import pytest

from py.xml import html
from selenium import webdriver
import platform

from common.readelement import Element
from config.conf import ConfigManager
from page_object.登录 import LoginObject
from utils.times import timestamp
from utils.times import dt_strftime
import os
import allure
from utils.logger import log

driver = None
elementlogin = Element('登录')

'''
conftest.py文件名称是固定的，pytest会自动识别该文件。放到工程的根目录下，就可以全局调用了，如果放到某个package包下，那就只在该package内有效
scope参数：标记方法的作用域。有4个可选值：function（默认，函数）、class（类）、module（模块）、package/session（包）
function:所有的函数在执行之前都会执行函数
class:每个class前执行一次
module：在当前.py脚本里面所有用例开始前只执行一次
package/session：可以跨.py模块调用的,也就是当我们有多个.py文件的用例时候，如果多个用例只需调用一次fixture，那就可以设置为scope="session"，并且写到conftest.py文件里
默认：被装饰的方法不会执行，被作用的类中的每个函数执行之前都会执行一次，在测试类前面添加：@pytest.mark.usefixtures('XXX') 其中XXX为被装饰的函数名
Scope使用范围大的fixture先执行："session"> "package"> "module"> "class">"function"
'''


# 是多个文件调用一次，可以跨.py文件调用，每个.py文件就是module
@pytest.fixture(scope='function')
def drivers(request):
    """整个包执行一次drivers方法
    :param request:
    :return: driver:默认调用chrome浏览器
    """
    global driver
    chromeOptions = webdriver.ChromeOptions()
    # 解决DevToolsActivePort文件不存在的报错
    chromeOptions.add_argument('--no-sandbox')
    # 适配jenkins构建时的报错{"error":"element not interactable"}
    chromeOptions.add_argument("--window-size=1920,1080")
    # 大量渲染时候写入/tmp而非/dev/shm
    chromeOptions.add_argument('--disable-dev-shm-usage')
    # 去掉提示以开发者模式调用
    chromeOptions.add_experimental_option("useAutomationExtension", False)
    # 以开发者模式启动调试chrome，可以去掉提示受到自动软件控制
    chromeOptions.add_experimental_option("excludeSwitches", ['enable-automation'])
    # 无界面模式    调试时关闭
    chromeOptions.add_argument('--headless')
    chromeOptions.add_argument('window-size=1920x1440')
    # 谷歌禁用GPU加速
    chromeOptions.add_argument('-–disable-gpu')
    # 判断操作系统
    if platform.system() == "Linux":
        # Linux 下连接到容器中的 Selenium 服务
        selenium_hub_url = "http://localhost:4444/wd/hub"  # 替换为你的 Selenium Hub 地址
        driver = webdriver.Remote(
            command_executor=selenium_hub_url,
            options=chromeOptions
        )
        print("Running on Linux: Connected to Selenium Grid in Docker container.")
    else:
        # Windows 下直接启动本地浏览器
        driver = webdriver.Chrome(options=chromeOptions)
    # # #调试时打开，第二个屏内运行
    # second_screen_x = 1920  # 第二个屏幕的起始 X 坐标
    # second_screen_y = 0  # 第二个屏幕的起始 Y 坐标
    # driver.set_window_position(second_screen_x, second_screen_y)
    driver.maximize_window()

    # 调试时关闭
    def fn():
        if driver:
            driver.quit()
    request.addfinalizer(fn)
    # #
    return driver


# pytest.hookimpl该插件作用于pytest的钩子函数上，可以获取到测试用例不同执行阶段的结果（setup，call，teardown）
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    # 获取钩子方法的调用结果,返回一个result对象
    # 获取调用结果的测试报告，返回一个report对象, reportd对象的属性包括when（steup, call, teardown三个值）、
    # nodeid(测试用例的名字)、outcome(用例的执行结果，passed,failed)
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            file_name = report.nodeid.replace("::", "_") + ".png"
            screen_img = _capture_screenshot()
            if file_name:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:600px;height:300px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))

            report.extra = extra
        report.description = str(item.function.__doc__)
        report.nodeid = report.nodeid.encode("utf-8").decode("unicode-escape")


def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例名称'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)


def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))


@pytest.mark.optionalhook
def pytest_html_report_title(report):
    report.title = "Xnurta自动化测试报告"




@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    # prefix.clear() # 清空summary中的内容
    prefix.extend([html.p("所属部门: R&D Unit-J")])
    prefix.extend([html.p("测试执行人: Leo sui")])


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    最后的结果汇总,可以拿到所有的执行结果
    :param terminalreporter: (_pytest.terminal.TerminalReporter) – 内部使用的终端测试报告对象
    :param exitstatus: (int) – 返回给操作系统的返回码
    :param config: (_pytest.config.Config) - pytest config对象
    :return:
    """
    """收集测试结果"""
    result = {
        "total": terminalreporter._numcollected,
        'passed': len(terminalreporter.stats.get('passed', [])),
        'failed': len(terminalreporter.stats.get('failed', [])),
        'error': len(terminalreporter.stats.get('error', [])),
        'skipped': len(terminalreporter.stats.get('skipped', [])),
        'total times': timestamp() - terminalreporter._sessionstarttime
    }
    # if result['failed'] or result['error']:
        # send_report()


def _capture_screenshot():
    """
    截图保存为base64
    """
    SCREENSHOT_DIR = os.path.join(ConfigManager.BASE_DIR, 'screenshot')
    now_time = dt_strftime("%Y%m%d%H%M%S")
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    screen_path = os.path.join(SCREENSHOT_DIR, "{}.png".format(now_time))
    driver.save_screenshot(screen_path)
    allure.attach.file(screen_path, "测试失败截图...{}".format(
        now_time), allure.attachment_type.PNG)
    with open(screen_path, 'rb') as f:
        imagebase64 = base64.b64encode(f.read())
    return imagebase64.decode()


