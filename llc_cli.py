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

__version__ = "0.0.3"

import datetime
import os
import random
import sys

import Musicreater
from Musicreater.plugin import ConvertConfig
from Musicreater.plugin.bdxfile import to_BDX_file_in_delay, to_BDX_file_in_score
from Musicreater.plugin.funcpack import to_function_addon_in_score
from Musicreater.plugin.mcstructpack import to_mcstructure_addon_in_delay
# from Musicreater.plugin.mcstructure import commands_to_structure, commands_to_redstone_delay_structure

from utils.io import *
from languages.lang import languages

print("小贴：不妨试试Mid-BDX转换网页：在线的多功能Midi转换器")
print("https://dislink.github.io/midi2bdx/")

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
MainConsole.rule(title="[#AB70FF]版本{} | 音·创内核版本{}".format(__version__,Musicreater.__version__), characters="=", style="#26E2FF")

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


def format_ipt(
    notice: str,
    fun,
    err_note: str = f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}",
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
    midi_path = ipt(f"{_('ChoosePath')}{_(':')}").lower()
    if os.path.exists(midi_path):
        if os.path.isfile(midi_path):
            midis = (midi_path,)
        elif os.path.isdir(midi_path):
            midis = tuple(
                (
                    os.path.join(midi_path, i)
                    for i in os.listdir(midi_path)
                    if i.lower().endswith(".mid") or i.lower().endswith(".midi")
                )
            )
        else:
            prt(f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}")
            continue
    else:
        prt(f"{_('FileNotFound')}{_(',')}{_('Re-Enter')}{_('.')}")
        continue
    break

# 获取输出地址
out_path = format_ipt(
    f"{_('ChooseOutPath')}{_(':')}",
    os.path.exists,
    f"{_('FileNotFound')}{_(',')}{_('Re-Enter')}{_('.')}",
)[0].lower()


# 选择输出格式


def is_in_bdx_mcpack(sth: str):
    if sth.lower() in ("0", "mcpack"):
        return 0

    elif sth.lower() in ("1", "bdx"):
        return 1

    else:
        raise ValueError("文件格式字符串啊？")


fileFormat = format_ipt(
    f"{_('ChooseFileFormat')}{_(':')}",
    is_in_bdx_mcpack,
    f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}",
)[1]


def is_in_player(sth: str):
    if sth.lower() in ("0", "延迟", "delay"):
        return 0
    elif sth.lower() in ("1", "计分板", "scoreboard"):
        return 1
    else:
        raise ValueError("播放器字符串啊？")


playerFormat = format_ipt(
    f"{_('ChoosePlayer')}{_(':')}",
    is_in_player,
    f"{_('ErrEnter')}{_(',')}{_('Re-Enter')}{_('.')}",
)[1]


# 真假字符串判断
def bool_str(sth: str) -> bool:
    try:
        return bool(int(sth))
    except ValueError:
        if str(sth).lower() in ("true", "真", "是"):
            return True
        elif str(sth).lower() == ("false", "假", "否", "非"):
            return False
        else:
            raise ValueError("布尔字符串啊？")


if os.path.exists("./demo_config.json"):
    import json

    prompts = json.load(open("./demo_config.json", "r", encoding="utf-8"))
    
    prompts = prompts[:-1]
else:
    prompts = []
    # 提示语 检测函数 错误提示语
    for args in [
        (
            f'{_("EnterVolume")}{_(":")}',
            float,
        ),
        (
            f'{_("EnterSpeed")}{_(":")}',
            float,
        ),
        (
            f'{_("WhetherPgb")}{_(":")}',
            bool_str,
        ),
        (
            f'{_("EnterSbName")}{_(":")}',
            str,
        )
        if playerFormat == 1
        else (
            f'{_("EnterSelecter")}{_(":")}',
            str,
        ),
        (
            f'{_("WhetherSbReset")}{_(":")}',
            bool_str,
        )
        if playerFormat == 1
        else (),
        (
            f'{_("EnterAuthor")}{_(":")}',
            str,
        )
        if fileFormat == 1
        else (),
        (
            f'{_("EnterMaxHeight")}{_(":")}',
            int,
        )
        if playerFormat == 0
        else (),
    ]:
        if args:
            prompts.append(format_ipt(*args)[1])


for singleMidi in midis:
    prt("\n" f"{_('Dealing')} {singleMidi} {_(':')}")
    cvt_mid = Musicreater.MidiConvert.from_midi_file(singleMidi, old_exe_format=False)
    cvt_cfg = ConvertConfig(out_path, *prompts[:3])
    
    conversion_result = ((
                to_function_addon_in_score(cvt_mid, cvt_cfg, *prompts[3:])
                if playerFormat == 1
                else to_mcstructure_addon_in_delay(cvt_mid, cvt_cfg, *prompts[3:])
            )if fileFormat == 0
        else (
                to_BDX_file_in_score(cvt_mid, cvt_cfg, *prompts[3:])
                if playerFormat == 1
                else to_BDX_file_in_delay(cvt_mid, cvt_cfg, *prompts[3:])
            ))

    prt(
            f"	{_('CmdLength')}{_(':')}{conversion_result[0]}{_(',')}{_('MaxDelay')}{_(':')}{conversion_result[1]}{f'''{_(',')}{_('PlaceSize')}{_(':')}{conversion_result[2]}{_(',')}{_('LastPos')}{_(':')}{conversion_result[3]}''' if fileFormat == 1 else ''}"
        )

exitSth = ipt(_("PressEnterExit")).lower()
if exitSth == "record":
    import json

    with open("./demo_config.json", "w", encoding="utf-8") as f:
        json.dump(prompts, f)
elif exitSth == "delrec":
    os.remove("./demo_config.json")
