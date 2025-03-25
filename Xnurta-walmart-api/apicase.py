#!/usr/bin/env python3
# 程序主入口
import sys
import pytest,os
import requests

# import sys
# print(sys.path)
# Walmart = os.path.dirname(os.path.dirname(__file__))
# print(Walmart)
# sys.path.append("yiyan/Xnurta/main.py")
if __name__ == '__main__':
    pytest.main(["-vs",
                 "--capture=sys", # 控制台输出
                 "Walmart/framework.py", # 要执行这个文件,Test_walmart
                 "--clean-alluredir", # 清除之前生成的测试报告
                 "--alluredir=allure-results" # 生成测试报告
                 ])
    os.system("allure generate ./allure-results/ -o ./allure_walmart_test/ --clean")# 执行操作系统命令，文件名变更



