# -*- coding:utf-8 -*-
'''对于伶伦的语言支持兼语言文件编辑器'''

"""
Copyright © 2023 all the developers of LinglunStudio
"""

from utils.io import *


DEFAULTLANGUAGE = 'ZH-CN'

LANGUAGELIST = {
    # 第一个是语言的中文名称和地区
    # 第二个是语言的英文名称和地区
    # 第三个是语言的本地名称和地区
    'ZH-CN': (
        "简体中文 中国大陆",
        "Simplified Chinese - China Mainland",
        "简体中文 中国大陆",
    ),
    'ZH-TW': (
        "繁体中文 中国台湾省",
        "Traditional Chinese - Taiwan Province, China",
        "正體中文,中国台灣省",
    ),
    # 'ZH-HK': (
    #     "繁体中文 香港",
    #     "Traditional Chinese - Hong Kong SAR",
    #     "繁體中文,香港特別行政區",
    # ),
    # 'ZH-MO': (
    #     "繁体中文 澳门",
    #     "Traditional Chinese - Macau SAR",
    #     "繁體中文,澳門特別行政區",
    # ),
    'EN-GB': (
        "英语 英国",
        "British English - the United Kingdom",
        "British English - the United Kingdom",
    ),
    'ZH-ME' : (
        "喵喵文 中国大陆",
        "Meow Catsnese - China Mainland"
        "喵喵喵~ 种花家~"
    )
}


languages = {
    "ZH-CN": {
        "MSCT": "音·创",
        "ChooseLang": "选择语言",
        "LangChd": "当前语言已经切换为",
        "ZH-CN": "简体中文",
        "ZH-TW": "繁体中文（台湾）",
        "EN-GB": "英语（英国）",
        "EN-US": "英语（美国）",
        ":": "：",
        ",": "，",
        ".": "。",
        "ChoosePath": "请输入MIDI路径或所在文件夹",
        "ChooseFileFormat": "请输入输出格式[BDX(1) 或 MCPACK(0)]",
        "EnterMethod": "请输入转换算法[{}~{}]",
        "MethodRangeErr": "输入的转换算法应为 [{},{}]（首尾皆含）之间的一个整数。",
        "ChoosePlayer": "请选择播放方式[计分板(1) 或 延迟(0)]",
        "WhetherArgEntering": "是否为文件夹内文件的转换统一参数[是(1) 或 否(0)]",
        "EnterArgs": "请输入转换参数",
        "noteofArgs": "注：文件夹内的全部midi将统一以此参数转换",
        "EnterVolume": "请输入音量大小(0~1)",
        "EnterSpeed": "请输入速度倍率",
        "WhetherPgb": "是否自动生成进度条[是(1) 或 否(0)]",
        "WhetherCstmProgressBar": "是否自定义进度条[是(1) 或 否(0)]",
        "EnterProgressBarStyle": "请输入进度条样式",
        "EnterSbName": "请输入计分板名称",
        "EnterSelecter": "请输入播放者选择器",
        "WhetherSbReset": "是否自动重置计分板[是(1) 或 否(0)]",
        "EnterAuthor": "请输入作者",
        "EnterMaxHeight": "请输入指令结构最大生成高度",
        "ErrEnter": "输入错误",
        "Re-Enter": "请重新输入",
        "Dealing": "正在处理",
        "FileNotFound": "文件(夹)不存在",
        "ChooseOutPath": "请输入结果输出路径",
        "Saying": "言·论",
        "Failed": "失败",
        "CmdLength": "指令数量",
        "MaxDelay": "曲目时间(游戏刻)",
        "PlaceSize": "结构占用大小",
        "LastPos": "最末方块坐标",
        "PressEnterExit": "请按下回车键退出。",
    }
}

def passbt():

    def __loadLanguage(languageFilename: str):
        with open(languageFilename, 'r', encoding='utf-8') as languageFile:
            _text = {}
            for line in languageFile:
                if line.startswith('#'):
                    continue
                line = line.split(' ', 1)
                _text[line[0]] = line[1].replace('\n', '')
        langkeys = _text.keys()
        with open(languageFilename.replace(languageFilename[-10:-5], 'ZH-CN'), 'r', encoding='utf-8') as defaultLangFile:
            for line in defaultLangFile:
                if line.startswith('#'):
                    continue
                line = line.split(' ', 1)
                if not line[0] in langkeys:
                    _text[line[0]] = line[1].replace('\n', '')
                    logger.warning(f'丢失对于 {line[0]} 的本地化文本',)
                    langkeys = _text.keys()
        # print(_text)
        return _text



    if DEFAULTLANGUAGE in LANGUAGELIST.keys():
        _TEXT = __loadLanguage('./languages/' + DEFAULTLANGUAGE + '.lang')
    else:
        logger.error(f"无法打开当前本地化文本{DEFAULTLANGUAGE}")
        raise KeyError(f'无法打开默认语言{DEFAULTLANGUAGE}')


    def wordTranslate(singleWord: str, debug: bool = False):
        try:
            return \
                requests.post('https://fanyi.baidu.com/sug', data={'kw': f'{singleWord}'}).json()['data'][0]['v'].split(
                    '; ')[0]
        except:
            logger.warning(f"无法翻译文本{singleWord}",)
            return None


    def _(text: str, debug: bool = False):
        try:
            return _TEXT[text]
        except:
            if debug:
                raise KeyError(f'无法找到本地化文本{text}')
            else:
                logger.warning(f'无法找到本地化文本{text}',)
                return ''


