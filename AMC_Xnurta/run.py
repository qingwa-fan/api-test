#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import os
import sys
import subprocess
import threading
import time
import platform

import pytest

WIN = platform.system() == "Windows"

currentPath = os.path.dirname(os.path.abspath(__file__))


def main():
    """主函数"""
    steps = [
        "venv\\Script\\activate" if WIN else "source venv/bin/activate",
        "pytest -q -s -n auto --reruns 1 --alluredir allurresults --clean-alluredir",  # pytest-xdist -n auto自动适配多进程
        "allure generate allurresults -c -o allure-report",
        # "allure open allure-report"
    ]
    for step in steps:
        subprocess.run("call " + step if WIN else step, shell=True)

if __name__ == "__main__":
    main()



