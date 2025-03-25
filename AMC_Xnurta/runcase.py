#!/usr/bin/env python3.8
# -*- coding:utf-8 -*-
import os
import sys
import subprocess
import threading
import time

import pytest

# WIN = sys.platform.startswith('win')

currentPath = os.path.dirname(os.path.abspath(__file__))


# def main():
#     """主函数"""
#     steps = [
#         "venv\\Script\\activate" if WIN else "source venv/bin/activate",
#         "pytest -v -n auto --alluredir allurresults --clean-alluredir", #pytest-xdist -n auto自动适配多进程
#         "allure generate allurresults -c -o allure-report",
#     ]
#     for step in steps:
#         subprocess.run("call " + step if WIN else step, shell=True)
def create_virtualenv():
    """创建虚拟环境"""
    venv_dir = "venv"
    if not os.path.exists(venv_dir):
        print("虚拟环境不存在，正在创建...")
        subprocess.run(f"python3.8 -m venv {venv_dir}", shell=True, check=True)
    else:
        print("虚拟环境已存在。")

def main():
    """主函数"""
    # 创建虚拟环境（如果不存在）
    create_virtualenv()
    steps = [
        "source venv/bin/activate",
        "python3.8 -m pytest -q -s -n auto --reruns 1   --alluredir allurresults --clean-alluredir", #pytest-xdist -n auto自动适配多进程
        "python3.8 -m allure generate allurresults -c -o allure-report",
    ]
    for step in steps:
        try:
            # 在 Linux 下直接运行命令，不需要 `call`
            subprocess.run(step, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"命令执行失败: {e}")
            sys.exit(1)  # 如果某一步失败，退出脚本

if __name__ == "__main__":
    main()