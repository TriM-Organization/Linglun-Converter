# -*- coding: utf-8 -*-

# 伶伦 开发交流群 861684859


"""
伶伦转换器 命令行
Linglun Converter CLI

版权所有 © 2025 金羿
Copyright © 2025 EillesWan

伶伦转换器命令行版本（“本项目”）的协议颁发者为 金羿
The Licensor of _Linglun Converter CLI_("this project") is Eilles Wan.

本项目根据 汉钰律许可协议，第一版（“本协议”）授权。
任何人皆可从以下地址获得本协议副本：https://gitee.com/EillesWan/YulvLicenses。
若非因法律要求或经过了特殊准许，此作品在根据本协议“原样”提供的基础上，不予提供任何形式的担保、任何明示、任何暗示或类似承诺。也就是说，用户将自行承担因此作品的质量或性能问题而产生的全部风险。
详细的准许和限制条款请见原协议文本。
"""

__version__ = "0.0.9.2"


import os
import random

try:

    import Musicreater
    from Musicreater import DEFAULT_PROGRESSBAR_STYLE
    from Musicreater.plugin.addonpack import (
        to_addon_pack_in_delay,
        to_addon_pack_in_repeater,
        to_addon_pack_in_score,
    )
    from Musicreater.plugin.bdxfile import to_BDX_file_in_delay, to_BDX_file_in_score
    from Musicreater.plugin.mcstructfile import (
        to_mcstructure_file_in_delay,
        to_mcstructure_file_in_repeater,
        to_mcstructure_file_in_score,
    )

    from utils.io import bool_str, float_str, int_str, ipt, isin, logger, prt
    from utils.yanlun import solar_date, yanlun_texts

except ImportError:
    if input("[ERROR] 当前环境中未安装所需依赖库，是否直接安装依赖库？[Y/n]") in (
        "y",
        "Y",
    ):
        os.system("pip install -r ./requirements_cli.txt")
        print("[INFO] 安装完成，请重新启动。")

    exit()

# import sys


# from Musicreater.plugin.mcstructure import commands_to_structure, commands_to_redstone_delay_structure


logger.console.print(
    "[#121110 on #F0F2F4]     ",
    style="#121110 on #F0F2F4",
    justify="center",
)

# osc.project_name = "伶伦转换器"
# osc.version = __version__


# if len(sys.argv) > 0:

#     def go_for_args(debugMode: str = "False", logfile: str = "True"):
#         global logger
#         osc.isRelease = False if debugMode.lower() in ("true", "1") else True
#         logger.printing = not osc.isRelease
#         logger.writing = True if logfile.lower() in ("true", "1") else False

#     go_for_args(*sys.argv)


# 显示大标题
logger.console.rule(
    title="[bold #AB70FF]欢迎使用伶伦独立转换器", characters="=", style="#26E2FF"
)
# MainConsole.rule(title="[bold #AB70FF]Welcome to Linglun Converter", characters="-")
logger.console.rule(
    title="[#AB70FF]版本{} | 音·创内核版本{}".format(
        __version__, Musicreater.__version__
    ),
    characters="-",
    style="#26E2FF",
)


if solar_date == (4, 3):
    # 诸葛八卦生日
    style_ = "#7DB5F0 on #121110"
elif solar_date == (8, 6):
    # 金羿生日快乐
    style_ = "#0089F2 on #F0F2F4"
elif solar_date == (8, 16):
    # 旧梦生日快乐
    style_ = "#F0F2F4 on #0089F2"  # TODO
else:
    style_ = "#121110 on #F0F2F4"
    yanlun_texts = [""]
# 显示箴言部分
logger.console.print(
    "[{}]{}".format(style_, random.choice(yanlun_texts)),
    style=style_,
    justify="center",
)
del style_

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
    midi_path = ipt(f"MIDI地址或所在目录地址：")
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
    out_path = ipt(f"文件生成输出地址：")
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
    return isin(
        sth.lower(),
        {
            1: ("bdx", "1", "币帝查", "币帝·艾克斯", "一", "幺"),
            0: ("mcpack", "0", "唉姆西·派克", "零", "〇"),
            2: ("mcstructure", "2", "二", "麦块结构", "MC结构", "两", "我的世界结构"),
        },
    )


def is_in_player(sth: str, in_ok: tuple = (0, 1, 2)):
    return isin(
        sth.lower(),
        dict(
            [
                (i, v)
                for i, v in [
                    (
                        0,
                        ("delay", "0", "延迟", "帝蕾"),
                    ),
                    (
                        1,
                        ("score", "1", "计分板", "积分", "积分板", "计分", "斯阔尔"),
                    ),
                    (
                        2,
                        ("repeater", "2", "中继器", "瑞皮特尔"),
                    ),
                ]
                if i in in_ok
            ]
        ),
    )


output_file_format = format_ipt(
    "输出文件类型 (mcpack/0|bdx/1|mcstructure/2)：",
    is_in_bdx_mcpack,
    "输入内容有误，请重新输入。",
)[1]

if output_file_format == 1:
    player_format = format_ipt(
        "播放器类型 (延迟/0|计分板/1)：",
        lambda a: is_in_player(a, (0, 1)),
        "输入内容有误，请重新输入。",
    )[1]
else:
    player_format = format_ipt(
        "播放器类型 (延迟/0|计分板/1|中继器/2)：",
        is_in_player,
        "输入内容有误，请重新输入。",
    )[1]

old_exe_enabled = format_ipt(
    "启用旧版代行指令 (否/0|是/1)：",
    bool_str,
    "输入内容格式错误，应为 是/1/真/t/y 或 否/0/假/f/n",
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
            "速度倍率 (0,+∞)：",
            float_str,
        ),
        (
            "最小音量 (0,1]：",
            float_str,
        ),
        (
            (
                "自动生成进度条 (否/0|是/1)：",
                bool_str,
            )
            if output_file_format != 2
            else ()
        ),
        (
            (
                "计分板名称：",
                str,
            )
            if player_format == 1
            else (
                "受播放玩家的选择器：",
                str,
            )
        ),
        (
            (
                "自动重置计分板 (否/0|是/1)：",
                bool_str,
            )
            if player_format == 1
            else ()
        ),
        (
            (
                "BDX作者署名：",
                str,
            )
            if output_file_format == 1
            else (
                (
                    "结构延展方向 (x+|z+|x-|z-)：",
                    lambda a: isin(
                        a,
                        {
                            "z+": ["z+", "Z+"],
                            "x+": ["X+", "x+"],
                            "z-": ["Z-", "z-"],
                            "x-": ["x-", "X-"],
                        },
                    ),
                )
                if (player_format == 2 and output_file_format == 2)
                else ()
            )
        ),
        (
            (
                "基础底部方块 (例：concrete)：",
                str,
            )
            if (player_format == 2 and output_file_format == 2)
            else (
                (
                    "结构生成最大高度 (0,+∞)：",
                    int_str,
                )
                if player_format == 0 or output_file_format != 0
                else ()
            )
        ),
    ]:
        if args:
            prompts.append(
                format_ipt(
                    *args, err_note="输入内容格式错误，应符合 {}".format(args[1])
                )[1]
            )

if output_file_format != 2 and prompts[2]:
    style = DEFAULT_PROGRESSBAR_STYLE
    costom_pgb_enabled = format_ipt(
        "自定义进度条样式 (否/0|是/1)：",
        bool_str,
        "输入内容格式错误，应为 是/1/真/t/y 或 否/0/假/f/n",
    )[1]
    if costom_pgb_enabled:

        base_style = ipt("基本样式组 (留空默认)：")
        if base_style:
            style.set_base_style(base_style)
        yet_part = ipt("未播放样式 (留空默认)：")
        if yet_part:
            style.set_to_play_style(yet_part)
        done_part = ipt("已播放样式 (留空默认)：")
        if done_part:
            style.set_played_style(done_part)
else:
    style = None

if output_file_format == 0:
    if player_format == 1:
        cvt_method = to_addon_pack_in_score
    elif player_format == 0:
        cvt_method = to_addon_pack_in_delay
    elif player_format == 2:
        cvt_method = to_addon_pack_in_repeater

elif output_file_format == 2:
    if player_format == 1:
        cvt_method = to_mcstructure_file_in_score
    if player_format == 0:
        cvt_method = to_mcstructure_file_in_delay
    elif player_format == 2:
        cvt_method = to_mcstructure_file_in_repeater


for singleMidi in midis:
    prt("\n" f"正在处理 {singleMidi}")
    cvt_mid = Musicreater.MidiConvert.from_midi_file(
        midi_file_path=singleMidi,
        play_speed=prompts[0],
        old_exe_format=old_exe_enabled,
        min_volume=prompts[1],
    )

    conversion_result = (
        (cvt_method(cvt_mid, out_path, style, *prompts[3:]))  # type: ignore
        if output_file_format == 0
        else (
            (
                to_BDX_file_in_score(cvt_mid, out_path, style, *prompts[3:])
                if player_format == 1
                else to_BDX_file_in_delay(cvt_mid, out_path, style, *prompts[3:])
            )
            if output_file_format == 1
            else (cvt_method(cvt_mid, out_path, *prompts[2:]))  # type: ignore
        )
    )

    prt(
        "\t{}：{}，播放刻数：{}{}".format(
            "结构大小" if output_file_format == 2 else "指令总长",
            conversion_result[0],
            conversion_result[1],
            (
                "，结构大小：{}，末点坐标：{}".format(*conversion_result[2:])
                if output_file_format == 1
                else ""
            ),
        )
    )

exitSth = ipt("结束。换行以退出程序。")
if exitSth == "record":
    import json

    with open("./demo_config.json", "w", encoding="utf-8") as f:
        json.dump(prompts, f)
elif exitSth == "delrec":
    os.remove("./demo_config.json")
