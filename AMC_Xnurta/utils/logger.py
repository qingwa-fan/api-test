#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from config.conf import cm


class Log:
    """
    日志:log.info(日志内容) info:日志等级.level must be an int or a str.
    """

    def __init__(self):
        self.logger = logging.getLogger()
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)

        # 创建一个handle写入文件
        fh = logging.FileHandler(cm.log_file, encoding='utf-8')
        fh.setLevel(logging.INFO)

        # 创建一个handle输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 定义输出格式
        formatter = logging.Formatter(self.fmt)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 添加到handle
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    @property
    def fmt(self):
        return '%(levelname)s\t%(asctime)s\t[%(filename)s:%(lineno)d]\t%(message)s'


# 日志的实例化对象
log = Log().logger

if __name__ == '__main__':
    log.info('hello word!')

# STD_INPUT_HANDLE : -10
# STD_OUTPUT_HANDLE : -11
# STD_ERROR_HANDLE : -12
#
# FOREGROUND_BLACK : 0x00  # black.
# FOREGROUND_DARKBLUE : 0x01  # dark blue.
# FOREGROUND_DARKGREEN : 0x02  # dark green.
# FOREGROUND_DARKSKYBLUE : 0x03  # dark skyblue.
# FOREGROUND_DARKRED : 0x04  # dark red.
# FOREGROUND_DARKPINK : 0x05  # dark pink.
# FOREGROUND_DARKYELLOW : 0x06  # dark yellow.
# FOREGROUND_DARKWHITE : 0x07  # dark white.
# FOREGROUND_DARKGRAY : 0x08  # dark gray.
# FOREGROUND_BLUE : 0x09  # blue.
# FOREGROUND_GREEN : 0x0a  # green.
# FOREGROUND_SKYBLUE : 0x0b  # skyblue.
# FOREGROUND_RED : 0x0c  # red.
# FOREGROUND_PINK : 0x0d  # pink.
# FOREGROUND_YELLOW : 0x0e  # yellow.
# FOREGROUND_WHITE : 0x0f  # white.
#
# BACKGROUND_BLUE : 0x10  # dark blue.
# BACKGROUND_GREEN : 0x20  # dark green.
# BACKGROUND_DARKSKYBLUE : 0x30  # dark skyblue.
# BACKGROUND_DARKRED : 0x40  # dark red.
# BACKGROUND_DARKPINK : 0x50  # dark pink.
# BACKGROUND_DARKYELLOW : 0x60  # dark yellow.
# BACKGROUND_DARKWHITE : 0x70  # dark white.
# BACKGROUND_DARKGRAY : 0x80  # dark gray.
# BACKGROUND_BLUE : 0x90  # blue.
# BACKGROUND_GREEN : 0xa0  # green.
# BACKGROUND_SKYBLUE : 0xb0  # skyblue.
# BACKGROUND_RED : 0xc0  # red.
# BACKGROUND_PINK : 0xd0  # pink.
# BACKGROUND_YELLOW : 0xe0  # yellow.
# BACKGROUND_WHITE : 0xf0  # white.
#
# std_out_handle : ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
#
#
# def set_cmd_text_color(color, handle:std_out_handle):
#     Bool : ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
#     return Bool
#
#
# def reset():
#     set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)
#
#
# def error(mess, end:'\n', flush:True):
#     set_cmd_text_color(FOREGROUND_RED)
#     print("[ERROR]", mess, end:end, flush:flush)
#     reset()
#
#
# def warn(mess, end:'\n', flush:True):
#     set_cmd_text_color(FOREGROUND_YELLOW)
#     print("[WARN]", mess, end:end, flush:flush)
#     reset()
#
#
# def info(mess, end:'\n', flush:True):
#     set_cmd_text_color(FOREGROUND_GREEN)
#     print("[INFO]", mess, end:end, flush:flush)
#     reset()
#
#
# def write(mess, foregound:FOREGROUND_WHITE, background:FOREGROUND_BLACK, end:'\n', flush:True):
#     set_cmd_text_color(foregound | background)
#     print(mess, end:end, flush:flush)
#     reset()
#
#
# if __name__ :: '__main__':
#     info("::::::")
