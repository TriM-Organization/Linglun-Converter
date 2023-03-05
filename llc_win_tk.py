# -*- coding: utf-8 -*-

# 伶伦 开发交流群 861684859


"""
伶伦转换器
Linglun Converter

版权所有 © 2023 金羿 & 睿穆开发组
Copyright © 2023 EillesWan & TriM Org.

开源相关声明请见 ./License.md
Terms & Conditions: ./Lisense.md
"""

__version__ = "0.0.1"

import datetime
import os
import random
import sys

print("小贴：不妨试试Mid-BDX转换网页：在线的多功能Midi转换器")
print("https://dislink.github.io/midi2bdx/")

import Musicreater

from utils.io import *
from languages.lang import languages

MainConsole.print(
    "[#121110 on #F0F2F4]     ",
    style="#121110 on #F0F2F4",
    justify="center",
)

osc.project_name = "伶伦转换器"
osc.version = __version__


def go_for_args(
    languageChange: str = "ZH-CN", debugMode: str = "False", logfile: str = "True"
):
    global currentLang
    global logger
    currentLang = (
        languageChange.upper()
        if languageChange.upper() in languages.keys()
        else "ZH-CN"
    )
    osc.isRelease = False if debugMode.lower() in ("true", "1") else True
    logger.printing = not osc.isRelease
    logger.writing = True if logfile.lower() in ("true", "1") else False


if len(sys.argv) > 0:
    go_for_args(*sys.argv)


def _(__):
    """
    `languages`
    """
    return languages[currentLang][__]


# 显示大标题
MainConsole.rule(title="[bold #AB70FF]欢迎使用伶伦独立转换器", characters="=", style="#26E2FF")
MainConsole.rule(title="[bold #AB70FF]Welcome to Linglun Converter", characters="-")

nowYang = datetime.datetime.now()

if nowYang.month == 8 and nowYang.day == 6:
    # 诸葛八卦生日
    MainConsole.print(
        "[#7DB5F0 on #121110]今天可不是催更的日子！\n诸葛亮与八卦阵{}岁生日快乐！".format(nowYang.year - 2008),
        style="#7DB5F0 on #121110",
        justify="center",
    )
elif nowYang.month == 4 and nowYang.day == 3:
    # 金羿生日快乐
    MainConsole.print(
        "[#0089F2 on #F0F2F4]今天就不要催更啦！\n金羿{}岁生日快乐！".format(nowYang.year - 2006),
        style="#0089F2 on #F0F2F4",
        justify="center",
    )
else:
    # 显示箴言部分
    MainConsole.print(
        "[#121110 on #F0F2F4]{}".format(random.choice(myWords)),
        style="#121110 on #F0F2F4",
        justify="center",
    )

prt(f"{_('LangChd')}{_(':')}{_(currentLang)}")




def __main__():

    print('伶伦转换器简易版 正在启动……')


    print('更新执行位置...')
    if sys.platform == 'win32':
        try:
            os.chdir(__file__[:len(__file__) - __file__[len(__file__)::-1].index('\\')])
            logger.info('更新执行位置，当前文件位置 {}'.format(__file__))
        except FileNotFoundError:  # 程序规范修改：根据新的语法标准：except后面不能没有错误类型，所以既然是pass就随便填一个错误
            pass
    else:
        try:
            os.chdir(__file__[:len(__file__) - __file__[len(__file__)::-1].index('/')])
        except Exception:
            pass
        log('其他平台：{} 更新执行位置，当前文件位置 {}'.format(sys.platform, __file__))
    print('完成！')
