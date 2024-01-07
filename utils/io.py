# -*- coding: utf-8 -*-

"""
伶伦转换器 命令行组件
Linglun Converter Command Line IO Component

版权所有 © 2023 金羿 & 睿穆开发组
Copyright © 2023 EillesWan & TriM Org.

开源相关声明请见 ./License.md
Terms & Conditions: ./Lisense.md
"""


import urllib.error
import urllib.request
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Set,
    TextIO,
    Tuple,
    Iterable,
    Sequence,
)

import TrimLog
from TrimLog import object_constants, logger

is_logging: bool = True

MainConsole = logger.console

logger.is_logging = True
logger.suffix = ".llc"
logger.is_tips = True


try:
    myWords = (
        urllib.request.urlopen(
            "https://gitee.com/TriM-Organization/LinglunStudio/raw/master/resources/myWords.txt"
        )
        .read()
        .decode("utf-8")
        .strip("\n")
        .split("\n")
    )
except (ConnectionError, urllib.error.HTTPError) as E:
    logger.warning(f"读取言·论信息发生 互联网连接 错误：\n{E}")
    myWords = ["以梦想为驱使 创造属于自己的未来"]
# noinspection PyBroadException
except BaseException as E:
    logger.warning(f"读取言·论信息发生 未知 错误：\n{E}")
    myWords = ["灵光焕发 深艺献心"]


JustifyMethod = Literal["default", "left", "center", "right", "full"]
OverflowMethod = Literal["fold", "crop", "ellipsis", "ignore"]


# 高级的打印函数
def prt(
    *objects: Any,
    sep: str = " ",
    end: str = "\n",
    justify: Optional[JustifyMethod] = None,
    overflow: Optional[OverflowMethod] = None,
    no_wrap: Optional[bool] = None,
    emoji: Optional[bool] = None,
    markup: Optional[bool] = None,
    highlight: Optional[bool] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crop: bool = True,
    soft_wrap: Optional[bool] = None,
    new_line_start: bool = False,
) -> None:
    """打印到控制台。

    Args:
        objects (位置性的args): 要记录到终端的对象。
        sep (str, 可选): 要在打印数据之间写入的字符串。默认为""。
        end (str, optio可选nal): 在打印数据结束时写入的字符串。默认值为"\\\\n"。
        justify (str, 可选): 校正位置，可为"default", "left", "right", "center" 或 "full". 默认为`None`。
        overflow (str, 可选): 控制溢出："ignore"忽略, "crop"裁剪, "fold"折叠, "ellipsis"省略号。默认为`None`。
        no_wrap (Optional[bool], 可选): 禁用文字包装。默认为`None`。
        emoji (Optional[bool], 可选): 启用表情符号代码，或使用控制台默认的`None`。默认为`None`。
        markup (Optional[bool], 可选): 启用标记，或`None`使用控制台默认值。默认为`None`。
        highlight (Optional[bool], 可选): 启用自动高亮，或`None`使用控制台默认值。默认为`None`。
        width (Optional[int], 可选): 输出的宽度，或`None`自动检测。默认为`None`。
        height
        crop (Optional[bool], 可选): 裁剪输出到终端的宽度。默认为`True`。
        soft_wrap (bool, 可选): 启用软包装模式，禁止文字包装和裁剪，或`None``用于 控制台默认值。默认为`None`。
        new_line_start (bool, False): 如果输出包含多行，在开始时插入一个新行。默认值为`False`。
    """
    MainConsole.print(
        *objects,
        sep=sep,
        end=end,
        style="#F0F2F4 on #121110",
        justify=justify,
        overflow=overflow,
        no_wrap=no_wrap,
        emoji=emoji,
        markup=markup,
        highlight=highlight,
        width=width,
        height=height,
        crop=crop,
        soft_wrap=soft_wrap,
        new_line_start=new_line_start,
    )


# 高级的输入函数
def ipt(
    *objects: Any,
    sep: str = " ",
    justify: Optional[JustifyMethod] = None,
    overflow: Optional[OverflowMethod] = None,
    no_wrap: Optional[bool] = None,
    emoji: Optional[bool] = None,
    markup: Optional[bool] = None,
    highlight: Optional[bool] = None,
    width: Optional[int] = None,
    height: Optional[int] = None,
    crop: bool = True,
    soft_wrap: Optional[bool] = None,
    new_line_start: bool = False,
    password: bool = False,
    stream: Optional[TextIO] = None,
) -> str:
    """显示一个提示并等待用户的输入。

    它的工作方式与Python内建的 :func:`input` 函数相同，如果Python内建的 :mod:`readline` 模块先前已经加载，则提供详细的行编辑和历史功能。

    Args:
        objects (位置性的args): 要记录到终端的对象。
        sep (str, 可选): 要在打印数据之间写入的字符串。默认为""。
        justify (str, 可选): 校正位置，可为"default", "left", "right", "center" 或 "full". 默认为`None`。
        overflow (str, 可选): 控制溢出："ignore"忽略, "crop"裁剪, "fold"折叠, "ellipsis"省略号。默认为`None`。
        no_wrap (Optional[bool], 可选): 禁用文字包装。默认为`None`。
        emoji (Optional[bool], 可选): 启用表情符号代码，或使用控制台默认的`None`。默认为`None`。
        markup (Optional[bool], 可选): 启用标记，或`None`使用控制台默认值。默认为`None`。
        highlight (Optional[bool], 可选): 启用自动高亮，或`None`使用控制台默认值。默认为`None`。
        width (Optional[int], 可选): 输出的宽度，或`None`自动检测。默认为`None`。
        crop (Optional[bool], 可选): 裁剪输出到终端的宽度。默认为`True`。
        height
        soft_wrap (bool, 可选): 启用软包装模式，禁止文字包装和裁剪，或`None``用于 控制台默认值。默认为`None`。
        new_line_start (bool, False): 如果输出包含多行，在开始时插入一个新行。默认值为`False`。
        password (bool, 可选): 隐藏已经输入的文案，默认值为`False`。
        stream (TextIO, 可选): 可选从文件中读取（而非控制台），默认为 `None`。

    Returns:
        str: 从stdin读取的字符串
    """
    MainConsole.print(
        *objects,
        sep=sep,
        end="",
        style="#F0F2F4 on #121110",
        justify=justify,
        overflow=overflow,
        no_wrap=no_wrap,
        emoji=emoji,
        markup=markup,
        highlight=highlight,
        width=width,
        height=height,
        crop=crop,
        soft_wrap=soft_wrap,
        new_line_start=new_line_start,
    )

    return MainConsole.input(password=password, stream=stream)


def format_ipt(
    notice: str,
    fun: Callable,
    err_note: str = "{}",
    strict_mode: bool = False,
    *extraArg,
) -> Tuple[str, Any]:
    """循环输入，以某种格式
    notice: 输入时的提示
    fun: 格式函数
    err_note: 输入不符格式时的提示
    strict_mode: 是否将函数值作为结束循环的判断依据之一
    *extraArg: 对于函数的其他参数"""
    while True:
        result = ipt(notice)
        try:
            if strict_mode:
                if fun_result := fun(result, *extraArg):
                    break
            else:
                fun_result = fun(result, *extraArg)
                break
        except ValueError as E:
            prt(err_note.format(E))
            continue
    return result, fun_result


def isin(sth: str, range_list: dict):
    sth = sth.lower()
    for bool_value, res_list in range_list.items():
        if sth in res_list:
            return bool_value
    raise ValueError


# 真假字符串判断
def bool_str(sth: str):
    try:
        return bool(float(sth))
    except:
        if str(sth).lower() in ("true", "真", "是", "y", "t"):
            return True
        elif str(sth).lower() in ("false", "假", "否", "f", "n"):
            return False
        else:
            raise ValueError


def float_str(sth: str):
    try:
        return float(sth)
    except ValueError:
        try:
            return float(
                sth.replace("壹", "1")
                .replace("贰", "2")
                .replace("叁", "3")
                .replace("肆", "4")
                .replace("伍", "5")
                .replace("陆", "6")
                .replace("柒", "7")
                .replace("捌", "8")
                .replace("玖", "9")
                .replace("零", "0")
                .replace("一", "1")
                .replace("二", "2")
                .replace("三", "3")
                .replace("四", "4")
                .replace("五", "5")
                .replace("六", "6")
                .replace("七", "7")
                .replace("八", "8")
                .replace("九", "9")
                .replace("〇", "0")
                .replace("洞", "0")
                .replace("幺", "1")
                .replace("俩", "2")
                .replace("两", "2")
                .replace("拐", "7")
                .replace("点", ".")
            )
        except:
            raise ValueError


def int_str(sth: str):
    try:
        return int(float_str(sth))
    except ValueError:
        raise ValueError
