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

__version__ = "0.0.6"

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

# from Musicreater.plugin.mcstructure import commands_to_structure, commands_to_redstone_delay_structure

from utils.io import *

MainConsole.print(
    "[#121110 on #F0F2F4]     ",
    style="#121110 on #F0F2F4",
    justify="center",
)

osc.project_name = "伶伦转换器"
osc.version = __version__


if len(sys.argv) > 0:

    def go_for_args(debugMode: str = "False", logfile: str = "True"):
        global logger
        osc.isRelease = False if debugMode.lower() in ("true", "1") else True
        logger.printing = not osc.isRelease
        logger.writing = True if logfile.lower() in ("true", "1") else False

    go_for_args(*sys.argv)


# 显示大标题
MainConsole.rule(title="[bold #AB70FF]欢迎使用伶伦独立转换器", characters="=", style="#26E2FF")
# MainConsole.rule(title="[bold #AB70FF]Welcome to Linglun Converter", characters="-")
MainConsole.rule(
    title="[#AB70FF]版本{} | 音·创内核版本{}".format(__version__, Musicreater.__version__),
    characters="-",
    style="#26E2FF",
)

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

# prt(f"{_('LangChd')}{_(':')}{_(currentLang)}")


def format_ipt(
    notice: str,
    fun,
    err_note: str = "输入内容有误，请重新输入。",
    *extraArg,
):
    """循环输入，以某种格式
    notice: 输入时的提示
    fun: 格式函数
    err_note: 输入不符格式时的提示
    *extraArg: 对于函数的其他参数"""
    while True:
        result = ipt(notice)
        try:
            fun_result = fun(result, *extraArg)
            break
        except ValueError:
            prt(err_note)
            continue
    return result, fun_result


# 获取midi列表
while True:
    midi_path = ipt(f"请键入MIDI地址或所在目录地址：")
    try:
        if os.path.exists(midi_path):
            if os.path.isfile(midi_path):
                midis = (midi_path,)
            elif os.path.isdir(midi_path):
                midis = (
                    os.path.join(midi_path, i)
                    for i in os.listdir(midi_path)
                    if i.lower().endswith(".mid") or i.lower().endswith(".midi")
                )
            else:
                prt("输入内容有误，请重新输入。")
                continue
        else:
            prt("该地址不存在，或无法访问该地址，请重新输入。")
            continue
    except PermissionError:
        prt("无法访问该地址，请检查是否给予程序相关文件的访问权限。")
        continue
    break

# 获取输出地址
while True:
    out_path = ipt(f"请键入文件生成输出地址：")
    try:
        if not os.path.exists(out_path):
            prt("该地址不存在，或无法访问该地址，请重新输入。")
            continue
    except PermissionError:
        prt("无法访问该地址，请检查是否给予程序相关文件的访问权限。")
        continue
    break


# 选择输出格式


def is_in_bdx_mcpack(sth: str):
    return isin(sth, {1: ("bdx", "1", "币帝查", "币帝·艾克斯"), 0: ("mcpack", "0", "唉姆西·派克")})


def is_in_player(sth: str):
    return isin(
        sth,
        {
            0: ("delay", "0", "延迟", "帝蕾"),
            1: ("score", "1", "计分板", "积分", "积分板", "计分", "斯阔尔"),
            2: ("repeater", "2", "中继器", "瑞皮特"),
        },
    )


output_file_format = format_ipt(
    "请键入输出文件类型 (mcpack/0|bdx/1)",
    is_in_bdx_mcpack,
    "输入内容有误，请重新输入。",
)[1]

if output_file_format == 0:
    player_format = format_ipt(
        "请选择播放器类型 (延迟/0|计分板/1|中继器/2)",
        is_in_player,
        "输入内容有误，请重新输入。",
    )[1]
else:
    player_format = format_ipt(
        "请选择播放器类型 (延迟/0|计分板/1)",
        is_in_player,
        "输入内容有误，请重新输入。",
    )[1]

old_exe_enabled = format_ipt(
    "启用1.19以前的旧版execute指令格式 (否/0|是/1)：", bool_str, "输入内容格式错误，应为 是/1/真/t/y 或 否/0/假/f/n"
)[1]


if os.path.exists("./demo_config.json"):
    import json

    prompts = json.load(open("./demo_config.json", "r", encoding="utf-8"))

    prompts = prompts[:-1]
else:
    prompts = []
    # 提示语 检测函数 错误提示语
    for args in [
        (
            "音量大小 (0,1]：",
            float_str,
        ),
        (
            "速度倍率 (0,+∞)：",
            float_str,
        ),
        (
            "自动生成进度条 (否/0|是/1)：",
            bool_str,
        ),
        (
            "计分板名称：",
            str,
        )
        if player_format == 1
        else (
            "受播放玩家的选择器：",
            str,
        ),
        (
            "自动重置计分板 (否/0|是/1)：",
            bool_str,
        )
        if player_format == 1
        else (),
        (
            "BDX作者署名：",
            str,
        )
        if output_file_format == 1
        else (),
        (
            "结构生成最大高度 (0,+∞)：",
            int,
        )
        if player_format == 0
        else (),
    ]:
        if args:
            prompts.append(
                format_ipt(*args, err_note="输入内容格式错误，应符合 {}".format(args[1]))[1]
            )

if prompts[2]:
    costom_pgb_enabled = format_ipt(
        "自定义进度条样式 (否/0|是/1)：", bool_str, "输入内容格式错误，应为 是/1/真/t/y 或 否/0/假/f/n"
    )[1]
    if costom_pgb_enabled:
        style = ipt("基本样式组 (回车默认)：")
        if not style:
            style = DEFAULT_PROGRESSBAR_STYLE[0]
        yet_part = ipt("未播放样式 (回车默认)：")
        if not yet_part:
            yet_part = DEFAULT_PROGRESSBAR_STYLE[1][1]
        done_part = ipt("已播放样式 (回车默认)：")
        if not done_part:
            done_part = DEFAULT_PROGRESSBAR_STYLE[1][0]

if player_format == 1:
    cvt_method = to_addon_pack_in_score
elif player_format == 0:
    cvt_method = to_addon_pack_in_delay
elif player_format == 2:
    cvt_method = to_addon_pack_in_repeater


for singleMidi in midis:
    prt("\n" f"正在处理 {singleMidi}")
    cvt_mid = Musicreater.MidiConvert.from_midi_file(
        singleMidi, old_exe_format=old_exe_enabled
    )
    cvt_cfg = ConvertConfig(out_path, *prompts[:2], progressbar=((style, (done_part, yet_part)) if costom_pgb_enabled else True) if prompts[2] else False)  # type: ignore

    conversion_result = (
        (cvt_method(cvt_mid, cvt_cfg, *prompts[3:]))  # type: ignore
        if output_file_format == 0
        else (
            to_BDX_file_in_score(cvt_mid, cvt_cfg, *prompts[3:])
            if player_format == 1
            else to_BDX_file_in_delay(cvt_mid, cvt_cfg, *prompts[3:])
        )
    )

    prt(
        f"	指令总长：{conversion_result[0]}，播放刻数：{conversion_result[1]}{f'''，结构大小：{conversion_result[2]}，末点坐标：{conversion_result[3]}''' if output_file_format == 1 else ''}"  # type: ignore
    )

exitSth = ipt("结束。换行以退出程序。")
if exitSth == "record":
    import json

    with open("./demo_config.json", "w", encoding="utf-8") as f:
        json.dump(prompts, f)
elif exitSth == "delrec":
    os.remove("./demo_config.json")
