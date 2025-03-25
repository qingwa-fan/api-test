#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import yaml
from config.conf import cm

sys.path.append((os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))))


class Element(object):
    """获取元素"""

    def __init__(self, name):
        """
        读取yaml文件
        :param name: yaml文件名字
        用法：Element('element')['账号']。结果：('id', 'userName')
        """
        self.file_name = '%s.yaml' % name
        self.element_path = os.path.join(cm.ELEMENT_PATH, self.file_name)
        if not os.path.exists(self.element_path):
            raise FileNotFoundError("%s 文件不存在！" % self.element_path)
        with open(self.element_path, encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def __getitem__(self, item):
        """获取属性"""
        # Element('element').__getitem__('账号')等价于Element('element')['账号']
        data = self.data.get(item)
        if data:
            name, value = data.split('==')
            return name, value
        raise ArithmeticError("{}中不存在关键字：{}".format(self.file_name, item))


# if __name__ == '__main__':
#     search = Element('element').__getitem__('账号')
#     print(search)
