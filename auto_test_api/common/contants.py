"""
该模块用来处理整个项目目录
"""
import os


# 项目目录路径
BASEDIR = os.path.dirname(os.path.dirname(__file__))

# 配置文件路径
CONF_DIR = os.path.join(BASEDIR, "config")

# 数据目录
DATA_DIR = os.path.join(BASEDIR, "data")

# 日志目录
LOG_DIR = os.path.join(BASEDIR, "log")

# 测试报告目录
REPORT_DIR = os.path.join(BASEDIR, "allure_report")

# 测试用例模块目录
CASE_DIR = os.path.join(BASEDIR, "testcases")

# 压缩文件目录
ZIP_DIR = os.path.join(BASEDIR, "report_zip")


if __name__ == '__main__':

    print(CONF_DIR)



