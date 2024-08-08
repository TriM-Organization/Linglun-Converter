# -*- coding: utf-8 -*-

"""
伶伦转换器 言论版组件
Linglun Converter Yan Lun Component

版权所有 © 2024 金羿
Copyright © 2024 EillesWan

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""

import requests
import zhDateTime

from .io import logger, prt

STANDARD_WHITE = (242, 244, 246)
STANDART_BLACK = (18, 17, 16)

yanlun_fg_colour = STANDARD_WHITE
yanlun_bg_colour = STANDART_BLACK

logger.info("获取 言·论 信息……")

solar_datetime = zhDateTime.DateTime.now()
lunar_datetime = solar_datetime.to_lunar()
solar_date = (solar_datetime.month, solar_datetime.day)
lunar_date = (lunar_datetime.lunar_month, lunar_datetime.lunar_day)

if solar_date == (4, 3):
    yanlun_texts = ["金羿ELS 生日快乐~！", "Happy Birthday, Eilles!"]
elif solar_date == (8, 6):
    yanlun_texts = ["诸葛亮与八卦阵 生日快乐~！", "Happy Birthday, bgArray~!"]
elif solar_date == (8, 16):
    yanlun_texts = ["鱼旧梦 生日快乐~！", "Happy Birthday, ElapsingDreams~!"]

else:
    try:
        yanlun_texts = (
            requests.get(
                "https://gitee.com/TriM-Organization/LinglunStudio/raw/master/resources/myWords.txt",
            )
            .text.strip("\n")
            .split("\n")
        )
    except (ConnectionError, requests.HTTPError, requests.RequestException) as E:
        logger.warning(f"读取言·论信息发生 互联网连接 错误：\n{E}")
        yanlun_texts = ["以梦想为驱使 创造属于自己的未来"]
    # noinspection PyBroadException
    except BaseException as E:
        logger.warning(f"读取言·论信息发生 未知 错误：\n{E}")
        yanlun_texts = ["灵光焕发 深艺献心"]
