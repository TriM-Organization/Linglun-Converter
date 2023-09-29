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


import Musicreater
from Musicreater.plugin import ConvertConfig
from Musicreater.plugin.bdxfile import to_BDX_file_in_delay, to_BDX_file_in_score
from Musicreater.plugin.addonpack import (
    to_addon_pack_in_delay,
    to_addon_pack_in_repeater,
    to_addon_pack_in_score,
)
from Musicreater.constants import DEFAULT_PROGRESSBAR_STYLE


from utils.io import *

osc.project_name = "伶伦转换器"
osc.version = __version__


def __main__():
    MainConsole.print(
        "[#121110 on #F0F2F4]     ",
        style="#121110 on #F0F2F4",
        justify="center",
    )

    if len(sys.argv) > 0:

        def go_for_args(debugMode: str = "False", logfile: str = "True"):
            global logger
            osc.isRelease = False if debugMode.lower() in ("true", "1") else True
            logger.printing = not osc.isRelease
            logger.writing = True if logfile.lower() in ("true", "1") else False

        go_for_args(*sys.argv)

    # 显示大标题
    MainConsole.rule(title="[bold #AB70FF]欢迎使用伶伦独立转换器", characters="=", style="#26E2FF")
    MainConsole.rule(title="[bold #AB70FF]Welcome to Linglun Converter", characters="-")

    nowYang = datetime.datetime.now()

    if nowYang.month == 8 and nowYang.day == 6:
        # 诸葛八卦生日
        MainConsole.print(
            "[#7DB5F0 on #121110]今天可不是催更的日子！\n诸葛亮与八卦阵{}岁生日快乐！".format(
                nowYang.year - 2008
            ),
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

    prt("伶伦转换器简易版 正在启动……")

    prt("更新执行位置...")
    if sys.platform == "win32":
        try:
            os.chdir(
                __file__[: len(__file__) - __file__[len(__file__) :: -1].index("\\")]
            )
            logger.info("Win32 更新执行位置，当前文件位置 {}".format(__file__))
        except FileNotFoundError:
            pass
    else:
        try:
            os.chdir(
                __file__[: len(__file__) - __file__[len(__file__) :: -1].index("/")]
            )
        except FileNotFoundError:
            pass
        log("其他平台：{} 更新执行位置，当前文件位置 {}".format(sys.platform, __file__))
    prt("完成！")

    prt("载入功能……")
