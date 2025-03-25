import time

import pytest
from py_page.base_page import BasePage
from common.log import Logger
from common.send_res import SendReportMessage

logging = Logger(__name__).get_logger()

@pytest.fixture()
def base_driver():
    """
    测试用例的前置条件：通过BasePage创建driver,传入测试用例；
    测试用例后置条件：把driver 进行关闭；
    """
    base_page = BasePage()   # 创建BasePage() 对象
    driver = base_page.driver
    yield driver    # 返回创建的 driver 对象给测试用例，相当于 return
    driver.quit()   # 测试用例执行完毕进行浏览器退出



@pytest.fixture()
def base_driver_new():
    print("实例化 BasePage(),获取构造方法中的 driver，并通过 yield 返回出去")
    driver = "1122333"
    yield driver
    print("测试用例结束关闭driver释放资源")


# 钩子函数
def pytest_terminal_summary(terminalreporter):
    """收集测试结果"""
    duration = time.time() - terminalreporter._sessionstarttime
    test_result = dict(total=terminalreporter._numcollected,
                       passed=len(terminalreporter.stats.get('passed', [])),
                       failed=len(terminalreporter.stats.get('failed', [])),
                       error=len(terminalreporter.stats.get('error', [])),
                       skipped=len(terminalreporter.stats.get('skipped', [])),
                       total_time=f"{duration} seconds")
    resport_str = f"本次测试结果：\n" \
                  f"total: {test_result.get('total')}\n" \
                  f"passed: {test_result.get('passed')}\n" \
                  f"failed: {test_result.get('failed')}\n" \
                  f"error: {test_result.get('error')}\n" \
                  f"skipped: {test_result.get('skipped')}\n" \
                  f"total_time: {test_result.get('total_time')}"
    logging.info(resport_str)
    # 发送通过钉钉发送测试简报
    SendReportMessage().send_dingtalk_message(resport_str)


