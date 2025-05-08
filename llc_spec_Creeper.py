# -*- coding: utf-8 -*-

# 伶伦 开发交流群 861684859


"""
伶伦转换器暨模组特用奇巧
Linglun Converter for Special Use with addons

版权所有 © 2025 金羿
Copyright © 2025 EillesWan

伶伦转换器暨模组特用奇巧版本（“本项目”）的协议颁发者为 金羿
The Licensor of _Linglun Converter for Special Use with addons_("this project") is Eilles Wan.

本项目根据 汉钰律许可协议，第一版（“本协议”）授权。
任何人皆可从以下地址获得本协议副本：https://gitee.com/EillesWan/YulvLicenses。
若非因法律要求或经过了特殊准许，此作品在根据本协议“原样”提供的基础上，不予提供任何形式的担保、任何明示、任何暗示或类似承诺。也就是说，用户将自行承担因此作品的质量或性能问题而产生的全部风险。
详细的准许和限制条款请见原协议文本。
"""

__version__ = "0.0.1"

import json
import os
import sys

from rich.table import Table

import Musicreater
from Musicreater.constants import MIDI_PITCH_NAME_TABLE, PERCUSSION_INSTRUMENT_LIST
from utils.io import *

osc.project_name = "伶伦暨模组特用奇巧"
osc.version = __version__


if len(sys.argv) > 0:

    def go_for_args(debugMode: str = "False", logfile: str = "True"):
        global logger
        osc.isRelease = False if debugMode.lower() in ("true", "1") else True
        logger.printing = not osc.isRelease
        logger.writing = True if logfile.lower() in ("true", "1") else False

    go_for_args(*sys.argv)


# 显示大标题

MainConsole.print(
    "[#121110 on #F0F2F4]     ",
    style="#121110 on #F0F2F4",
    justify="center",
)
MainConsole.rule(
    title="[bold #AB70FF]欢迎使用{}".format(osc.project_name),
    characters="=",
    style="#26E2FF",
)
# MainConsole.rule(title="[bold #AB70FF]Welcome to Linglun Converter", characters="-")
MainConsole.rule(
    title="[#AB70FF]版本{} | 音·创内核版本{}".format(
        __version__, Musicreater.__version__
    ),
    characters="-",
    style="#26E2FF",
)
MainConsole.print(
    "[#121110 on #F0F2F4]     ",
    style="#121110 on #F0F2F4",
    justify="center",
)


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


# percussion_only = format_ipt(
#     "仅处理打击乐器 (否/0|是/1)：", bool_str, "输入内容格式错误，应为 是/1/真/t/y 或 否/0/假/f/n"
# )[1]

speed: float = format_ipt("播放速度", float_str, "错误，需要浮点型数据；请重新输入。")[
    1
]


final_result: Dict[str, Dict[int, List[Tuple[str, int, str]]]] = {}

for single_midi in midis:
    fn = os.path.splitext(os.path.split(single_midi)[-1])[0]
    midi_cvt = Musicreater.MidiConvert.from_midi_file(
        single_midi,
    )
    midi_cvt.to_music_channels()

    max_delay = 0
    instrument_ID = -1
    total_track = {}
    instriments = {}

    # 此处 我们把通道视为音轨
    for i in midi_cvt.channels.keys():
        # 如果当前通道为空 则跳过
        if not midi_cvt.channels[i]:
            continue

        # 第十通道是打击乐通道
        SpecialBits = True if i == 9 else False

        for track_no, track in midi_cvt.channels[i].items():
            for msg in track:
                if msg[0] == "PgmC":
                    instrument_ID = msg[1]

                if msg[0] == "NoteS":
                    soundID, _X = (
                        midi_cvt.perc_inst_to_soundID_withX(msg[1])
                        if SpecialBits
                        else midi_cvt.inst_to_souldID_withX(instrument_ID)
                    )
                    score_now = round(msg[-1] / float(speed) / 50)
                    max_delay = max(max_delay, score_now)
                    mc_pitch = "" if SpecialBits else 2 ** ((msg[1] - 60 - _X) / 12)
                    try:
                        total_track[score_now].append(
                            (MIDI_PITCH_NAME_TABLE[msg[1]], mc_pitch, soundID),
                        )
                    except (IndexError, KeyError):
                        total_track[score_now] = [
                            (MIDI_PITCH_NAME_TABLE[msg[1]], mc_pitch, soundID),
                        ]

                    try:
                        instriments[soundID] += 1
                    except (IndexError, KeyError):
                        instriments[soundID] = 1

    del midi_cvt

    table = Table(
        *instriments.keys(),
        title="[bold #AB70FF on #121110]{} 乐器统计".format(fn),
        title_style="#26E2FF on #121110",
    )
    table.add_row(*[str(i) for i in instriments.values()])

    MainConsole.print(
        "[bold #8B50DF on #F0F2F4]-={}=-".format(fn),
        style="#AB70FF on #F0F2F4",
        justify="center",
    )

    prt(table)

    inst_selected: Set[str] = format_ipt(
        """请选择需要保留的乐器；以空格作分割；以 percussion 表示全部打击乐器|以 pitched 表示全部乐音乐器|以 all 表示所有乐器\n：""",
        lambda x: set(
            [
                i.lower()
                for i in x.split(" ")
                if isin(
                    i,
                    {
                        True: (
                            list(instriments.keys()) + ["all", "pitched", "percussion"]
                        )
                    },
                )
            ]
        ),
        "输入错误，需要在已有的乐器范围之内。",
        strict_mode=True,
    )[1]

    if "all" in inst_selected:
        inst_selected.remove("all")
        for i in instriments.keys():
            inst_selected.add(i)

    if "percussion" in inst_selected:
        inst_selected.remove("percussion")
        for i in instriments.keys():
            if i in PERCUSSION_INSTRUMENT_LIST:
                inst_selected.add(i)

    if "pitched" in inst_selected:
        inst_selected.remove("pitched")
        for i in instriments.keys():
            if i not in PERCUSSION_INSTRUMENT_LIST:
                inst_selected.add(i)

    result_piece = []
    for i, ele in total_track.items():
        this_ele = [k for k in ele if k[-1] in inst_selected]
        if this_ele:
            result_piece.append((i, this_ele))

    result_piece.sort(key=lambda x: x[0])

    final_result[fn] = {}
    for ind, ele in result_piece:
        final_result[fn][ind - result_piece[0][0]] = ele

    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(
            final_result,
            f,
            ensure_ascii=False,
            indent=3,
            sort_keys=True,
        )
