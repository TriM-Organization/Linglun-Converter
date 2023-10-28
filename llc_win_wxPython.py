# -*- coding: utf-8 -*-

# 导入所需库
import datetime
import os
import random
import sys
import urllib.error
import urllib.request


import Musicreater
from Musicreater.constants import DEFAULT_PROGRESSBAR_STYLE
from Musicreater.plugin import ConvertConfig
from Musicreater.plugin.addonpack import (
    to_addon_pack_in_delay,
    to_addon_pack_in_repeater,
    to_addon_pack_in_score,
)
from Musicreater.plugin.bdxfile import to_BDX_file_in_delay, to_BDX_file_in_score

# import TrimLog
import wx

# from TrimLog import Console, object_constants

# from utils.io import prt

# is_logging: bool = True

# osc = object_constants.ObjectStateConstant()
# logger = TrimLog.Logger(
#     is_logging=is_logging,
#     printing=not osc.isRelease,
#     in_suffix=".llc",
# )

WHITE = (242, 244, 246)  # F2F4F6
BLACK = (18, 17, 16)  # 121110

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
    # logger.warning(f"读取言·论信息发生 互联网连接 错误：\n{E}")
    myWords = ["以梦想为驱使 创造属于自己的未来"]
# noinspection PyBroadException
except BaseException as E:
    # logger.warning(f"读取言·论信息发生 未知 错误：\n{E}")
    myWords = ["灵光焕发 深艺献心"]

__appname__ = "伶伦转换器"
__version__ = "WXGUI 0.0.2"


yanlun_length = len(myWords)


# 创建应用程序类
class LinglunConverterApp(wx.App):
    def OnInit(self):
        # 创建主窗口
        self.SetAppName(__appname__)
        self.frame = LingLunMainFrame(
            None,
        )
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


class LingLunMainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="{} {}".format(__appname__, __version__),
            pos=wx.DefaultPosition,
            size=wx.Size(660, 780),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans R",
            )
        )
        self.SetForegroundColour(BLACK)
        self.SetBackgroundColour(WHITE)

        self.m_statusBar2 = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)
        self.m_menubar1 = wx.MenuBar(0)
        self.FileMenu = wx.Menu()
        self.m_Exit_menuItem1 = wx.MenuItem(
            self.FileMenu, wx.ID_ANY, "退出", "这是退出按钮", wx.ITEM_NORMAL
        )
        self.FileMenu.Append(self.m_Exit_menuItem1)

        self.m_menubar1.Append(self.FileMenu, "文件")

        self.SetMenuBar(self.m_menubar1)

        m_mainBoxSizer = wx.BoxSizer(wx.VERTICAL)

        s_yanLunbarSizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "言·论"), wx.VERTICAL
        )

        self.yanlun_now = random.randrange(0, yanlun_length)
        self.m_LinglunWords_staticText1 = wx.StaticText(
            s_yanLunbarSizer.GetStaticBox(),
            wx.ID_ANY,
            myWords[self.yanlun_now] + "\r",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL | wx.ST_ELLIPSIZE_MIDDLE | wx.ST_NO_AUTORESIZE,
        )
        self.m_LinglunWords_staticText1.Wrap(-1)

        self.m_LinglunWords_staticText1.SetFont(
            wx.Font(
                12,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans B",
            )
        )
        self.m_LinglunWords_staticText1.SetForegroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT)
        )
        self.m_LinglunWords_staticText1.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT)
        )

        s_yanLunbarSizer.Add(self.m_LinglunWords_staticText1, 0, wx.EXPAND, 5)

        m_mainBoxSizer.Add(
            s_yanLunbarSizer,
            1,
            wx.ALL | wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.TOP,
            2,
        )

        s_midiChooseSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_ChooseMidiTips_staticText3 = wx.StaticText(
            self, wx.ID_ANY, "选择MIDI文件\n（双击移除）", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_ChooseMidiTips_staticText3.Wrap(-1)

        s_midiChooseSizer.Add(
            self.m_ChooseMidiTips_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5
        )

        ss_MidiChooserSizer_bSizer9 = wx.BoxSizer(wx.VERTICAL)

        self.midiFilesList = set()
        self.m_midiFilesList_listBox2 = wx.ListBox(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            [],
            wx.LB_HSCROLL | wx.LB_SORT,
        )
        ss_MidiChooserSizer_bSizer9.Add(self.m_midiFilesList_listBox2, 0, wx.EXPAND, 0)

        s_midiChooseSizer.Add(ss_MidiChooserSizer_bSizer9, 1, wx.EXPAND, 5)

        self.m_midiBroseButton_button21 = wx.Button(
            self, wx.ID_ANY, "打开…", wx.DefaultPosition, wx.DefaultSize, 0
        )
        s_midiChooseSizer.Add(
            self.m_midiBroseButton_button21, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5
        )

        m_mainBoxSizer.Add(s_midiChooseSizer, 1, wx.EXPAND, 5)

        s_formatChooseSizer = wx.BoxSizer(wx.HORIZONTAL)

        ss_outputFormatChooseSizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "选择输出格式"), wx.VERTICAL
        )

        m_outformatChoice_choice1Choices = ["附加包", "BDX结构"]
        self.m_outformatChoice_choice1 = wx.Choice(
            ss_outputFormatChooseSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            m_outformatChoice_choice1Choices,
        )
        self.m_outformatChoice_choice1.SetSelection(0)
        ss_outputFormatChooseSizer.Add(
            self.m_outformatChoice_choice1, 0, wx.ALL | wx.EXPAND, 5
        )

        s_formatChooseSizer.Add(ss_outputFormatChooseSizer, 1, wx.ALL | wx.EXPAND, 5)

        ss_playerChooseSizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "选择播放器"), wx.VERTICAL
        )

        m_playerChoice_choice2Choices = ["计分板", "延时", "中继器"]
        self.m_playerChoice_choice2 = wx.Choice(
            ss_playerChooseSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            m_playerChoice_choice2Choices,
            0,
        )
        self.m_playerChoice_choice2.SetSelection(0)
        ss_playerChooseSizer.Add(self.m_playerChoice_choice2, 0, wx.ALL | wx.EXPAND, 5)

        s_formatChooseSizer.Add(ss_playerChooseSizer, 1, wx.ALL | wx.EXPAND, 5)

        m_mainBoxSizer.Add(s_formatChooseSizer, 1, wx.EXPAND, 5)

        s_promptSizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "转换参数"), wx.VERTICAL
        )

        ss_regularPromoptsEnteringSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        sss_VolumnPersentageEnteringSizer = wx.StaticBoxSizer(
            wx.StaticBox(s_promptSizer.GetStaticBox(), wx.ID_ANY, "音量大小"), wx.HORIZONTAL
        )

        self.m_volumn_slider = wx.Slider(
            sss_VolumnPersentageEnteringSizer.GetStaticBox(),
            wx.ID_ANY,
            1000,
            0,
            1000,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SL_HORIZONTAL,
        )
        sss_VolumnPersentageEnteringSizer.Add(self.m_volumn_slider, 0, wx.ALL, 5)

        self.m_volumn_spinCtrlDouble1 = wx.SpinCtrlDouble(
            sss_VolumnPersentageEnteringSizer.GetStaticBox(),
            wx.ID_ANY,
            "100",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER,
            0,
            100,
            100.000000,
            0.5,
        )
        self.m_volumn_spinCtrlDouble1.SetDigits(2)
        sss_VolumnPersentageEnteringSizer.Add(
            self.m_volumn_spinCtrlDouble1, 0, wx.ALL, 5
        )

        ss_regularPromoptsEnteringSizer1.Add(
            sss_VolumnPersentageEnteringSizer, 1, wx.ALL | wx.EXPAND, 5
        )

        sss_SpeedEnteringSizer = wx.StaticBoxSizer(
            wx.StaticBox(s_promptSizer.GetStaticBox(), wx.ID_ANY, "播放倍速"), wx.HORIZONTAL
        )

        self.m_speed_slider = wx.Slider(
            sss_SpeedEnteringSizer.GetStaticBox(),
            wx.ID_ANY,
            50,
            0,
            100,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SL_HORIZONTAL,
        )
        sss_SpeedEnteringSizer.Add(self.m_speed_slider, 0, wx.ALL, 5)

        self.m_speed_spinCtrlDouble = wx.SpinCtrlDouble(
            sss_SpeedEnteringSizer.GetStaticBox(),
            wx.ID_ANY,
            "1",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER,
            0.01,
            10,
            1,
            0.1,
        )
        self.m_speed_spinCtrlDouble.SetDigits(2)
        sss_SpeedEnteringSizer.Add(self.m_speed_spinCtrlDouble, 0, wx.ALL, 5)

        ss_regularPromoptsEnteringSizer1.Add(
            sss_SpeedEnteringSizer, 1, wx.ALL | wx.EXPAND, 5
        )

        self.m_oldExeFormatChecker_checkBox3 = wx.CheckBox(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "启用\n旧版\n执行\n指令\n格式",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        ss_regularPromoptsEnteringSizer1.Add(
            self.m_oldExeFormatChecker_checkBox3, 0, wx.SHAPED, 0
        )
        s_promptSizer.Add(ss_regularPromoptsEnteringSizer1, 1, wx.EXPAND | wx.SHAPED, 5)

        ss_progressbarCheckingSizer = wx.StaticBoxSizer(
            wx.StaticBox(s_promptSizer.GetStaticBox(), wx.ID_ANY, "进度条"), wx.HORIZONTAL
        )

        self.m_progressBarEnablingCheckBox1 = wx.CheckBox(
            ss_progressbarCheckingSizer.GetStaticBox(),
            wx.ID_ANY,
            "启用进度条",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_RIGHT,
        )
        self.m_progressBarEnablingCheckBox1.SetValue(True)
        ss_progressbarCheckingSizer.Add(
            self.m_progressBarEnablingCheckBox1, 0, wx.ALL, 5
        )

        sss_customProgressBarSizer_wSizer6 = wx.WrapSizer(
            wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS
        )

        ssss_basicProgressStylePattle_sbSizer9 = wx.StaticBoxSizer(
            wx.StaticBox(
                ss_progressbarCheckingSizer.GetStaticBox(), wx.ID_ANY, "基本样式组"
            ),
            wx.VERTICAL,
        )

        self.m_BasicProgressBarStyleEntering_textCtrl4 = wx.TextCtrl(
            ssss_basicProgressStylePattle_sbSizer9.GetStaticBox(),
            wx.ID_ANY,
            DEFAULT_PROGRESSBAR_STYLE[0],
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_LEFT | wx.TE_NO_VSCROLL,
        )
        ssss_basicProgressStylePattle_sbSizer9.Add(
            self.m_BasicProgressBarStyleEntering_textCtrl4, 0, wx.ALL | wx.EXPAND, 5
        )

        sss_customProgressBarSizer_wSizer6.Add(
            ssss_basicProgressStylePattle_sbSizer9, 1, wx.EXPAND, 5
        )

        ssss_UnplayedPartProgressbarPattle_sbSizer10 = wx.StaticBoxSizer(
            wx.StaticBox(
                ss_progressbarCheckingSizer.GetStaticBox(), wx.ID_ANY, "未播放之样式"
            ),
            wx.VERTICAL,
        )

        self.m_unplayedProgressbarStyleEntering_textCtrl5 = wx.TextCtrl(
            ssss_UnplayedPartProgressbarPattle_sbSizer10.GetStaticBox(),
            wx.ID_ANY,
            DEFAULT_PROGRESSBAR_STYLE[1][1],
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_LEFT | wx.TE_NO_VSCROLL,
        )
        ssss_UnplayedPartProgressbarPattle_sbSizer10.Add(
            self.m_unplayedProgressbarStyleEntering_textCtrl5, 0, wx.ALL, 5
        )

        sss_customProgressBarSizer_wSizer6.Add(
            ssss_UnplayedPartProgressbarPattle_sbSizer10, 1, wx.EXPAND, 5
        )

        ssss_PlayedPartProgressbarPattle_sbSizer11 = wx.StaticBoxSizer(
            wx.StaticBox(
                ss_progressbarCheckingSizer.GetStaticBox(), wx.ID_ANY, "已播放之样式"
            ),
            wx.VERTICAL,
        )

        self.m_playedProgressbarStyleEntering_textCtrl5 = wx.TextCtrl(
            ssss_PlayedPartProgressbarPattle_sbSizer11.GetStaticBox(),
            wx.ID_ANY,
            DEFAULT_PROGRESSBAR_STYLE[1][0],
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_LEFT | wx.TE_NO_VSCROLL,
        )
        ssss_PlayedPartProgressbarPattle_sbSizer11.Add(
            self.m_playedProgressbarStyleEntering_textCtrl5, 0, wx.ALL, 5
        )

        sss_customProgressBarSizer_wSizer6.Add(
            ssss_PlayedPartProgressbarPattle_sbSizer11, 1, wx.EXPAND, 5
        )

        ss_progressbarCheckingSizer.Add(
            sss_customProgressBarSizer_wSizer6, 1, wx.EXPAND, 5
        )

        s_promptSizer.Add(ss_progressbarCheckingSizer, 1, wx.EXPAND, 5)

        self.ss_HideAndSeekSizer_bSizer15 = wx.BoxSizer(wx.VERTICAL)

        self.sss_ScoreboardPlayerPromptsSizer_bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_EnterScoreboardNameTip_staticText4 = wx.StaticText(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "播放计分板名称",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_EnterScoreboardNameTip_staticText4.Wrap(-1)

        self.sss_ScoreboardPlayerPromptsSizer_bSizer7.Add(
            self.m_EnterScoreboardNameTip_staticText4, 0, wx.ALL, 5
        )

        self.m_ScoreboardNameEntering_textCtrl9 = wx.TextCtrl(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "mscplay",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_ScoreboardNameEntering_textCtrl9.SetMaxLength(10)
        self.sss_ScoreboardPlayerPromptsSizer_bSizer7.Add(
            self.m_ScoreboardNameEntering_textCtrl9, 0, wx.ALL, 5
        )

        self.m_staticline1 = wx.StaticLine(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.LI_HORIZONTAL,
        )
        self.m_staticline1.SetMinSize(wx.Size(2, -1))

        self.sss_ScoreboardPlayerPromptsSizer_bSizer7.Add(
            self.m_staticline1, 0, wx.ALL | wx.EXPAND, 5
        )

        self.m_IsAutoResetScoreboard_checkBox2 = wx.CheckBox(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "自动重置计分板",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_RIGHT,
        )
        self.sss_ScoreboardPlayerPromptsSizer_bSizer7.Add(
            self.m_IsAutoResetScoreboard_checkBox2, 0, wx.ALL, 5
        )

        self.ss_HideAndSeekSizer_bSizer15.Add(
            self.sss_ScoreboardPlayerPromptsSizer_bSizer7, 1, wx.SHAPED, 5
        )

        self.sss_StructurePlayerPromptsSizer_bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_PlayerSelectorEnteringTips_staticText41 = wx.StaticText(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "玩家选择器",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_PlayerSelectorEnteringTips_staticText41.Wrap(-1)

        self.sss_StructurePlayerPromptsSizer_bSizer8.Add(
            self.m_PlayerSelectorEnteringTips_staticText41, 0, wx.ALL, 5
        )

        m_PlayerSelectorEntering_comboBox1Choices = ["@a", "@p", "@e[type=player]"]
        self.m_PlayerSelectorEntering_comboBox1 = wx.ComboBox(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "@a",
            wx.DefaultPosition,
            wx.DefaultSize,
            m_PlayerSelectorEntering_comboBox1Choices,
            wx.CB_DROPDOWN | wx.TE_PROCESS_ENTER,
        )
        self.m_PlayerSelectorEntering_comboBox1.SetSelection(0)
        self.sss_StructurePlayerPromptsSizer_bSizer8.Add(
            self.m_PlayerSelectorEntering_comboBox1, 0, wx.ALL, 5
        )

        self.m_staticline2 = wx.StaticLine(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.LI_HORIZONTAL,
        )
        self.m_staticline2.SetMinSize(wx.Size(2, -1))

        self.sss_StructurePlayerPromptsSizer_bSizer8.Add(
            self.m_staticline2, 0, wx.ALL | wx.EXPAND, 5
        )

        self.StructureMaxHeoghtTips_ = wx.StaticText(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "结构生成最大高度",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.StructureMaxHeoghtTips_.Wrap(-1)

        self.sss_StructurePlayerPromptsSizer_bSizer8.Add(
            self.StructureMaxHeoghtTips_, 0, wx.ALL, 5
        )

        self.m_StructureHeight_slider7 = wx.Slider(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            50,
            3,
            1024,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SL_HORIZONTAL,
        )
        self.sss_StructurePlayerPromptsSizer_bSizer8.Add(
            self.m_StructureHeight_slider7, 0, wx.ALL, 5
        )

        self.m_enteringStructureMaxHeight_spinCtrl1 = wx.SpinCtrl(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "50",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.SP_ARROW_KEYS,
            3,
            1024,
            50,
        )
        self.sss_StructurePlayerPromptsSizer_bSizer8.Add(
            self.m_enteringStructureMaxHeight_spinCtrl1, 0, wx.ALL, 5
        )

        self.ss_HideAndSeekSizer_bSizer15.Add(
            self.sss_StructurePlayerPromptsSizer_bSizer8, 1, wx.SHAPED, 5
        )

        self.sss_BDXfileSignNameSizer_bSizer13 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_BDXfileSignNameTips_staticText8 = wx.StaticText(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "BDX作者署名",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_BDXfileSignNameTips_staticText8.Wrap(-1)

        self.sss_BDXfileSignNameSizer_bSizer13.Add(
            self.m_BDXfileSignNameTips_staticText8, 0, wx.ALL, 5
        )

        self.m_EnteringBDXfileSignName_textCtrl12 = wx.TextCtrl(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "UserYou",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.sss_BDXfileSignNameSizer_bSizer13.Add(
            self.m_EnteringBDXfileSignName_textCtrl12, 0, wx.ALL, 5
        )

        self.ss_HideAndSeekSizer_bSizer15.Add(
            self.sss_BDXfileSignNameSizer_bSizer13, 1, wx.SHAPED, 5
        )

        s_promptSizer.Add(self.ss_HideAndSeekSizer_bSizer15, 1, wx.EXPAND, 5)

        m_mainBoxSizer.Add(s_promptSizer, 1, wx.EXPAND, 5)

        s_StartSizer_sbSizer18 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "开始转换"), wx.HORIZONTAL
        )

        s_StartSizer_sbSizer18.SetMinSize(wx.Size(-1, 100))

        s_StartSizer_sbSizer18.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_button2 = wx.Button(
            s_StartSizer_sbSizer18.GetStaticBox(),
            wx.ID_ANY,
            "开始转换",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        s_StartSizer_sbSizer18.Add(self.m_button2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        m_mainBoxSizer.Add(
            s_StartSizer_sbSizer18,
            1,
            wx.ALL | wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
            5,
        )

        self.SetSizer(m_mainBoxSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(
            wx.EVT_MENU, self.onExitButtonPressed, id=self.m_Exit_menuItem1.GetId()
        )
        self.m_LinglunWords_staticText1.Bind(wx.EVT_LEFT_DCLICK, self.onYanlunDClicked)
        self.m_LinglunWords_staticText1.Bind(wx.EVT_MOUSEWHEEL, self.onYanlunWheeled)
        self.m_ChooseMidiTips_staticText3.Bind(wx.EVT_LEFT_DCLICK, self.MidiEasterEgg)

        self.m_midiFilesList_listBox2.Bind(wx.EVT_LISTBOX, self.onFileListUpdated)
        self.m_midiFilesList_listBox2.Bind(
            wx.EVT_LISTBOX_DCLICK, self.onFileDoubleClicked
        )
        self.m_midiBroseButton_button21.Bind(wx.EVT_BUTTON, self.openFile)

        self.m_outformatChoice_choice1.Bind(wx.EVT_CHOICE, self.onOutputFormatChosen)
        self.m_playerChoice_choice2.Bind(wx.EVT_CHOICE, self.onPlayerChosen)
        self.m_volumn_slider.Bind(wx.EVT_SCROLL, self.onVolumeScrolling)
        self.m_volumn_spinCtrlDouble1.Bind(
            wx.EVT_SPINCTRLDOUBLE, self.onVolumeSpinChanged
        )
        self.m_speed_slider.Bind(wx.EVT_SCROLL, self.onSpeedScrolling)
        self.m_speed_spinCtrlDouble.Bind(wx.EVT_SPINCTRLDOUBLE, self.onSpeedSpinChanged)
        self.m_progressBarEnablingCheckBox1.Bind(
            wx.EVT_CHECKBOX, self.onProgressbarChecked
        )
        self.m_BasicProgressBarStyleEntering_textCtrl4.Bind(
            wx.EVT_TEXT, self.onProgressbarBasicStyleUpdating
        )
        self.m_unplayedProgressbarStyleEntering_textCtrl5.Bind(
            wx.EVT_TEXT, self.onProgressbarUnplayedStyleUpdating
        )
        self.m_playedProgressbarStyleEntering_textCtrl5.Bind(
            wx.EVT_TEXT, self.onProgressbarPlayedStyleUpdating
        )
        self.m_ScoreboardNameEntering_textCtrl9.Bind(
            wx.EVT_TEXT, self.onScoreboredNameUpdating
        )
        self.m_IsAutoResetScoreboard_checkBox2.Bind(
            wx.EVT_CHECKBOX, self.onAutoResetScoreboardChecked
        )
        self.m_PlayerSelectorEntering_comboBox1.Bind(
            wx.EVT_TEXT, self.onPlayerSelectorUpdating
        )
        self.m_StructureHeight_slider7.Bind(
            wx.EVT_SCROLL, self.onStructureMaxHeightScrolling
        )
        self.m_enteringStructureMaxHeight_spinCtrl1.Bind(
            wx.EVT_SPINCTRL, self.onStructureMaxHeightSpinChanged
        )
        self.m_EnteringBDXfileSignName_textCtrl12.Bind(
            wx.EVT_TEXT, self.onBDXfileSignNameUpdating
        )
        self.m_button2.Bind(wx.EVT_BUTTON, self.onStartButtonPressed)

        # self.ss_HideAndSeekSizer_bSizer15.Hide(
        #     self.sss_BDXfileSignNameSizer_bSizer13
        # )
        # self.ss_HideAndSeekSizer_bSizer15.Hide(
        #     self.sss_StructurePlayerPromptsSizer_bSizer8
        # )

        self.m_EnteringBDXfileSignName_textCtrl12.Enable(False)

        self.m_PlayerSelectorEntering_comboBox1.Enable(False)
        self.m_StructureHeight_slider7.Enable(False)
        self.m_enteringStructureMaxHeight_spinCtrl1.Enable(False)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def onExitButtonPressed(self, event):
        self.Destroy()

    def onYanlunDClicked(self, event):
        self.yanlun_now = random.randrange(0, yanlun_length)
        self.m_LinglunWords_staticText1.SetLabelText(myWords[self.yanlun_now] + "\r")

    def onYanlunWheeled(self, event):
        if event.GetWheelRotation() < 0:
            self.yanlun_now -= 1
        else:
            self.yanlun_now += 1
        self.yanlun_now += (
            -yanlun_length
            if self.yanlun_now >= yanlun_length
            else (yanlun_length if self.yanlun_now < 0 else 0)
        )
        self.m_LinglunWords_staticText1.SetLabelText(myWords[self.yanlun_now] + "\r")

    def MidiEasterEgg(self, event):
        if "诸葛亮与八卦阵-山水千年" not in self.midiFilesList:
            self.midiFilesList.add("诸葛亮与八卦阵-山水千年")
            self.m_midiFilesList_listBox2.Append("诸葛亮与八卦阵-山水千年")

    def onFileListUpdated(self, event):
        # prt(self.m_ChooseMIDI_filePicker1.GetTextCtrl().Value)
        # self.midi_cvt = Musicreater.MidiConvert.from_midi_file(self.m_ChooseMIDI_filePicker1.GetLabel(),self.m_oldExeFormatChecker_checkBox3.GetValue())
        event.Skip()

    def onFileDoubleClicked(self, event):
        # print(self.m_midiFilesList_listBox2.Selection)
        self.midiFilesList.remove(self.m_midiFilesList_listBox2.GetStringSelection())
        # print(self.midiFilesList)
        self.m_midiFilesList_listBox2.Delete(self.m_midiFilesList_listBox2.Selection)

    def openFile(self, event):
        fileDialog = wx.FileDialog(
            None,
            message="选择MIDI文件",
            defaultDir="./",
            wildcard="MIDI 序列 (*.mid;*.midi)|*.mid;*.midi",
            style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_FILE_MUST_EXIST,
        )
        dialogResult = fileDialog.ShowModal()
        if dialogResult == wx.ID_OK:
            self.midiFilesList.update(fileDialog.GetPaths())
            self.m_midiFilesList_listBox2.Set(list(self.midiFilesList))

        fileDialog.Destroy()

    def onOutputFormatChosen(self, event):
        # 0: 附加包
        # 1: BDX
        # prt("选择中：",self.m_outformatChoice_choice1.GetSelection())
        if self.m_outformatChoice_choice1.GetSelection() == 0:
            self.m_EnteringBDXfileSignName_textCtrl12.Enable(False)
            if self.m_playerChoice_choice2.GetSelection() == 0:
                self.m_StructureHeight_slider7.Enable(False)
                self.m_enteringStructureMaxHeight_spinCtrl1.Enable(False)
            else:
                self.m_StructureHeight_slider7.Enable(True)
                self.m_enteringStructureMaxHeight_spinCtrl1.Enable(True)
        elif self.m_outformatChoice_choice1.GetSelection() == 1:
            self.m_EnteringBDXfileSignName_textCtrl12.Enable(True)
            self.m_enteringStructureMaxHeight_spinCtrl1.Enable(True)
            self.m_StructureHeight_slider7.Enable(True)

    def onPlayerChosen(self, event):
        # 0 计分板    1 延时    2中继器
        if self.m_playerChoice_choice2.GetSelection() == 0:
            self.m_PlayerSelectorEntering_comboBox1.Enable(False)
            self.m_StructureHeight_slider7.Enable(False)
            self.m_enteringStructureMaxHeight_spinCtrl1.Enable(False)
            self.m_ScoreboardNameEntering_textCtrl9.Enable(True)
            self.m_IsAutoResetScoreboard_checkBox2.Enable(True)
        else:
            self.m_PlayerSelectorEntering_comboBox1.Enable(True)
            self.m_StructureHeight_slider7.Enable(True)
            self.m_enteringStructureMaxHeight_spinCtrl1.Enable(True)
            self.m_ScoreboardNameEntering_textCtrl9.Enable(False)
            self.m_IsAutoResetScoreboard_checkBox2.Enable(False)

    def onVolumeScrolling(self, event):
        # prt(self.m_volumn_slider.Value)
        self.m_volumn_spinCtrlDouble1.SetValue(self.m_volumn_slider.Value / 10)

    def onVolumeSpinChanged(self, event):
        # prt(self.m_volumn_spinCtrlDouble1.Value)
        self.m_volumn_slider.SetValue(int(self.m_volumn_spinCtrlDouble1.Value * 10))

    def onSpeedScrolling(self, event):
        # prt(self.m_speed_slider.Value)
        if self.m_speed_slider.Value > 50:
            self.m_speed_spinCtrlDouble.SetValue(
                (self.m_speed_slider.Value * 9 - 400) / 50
            )
        else:
            self.m_speed_spinCtrlDouble.SetValue(
                (self.m_speed_slider.Value * 99 + 50) / 5000
            )

    def onSpeedSpinChanged(self, event):
        if self.m_speed_spinCtrlDouble.Value > 1:
            self.m_speed_slider.SetValue(
                int((self.m_speed_spinCtrlDouble.Value + 8) * 50 / 9)
            )
        else:
            self.m_speed_slider.SetValue(
                int((self.m_speed_spinCtrlDouble.Value - 0.01) * 5000 / 99)
            )

    def onProgressbarChecked(self, event):
        if self.m_progressBarEnablingCheckBox1.GetValue():
            self.m_BasicProgressBarStyleEntering_textCtrl4.Enable(True)
            self.m_unplayedProgressbarStyleEntering_textCtrl5.Enable(True)
            self.m_playedProgressbarStyleEntering_textCtrl5.Enable(True)
        else:
            self.m_BasicProgressBarStyleEntering_textCtrl4.Enable(False)
            self.m_unplayedProgressbarStyleEntering_textCtrl5.Enable(False)
            self.m_playedProgressbarStyleEntering_textCtrl5.Enable(False)

    def onProgressbarBasicStyleUpdating(self, event):
        event.Skip()

    def onProgressbarUnplayedStyleUpdating(self, event):
        event.Skip()

    def onProgressbarPlayedStyleUpdating(self, event):
        event.Skip()

    def onScoreboredNameUpdating(self, event):
        event.Skip()

    def onAutoResetScoreboardChecked(self, event):
        event.Skip()

    def onPlayerSelectorUpdating(self, event):
        event.Skip()

    def onStructureMaxHeightScrolling(self, event):
        self.m_enteringStructureMaxHeight_spinCtrl1.SetValue(
            self.m_StructureHeight_slider7.GetValue()
        )

    def onStructureMaxHeightSpinChanged(self, event):
        self.m_StructureHeight_slider7.SetValue(
            self.m_enteringStructureMaxHeight_spinCtrl1.GetValue()
        )

    def onBDXfileSignNameUpdating(self, event):
        event.Skip()

    def onStartButtonPressed(self, event):
        for file_name in self.m_midiFilesList_listBox2.GetStrings():
            if file_name == "诸葛亮与八卦阵-山水千年":
                mid_cvt = Musicreater.MidiConvert(
                    None, "山水千年", self.m_oldExeFormatChecker_checkBox3.GetValue()
                )
            else:
                mid_cvt = Musicreater.MidiConvert.from_midi_file(
                    file_name,
                    self.m_oldExeFormatChecker_checkBox3.GetValue(),
                )

            cvt_cfg = ConvertConfig(
                os.path.split(file_name)[0],
                self.m_volumn_spinCtrlDouble1.GetValue() / 100,
                self.m_speed_spinCtrlDouble.GetValue(),
                progressbar=(
                    self.m_BasicProgressBarStyleEntering_textCtrl4.GetValue(),
                    (
                        self.m_playedProgressbarStyleEntering_textCtrl5.GetValue(),
                        self.m_unplayedProgressbarStyleEntering_textCtrl5.GetValue(),
                    ),
                ),
            )

            # 0: 附加包
            # 1: BDX

            # 0 计分板    1 延时    2中继器
            if self.m_outformatChoice_choice1.GetSelection() == 0:
                if self.m_playerChoice_choice2.GetSelection() == 0:
                    cmd_num, total_delay = to_addon_pack_in_score(
                        mid_cvt,
                        cvt_cfg,
                        self.m_ScoreboardNameEntering_textCtrl9.GetValue(),
                        self.m_IsAutoResetScoreboard_checkBox2.GetValue(),
                    )
                elif self.m_playerChoice_choice2.GetSelection() == 1:
                    cmd_num, total_delay = to_addon_pack_in_delay(
                        mid_cvt,
                        cvt_cfg,
                        self.m_PlayerSelectorEntering_comboBox1.GetValue(),
                        self.m_enteringStructureMaxHeight_spinCtrl1.GetValue(),
                    )
                elif self.m_playerChoice_choice2.GetSelection() == 2:
                    cmd_num, total_delay = to_addon_pack_in_repeater(
                        mid_cvt,
                        cvt_cfg,
                        self.m_PlayerSelectorEntering_comboBox1.GetValue(),
                        self.m_enteringStructureMaxHeight_spinCtrl1.GetValue(),
                    )
                else:
                    wx.MessageDialog(
                        None, "你输入的播放器有误!", "错误", wx.YES_DEFAULT | wx.ICON_ERROR
                    ).ShowModal()
                    return
                wx.MessageDialog(
                    None,
                    "完成！\n指令数量：{}\n延迟总长：{}".format(cmd_num, total_delay),
                    "转换成功",
                    wx.YES_DEFAULT | wx.ICON_INFORMATION,
                ).ShowModal()
            elif self.m_outformatChoice_choice1.GetSelection() == 1:
                if self.m_playerChoice_choice2.GetSelection() == 0:
                    cmd_num, total_delay, size, final_pos = to_BDX_file_in_score(
                        midi_cvt=mid_cvt,
                        data_cfg=cvt_cfg,
                        scoreboard_name=self.m_ScoreboardNameEntering_textCtrl9.GetValue(),
                        auto_reset=self.m_IsAutoResetScoreboard_checkBox2.GetValue(),
                        author=self.m_EnteringBDXfileSignName_textCtrl12.GetValue(),
                        max_height=self.m_enteringStructureMaxHeight_spinCtrl1.GetValue(),
                    )
                elif self.m_playerChoice_choice2.GetSelection() == 1:
                    cmd_num, total_delay, size, final_pos = to_BDX_file_in_delay(
                        midi_cvt=mid_cvt,
                        data_cfg=cvt_cfg,
                        player=self.m_PlayerSelectorEntering_comboBox1.GetValue(),
                        author=self.m_EnteringBDXfileSignName_textCtrl12.GetValue(),
                        max_height=self.m_enteringStructureMaxHeight_spinCtrl1.GetValue(),
                    )
                else:
                    wx.MessageDialog(
                        None, "你输入的播放器有误!", "错误", wx.YES_DEFAULT | wx.ICON_ERROR
                    ).ShowModal()
                    return
                wx.MessageDialog(
                    None,
                    "{}\n\n完成！\n指令数量：{}\n延迟总长：{}\n结构大小：{}\n终点坐标：{}".format(
                        file_name, cmd_num, total_delay, size, final_pos
                    ),
                    "转换成功",
                    wx.YES_DEFAULT | wx.ICON_INFORMATION,
                ).ShowModal()


# 启动应用程序
if __name__ == "__main__":
    app = LinglunConverterApp()
    app.MainLoop()

    # input("按下回车退出……")
