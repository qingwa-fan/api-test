import os
import pytest
from common.my_log import Logger


logging = Logger(__name__).get_logger()

logging.info("开始测试")
try:
	pytest.main(['-v', '--alluredir', './result', '--clean-alluredir'])
	os.system('allure generate ./result -o ./report --clean')
except:
	logging.info("测试任务报错")