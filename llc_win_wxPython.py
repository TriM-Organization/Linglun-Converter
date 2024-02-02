# -*- coding: utf-8 -*-

"""
伶伦转换器 WXGUI
Linglun Converter WxPython GUI

版权所有 © 2024 金羿 & 睿穆开发组
Copyright © 2024 EillesWan & TriM Org.

开源相关声明请见 ./License.md
Terms & Conditions: ./Lisense.md
"""


# 导入所需库
import os
import random
import sys

if sys.argv:
    if "-l" in sys.argv:
        pass  # 更换语言
    elif "--edit-lang" in sys.argv:
        from utils.localize import main

        main()
        exit()

import Musicreater
import Musicreater.experiment
from Musicreater.plugin import ConvertConfig
from Musicreater.plugin.addonpack import (
    to_addon_pack_in_delay,
    to_addon_pack_in_repeater,
    to_addon_pack_in_score,
)
from Musicreater.plugin.bdxfile import to_BDX_file_in_delay, to_BDX_file_in_score

import wx
import wx.xrc
import wx.propgrid as pg

from utils.io import myWords, logger, object_constants  # , TrimLog, is_logging
from utils.update_check import check_update
from utils.packdata import enpack_llc_pack, unpack_llc_pack

logger.info("注册全局变量……")


WHITE = (242, 244, 246)  # F2F4F6
BLACK = (18, 17, 16)  # 121110


__appname__ = "伶伦转换器"
__version__ = "WXGUI 1.0.0"
__zhver__ = "WX图形界面 初代预版第〇次修订"


yanlun_length = len(myWords)


# global pgb_style
# global on_exit_saving
# global ignore_midi_mismatch_error
# global convert_tables
# global convert_table_selection
# global ConvertClass

pgb_style: Musicreater.ProgressBarStyle = Musicreater.DEFAULT_PROGRESSBAR_STYLE.copy()
on_exit_saving: bool = True
ignore_midi_mismatch_error: bool = True
convert_tables = {
    "PITCHED": {
        "“偷吃”的对照表": Musicreater.MM_TOUCH_PITCHED_INSTRUMENT_TABLE,
        "“经典”对照表": Musicreater.MM_CLASSIC_PITCHED_INSTRUMENT_TABLE,
    },
    "PERCUSSION": {
        "“偷吃”的对照表": Musicreater.MM_TOUCH_PERCUSSION_INSTRUMENT_TABLE,
        "“经典”对照表": Musicreater.MM_CLASSIC_PERCUSSION_INSTRUMENT_TABLE,
    },
}
convert_table_selection = {
    "PITCHED": "“偷吃”的对照表",
    "PERCUSSION": "“偷吃”的对照表",
}
ConvertClass = (Musicreater.MidiConvert, "常规转换")

if os.path.isfile("save.llc.config"):
    unpacked_data = unpack_llc_pack("save.llc.config", False)
    if isinstance(unpacked_data, Exception):
        logger.warning("读取设置文件失败：{}；使用默认设置信息。")
    else:
        (
            pgb_style,
            on_exit_saving,
            ignore_midi_mismatch_error,
            convert_tables,
            convert_table_selection,
            ConvertClass,
        ) = unpacked_data


osc = object_constants.ObjectStateConstant(
    logging_project_name=__appname__,
    logging_project_version=__version__,
    logging_exit_exec=lambda sth: wx.MessageDialog(
        None, sth, "崩溃", wx.YES_DEFAULT | wx.ICON_STOP
    ).ShowModal(),
)
logger.printing = not osc.is_release


logger.info("加载窗口布局……")


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


logger.info("加载主框架……")


class LingLunMainFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title="{} {}".format(__appname__, __zhver__),
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
        self.m_statusBar2.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans R",
            )
        )

        self.m_menubar1 = wx.MenuBar(0)
        self.m_menubar1.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans R",
            )
        )

        self.FileMenu = wx.Menu()
        self.m_ClearSetting_menuItem2 = wx.MenuItem(
            self.FileMenu,
            wx.ID_ANY,
            "重置设置",
            "将全部数据设置重置为默认值（下次启动时生效）",
            wx.ITEM_CHECK,
        )
        self.FileMenu.Append(self.m_ClearSetting_menuItem2)

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

        self.m_LinglunWords_staticText1 = wx.StaticText(
            s_yanLunbarSizer.GetStaticBox(),
            wx.ID_ANY,
            "灵光焕发 深艺献心",
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
            0,
            wx.ALL | wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN | wx.TOP,
            2,
        )

        self.mian_notebook = wx.Notebook(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.mian_notebook.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans R",
            )
        )

        self.convert_page = ConvertPagePanel(
            self.mian_notebook,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        self.mian_notebook.AddPage(self.convert_page, "开始转换", True)
        self.setting_page = SettingPagePannel(
            self.mian_notebook,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        self.mian_notebook.AddPage(self.setting_page, "数据设置", False)

        m_mainBoxSizer.Add(self.mian_notebook, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(m_mainBoxSizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.Bind(
            wx.EVT_MENU,
            self.onResetSettingButtonSelection,
            id=self.m_ClearSetting_menuItem2.GetId(),
        )
        self.Bind(
            wx.EVT_MENU, self.onExitButtonPressed, id=self.m_Exit_menuItem1.GetId()
        )
        self.m_LinglunWords_staticText1.Bind(wx.EVT_LEFT_DCLICK, self.onYanlunDClicked)
        self.m_LinglunWords_staticText1.Bind(wx.EVT_MOUSEWHEEL, self.onYanlunWheeled)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def onResetSettingButtonSelection(self, event):
        global on_exit_saving
        if self.m_ClearSetting_menuItem2.IsChecked():
            on_exit_saving = False
        else:
            on_exit_saving = True

    def onExitButtonPressed(self, event):
        self.Destroy()

    def onYanlunDClicked(self, event):
        self.yanlun_now = random.randrange(0, yanlun_length)
        self.m_LinglunWords_staticText1.SetLabelText(myWords[self.yanlun_now] + "\r")

    def onYanlunWheeled(self, event):
        if event.GetWheelRotation() < 0:
            self.yanlun_now += 1
        else:
            self.yanlun_now -= 1
        self.yanlun_now += (
            -yanlun_length
            if self.yanlun_now >= yanlun_length
            else (yanlun_length if self.yanlun_now < 0 else 0)
        )
        self.m_LinglunWords_staticText1.SetLabelText(myWords[self.yanlun_now] + "\r")


logger.info("加载分页……")

###########################################################################
## Class convert_page_panel
###########################################################################


class ConvertPagePanel(wx.Panel):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.Size(565, 540),
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        wx.Panel.__init__(
            self, parent, id=id, pos=pos, size=size, style=style, name=name
        )

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        main_page_sizer = wx.BoxSizer(wx.VERTICAL)

        s_midiChooseSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.m_ChooseMidiTips_staticText3 = wx.StaticText(
            self,
            wx.ID_ANY,
            "选择MIDI文件\n（双击移除）",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
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

        main_page_sizer.Add(s_midiChooseSizer, 0, wx.EXPAND, 5)

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
            0,
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

        main_page_sizer.Add(s_formatChooseSizer, 0, wx.EXPAND, 5)

        s_promptSizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "转换参数"), wx.VERTICAL
        )

        ss_regularPromoptsEnteringSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        sss_VolumnPersentageEnteringSizer = wx.StaticBoxSizer(
            wx.StaticBox(s_promptSizer.GetStaticBox(), wx.ID_ANY, "音量大小"),
            wx.HORIZONTAL,
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
            sss_VolumnPersentageEnteringSizer,
            0,
            wx.ALL | wx.EXPAND | wx.SHAPED | wx.ALIGN_CENTER_VERTICAL,
            5,
        )

        sss_SpeedEnteringSizer = wx.StaticBoxSizer(
            wx.StaticBox(s_promptSizer.GetStaticBox(), wx.ID_ANY, "播放倍速"),
            wx.HORIZONTAL,
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
            sss_SpeedEnteringSizer,
            0,
            wx.ALL | wx.EXPAND | wx.SHAPED | wx.ALIGN_CENTER_VERTICAL,
            5,
        )

        s_promptSizer.Add(ss_regularPromoptsEnteringSizer1, 0, wx.EXPAND, 5)

        ss_commandCheckingSizer = wx.StaticBoxSizer(
            wx.StaticBox(s_promptSizer.GetStaticBox(), wx.ID_ANY, "指令设置"),
            wx.HORIZONTAL,
        )

        self.m_progressBarEnablingCheckBox1 = wx.CheckBox(
            ss_commandCheckingSizer.GetStaticBox(),
            wx.ID_ANY,
            "启用进度条",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        ss_commandCheckingSizer.Add(
            self.m_progressBarEnablingCheckBox1, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5
        )

        self.m_oldExeFormatChecker_checkBox3 = wx.CheckBox(
            ss_commandCheckingSizer.GetStaticBox(),
            wx.ID_ANY,
            "启用旧版执行指令格式",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        ss_commandCheckingSizer.Add(
            self.m_oldExeFormatChecker_checkBox3,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            5,
        )

        s_promptSizer.Add(ss_commandCheckingSizer, 0, wx.EXPAND, 5)

        ss_HideAndSeekSizer_bSizer15 = wx.BoxSizer(wx.VERTICAL)

        sss_ScoreboardPlayerPromptsSizer_bSizer7 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_EnterScoreboardNameTip_staticText4 = wx.StaticText(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "播放计分板名称",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_EnterScoreboardNameTip_staticText4.Wrap(-1)

        sss_ScoreboardPlayerPromptsSizer_bSizer7.Add(
            self.m_EnterScoreboardNameTip_staticText4,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            5,
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
        sss_ScoreboardPlayerPromptsSizer_bSizer7.Add(
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

        sss_ScoreboardPlayerPromptsSizer_bSizer7.Add(
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
        sss_ScoreboardPlayerPromptsSizer_bSizer7.Add(
            self.m_IsAutoResetScoreboard_checkBox2,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            5,
        )

        ss_HideAndSeekSizer_bSizer15.Add(
            sss_ScoreboardPlayerPromptsSizer_bSizer7, 0, wx.SHAPED | wx.EXPAND, 5
        )

        sss_StructurePlayerPromptsSizer_bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_PlayerSelectorEnteringTips_staticText41 = wx.StaticText(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "玩家选择器",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_PlayerSelectorEnteringTips_staticText41.Wrap(-1)

        sss_StructurePlayerPromptsSizer_bSizer8.Add(
            self.m_PlayerSelectorEnteringTips_staticText41,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            5,
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
        sss_StructurePlayerPromptsSizer_bSizer8.Add(
            self.m_PlayerSelectorEntering_comboBox1,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            5,
        )

        self.m_staticline2 = wx.StaticLine(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.LI_HORIZONTAL,
        )
        self.m_staticline2.SetMinSize(wx.Size(2, -1))

        sss_StructurePlayerPromptsSizer_bSizer8.Add(
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

        sss_StructurePlayerPromptsSizer_bSizer8.Add(
            self.StructureMaxHeoghtTips_, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5
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
        sss_StructurePlayerPromptsSizer_bSizer8.Add(
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
        sss_StructurePlayerPromptsSizer_bSizer8.Add(
            self.m_enteringStructureMaxHeight_spinCtrl1,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            5,
        )

        ss_HideAndSeekSizer_bSizer15.Add(
            sss_StructurePlayerPromptsSizer_bSizer8, 0, wx.SHAPED | wx.EXPAND, 5
        )

        sss_BDXfileSignNameSizer_bSizer13 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_BDXfileSignNameTips_staticText8 = wx.StaticText(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "BDX作者署名",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_BDXfileSignNameTips_staticText8.Wrap(-1)

        sss_BDXfileSignNameSizer_bSizer13.Add(
            self.m_BDXfileSignNameTips_staticText8,
            0,
            wx.ALL | wx.ALIGN_CENTER_VERTICAL,
            5,
        )

        self.m_EnteringBDXfileSignName_textCtrl12 = wx.TextCtrl(
            s_promptSizer.GetStaticBox(),
            wx.ID_ANY,
            "UserYou",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        sss_BDXfileSignNameSizer_bSizer13.Add(
            self.m_EnteringBDXfileSignName_textCtrl12, 0, wx.ALL, 5
        )

        ss_HideAndSeekSizer_bSizer15.Add(
            sss_BDXfileSignNameSizer_bSizer13, 0, wx.SHAPED | wx.EXPAND, 5
        )

        s_promptSizer.Add(ss_HideAndSeekSizer_bSizer15, 0, wx.EXPAND, 5)

        main_page_sizer.Add(
            s_promptSizer, 0, wx.SHAPED | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 5
        )

        s_StartSizer_sbSizer18 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "开始转换"), wx.HORIZONTAL
        )

        s_StartSizer_sbSizer18.SetMinSize(wx.Size(-1, 100))

        s_StartSizer_sbSizer18.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_start_button2 = wx.Button(
            s_StartSizer_sbSizer18.GetStaticBox(),
            wx.ID_ANY,
            "开始转换",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        s_StartSizer_sbSizer18.Add(self.m_start_button2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        main_page_sizer.Add(
            s_StartSizer_sbSizer18,
            1,
            wx.ALL | wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN,
            5,
        )

        self.SetSizer(main_page_sizer)
        self.Layout()

        # Connect Events
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
        self.m_start_button2.Bind(wx.EVT_BUTTON, self.onStartButtonPressed)

        self.m_EnteringBDXfileSignName_textCtrl12.Enable(False)

        self.m_PlayerSelectorEntering_comboBox1.Enable(False)
        self.m_StructureHeight_slider7.Enable(False)
        self.m_enteringStructureMaxHeight_spinCtrl1.Enable(False)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
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

            if self.m_outformatChoice_choice1.GetSelection() == 0:
                self.m_enteringStructureMaxHeight_spinCtrl1.Enable(False)
            elif self.m_outformatChoice_choice1.GetSelection() == 1:
                self.m_enteringStructureMaxHeight_spinCtrl1.Enable(True)

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
        pass
        # if self.m_progressBarEnablingCheckBox1.GetValue():
        #     self.m_BasicProgressBarStyleEntering_textCtrl4.Enable(True)
        #     self.m_unplayedProgressbarStyleEntering_textCtrl5.Enable(True)
        #     self.m_playedProgressbarStyleEntering_textCtrl5.Enable(True)
        # else:
        #     self.m_BasicProgressBarStyleEntering_textCtrl4.Enable(False)
        #     self.m_unplayedProgressbarStyleEntering_textCtrl5.Enable(False)
        #     self.m_playedProgressbarStyleEntering_textCtrl5.Enable(False)

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
        global pgb_style
        for file_name in self.m_midiFilesList_listBox2.GetStrings():
            if file_name == "诸葛亮与八卦阵-山水千年":
                mid_cvt = ConvertClass[0](
                    None,
                    "山水千年",
                    self.m_oldExeFormatChecker_checkBox3.GetValue(),
                    convert_tables["PITCHED"][convert_table_selection["PITCHED"]],
                    convert_tables["PERCUSSION"][convert_table_selection["PERCUSSION"]],
                )
            else:
                mid_cvt = ConvertClass[0].from_midi_file(
                    file_name,
                    self.m_oldExeFormatChecker_checkBox3.GetValue(),
                    convert_tables["PITCHED"][convert_table_selection["PITCHED"]],
                    convert_tables["PERCUSSION"][convert_table_selection["PERCUSSION"]],
                )

            cvt_cfg = ConvertConfig(
                os.path.split(file_name)[0],
                self.m_volumn_spinCtrlDouble1.GetValue() / 100,
                self.m_speed_spinCtrlDouble.GetValue(),
                progressbar=pgb_style,
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
                        None,
                        "你输入的播放器有误!",
                        "错误",
                        wx.YES_DEFAULT | wx.ICON_ERROR,
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
                        None,
                        "你输入的播放器有误!",
                        "错误",
                        wx.YES_DEFAULT | wx.ICON_ERROR,
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
            else:
                wx.MessageDialog(
                    None,
                    "你输入的输出格式有误!",
                    "错误",
                    wx.YES_DEFAULT | wx.ICON_ERROR,
                ).ShowModal()
                return


###########################################################################
## Class setting_page_pannel
###########################################################################


class SettingPagePannel(wx.Panel):
    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.Size(565, 540),
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        wx.Panel.__init__(
            self, parent, id=id, pos=pos, size=size, style=style, name=name
        )

        setting_page_sizer = wx.BoxSizer(wx.VERTICAL)

        self.setting_notebook = wx.Notebook(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.NB_FIXEDWIDTH | wx.NB_MULTILINE | wx.NB_RIGHT,
        )
        self.setting_notebook.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "@OPPOSans R",
            )
        )
        self.setting_notebook.SetBackgroundColour(
            wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW)
        )

        self.setting_page1 = wx.Panel(
            self.setting_notebook,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        self.setting_page1.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans R",
            )
        )

        setting_page1_box_sizer = wx.BoxSizer(wx.VERTICAL)

        sss_customProgressBarSizer_wSizer6 = wx.WrapSizer(
            wx.HORIZONTAL, wx.WRAPSIZER_DEFAULT_FLAGS
        )

        setting_page1_progressbar_style = wx.StaticBoxSizer(
            wx.StaticBox(self.setting_page1, wx.ID_ANY, "进度条"), wx.HORIZONTAL
        )

        ssss_basicProgressStylePattle_sbSizer9 = wx.StaticBoxSizer(
            wx.StaticBox(
                setting_page1_progressbar_style.GetStaticBox(), wx.ID_ANY, "基本样式组"
            ),
            wx.VERTICAL,
        )

        self.m_BasicProgressBarStyleEntering_textCtrl4 = wx.TextCtrl(
            ssss_basicProgressStylePattle_sbSizer9.GetStaticBox(),
            wx.ID_ANY,
            pgb_style.base_style,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_LEFT | wx.TE_NO_VSCROLL,
        )
        ssss_basicProgressStylePattle_sbSizer9.Add(
            self.m_BasicProgressBarStyleEntering_textCtrl4, 0, wx.ALL | wx.EXPAND, 5
        )

        setting_page1_progressbar_style.Add(
            ssss_basicProgressStylePattle_sbSizer9, 1, wx.ALL | wx.EXPAND, 5
        )

        ssss_UnplayedPartProgressbarPattle_sbSizer10 = wx.StaticBoxSizer(
            wx.StaticBox(
                setting_page1_progressbar_style.GetStaticBox(),
                wx.ID_ANY,
                "未播放之样式",
            ),
            wx.VERTICAL,
        )

        self.m_unplayedProgressbarStyleEntering_textCtrl5 = wx.TextCtrl(
            ssss_UnplayedPartProgressbarPattle_sbSizer10.GetStaticBox(),
            wx.ID_ANY,
            pgb_style.to_play_style,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_LEFT | wx.TE_NO_VSCROLL,
        )
        ssss_UnplayedPartProgressbarPattle_sbSizer10.Add(
            self.m_unplayedProgressbarStyleEntering_textCtrl5, 0, wx.ALL, 5
        )

        setting_page1_progressbar_style.Add(
            ssss_UnplayedPartProgressbarPattle_sbSizer10, 1, wx.ALL | wx.EXPAND, 5
        )

        ssss_PlayedPartProgressbarPattle_sbSizer11 = wx.StaticBoxSizer(
            wx.StaticBox(
                setting_page1_progressbar_style.GetStaticBox(),
                wx.ID_ANY,
                "已播放之样式",
            ),
            wx.VERTICAL,
        )

        self.m_playedProgressbarStyleEntering_textCtrl5 = wx.TextCtrl(
            ssss_PlayedPartProgressbarPattle_sbSizer11.GetStaticBox(),
            wx.ID_ANY,
            pgb_style.played_style,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_LEFT | wx.TE_NO_VSCROLL,
        )
        ssss_PlayedPartProgressbarPattle_sbSizer11.Add(
            self.m_playedProgressbarStyleEntering_textCtrl5, 0, wx.ALL, 5
        )

        setting_page1_progressbar_style.Add(
            ssss_PlayedPartProgressbarPattle_sbSizer11, 1, wx.ALL | wx.EXPAND, 5
        )

        sss_customProgressBarSizer_wSizer6.Add(
            setting_page1_progressbar_style, 1, wx.ALL | wx.EXPAND, 5
        )

        setting_page1_experiment_style = wx.StaticBoxSizer(
            wx.StaticBox(self.setting_page1, wx.ID_ANY, "实验性功能"), wx.HORIZONTAL
        )

        self.m_enable_experiment_checkBox = wx.CheckBox(
            setting_page1_experiment_style.GetStaticBox(),
            wx.ID_ANY,
            "启用实验性功能",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        setting_page1_experiment_style.Add(
            self.m_enable_experiment_checkBox,
            1,
            wx.ALL | wx.EXPAND,
            5,
        )

        experiment_type_choiceChoices = ["常规转换", "长音插值", "同刻偏移"]
        self.experiment_type_choice = wx.Choice(
            setting_page1_experiment_style.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            experiment_type_choiceChoices,
            0,
        )
        self.experiment_type_choice.SetSelection(
            experiment_type_choiceChoices.index(ConvertClass[1])
        )
        setting_page1_experiment_style.Add(
            self.experiment_type_choice,
            2,
            wx.ALL | wx.EXPAND,
            5,
        )

        self.m_ignore_midi_error_checkBox = wx.CheckBox(
            setting_page1_experiment_style.GetStaticBox(),
            wx.ID_ANY,
            "忽略MIDI错误",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_ignore_midi_error_checkBox.SetValue(ignore_midi_mismatch_error)
        setting_page1_experiment_style.Add(
            self.m_ignore_midi_error_checkBox, 1, wx.ALL, 5
        )

        sss_customProgressBarSizer_wSizer6.Add(
            setting_page1_experiment_style, 1, wx.ALL | wx.EXPAND, 5
        )

        setting_page1_box_sizer.Add(
            sss_customProgressBarSizer_wSizer6, 1, wx.ALL | wx.EXPAND, 5
        )

        self.setting_page1.SetSizer(setting_page1_box_sizer)
        self.setting_page1.Layout()
        setting_page1_box_sizer.Fit(self.setting_page1)
        self.setting_notebook.AddPage(self.setting_page1, "基本信息", True)
        self.setting_page2 = wx.Panel(
            self.setting_notebook,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        self.setting_page2.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                wx.EmptyString,
            )
        )

        setting_page2_box_sizer = wx.BoxSizer(wx.VERTICAL)

        self.m_pitched_instrument_table_choice = wx.Choice(
            self.setting_page2,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            list(convert_tables["PITCHED"].keys()),
            0,
        )
        self.m_pitched_instrument_table_choice.SetSelection(
            list(convert_tables["PITCHED"].keys()).index(
                convert_table_selection["PITCHED"]
            )
        )

        self.m_pitched_instrument_table_choice.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans R",
            )
        )

        setting_page2_box_sizer.Add(
            self.m_pitched_instrument_table_choice,
            0,
            wx.ALL | wx.EXPAND,
            5,
        )

        self.m_pitched_notes_table_propertyGrid1 = pg.PropertyGrid(
            self.setting_page2,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            pg.PG_BOLD_MODIFIED | pg.PG_DEFAULT_STYLE,
        )
        self.m_pitched_notes_table_propertyGrid1.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans R",
            )
        )

        for midi_inst, mc_inst_patern in convert_tables["PITCHED"][
            convert_table_selection["PITCHED"]
        ].items():
            self.m_pitched_notes_table_propertyGrid1.Append(
                pg.StringProperty(
                    Musicreater.MIDI_PITCHED_NOTE_NAME_TABLE[midi_inst + 1][0],
                    "pitched_inst_{}".format(midi_inst),
                    mc_inst_patern[0],
                )
            )

        setting_page2_box_sizer.Add(
            self.m_pitched_notes_table_propertyGrid1,
            1,
            wx.ALL | wx.EXPAND,
            5,
        )

        self.setting_page2.SetSizer(setting_page2_box_sizer)
        self.setting_page2.Layout()
        setting_page2_box_sizer.Fit(self.setting_page2)
        self.setting_notebook.AddPage(self.setting_page2, "乐音乐器对照表", False)
        self.setting_page3 = wx.Panel(
            self.setting_notebook,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        setting_page3_box_sizer = wx.BoxSizer(wx.VERTICAL)

        self.m_percussion_instrument_table_choice1 = wx.Choice(
            self.setting_page3,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            list(convert_tables["PERCUSSION"].keys()),
            0,
        )
        self.m_percussion_instrument_table_choice1.SetSelection(
            list(convert_tables["PERCUSSION"].keys()).index(
                convert_table_selection["PERCUSSION"]
            )
        )
        self.m_percussion_instrument_table_choice1.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans R",
            )
        )

        setting_page3_box_sizer.Add(
            self.m_percussion_instrument_table_choice1,
            0,
            wx.ALL | wx.EXPAND,
            5,
        )

        self.m_percussion_notes_table_propertyGrid11 = pg.PropertyGrid(
            self.setting_page3,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            pg.PG_BOLD_MODIFIED | pg.PG_DEFAULT_STYLE,
        )
        self.m_percussion_notes_table_propertyGrid11.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans R",
            )
        )

        for midi_inst, mc_inst_patern in convert_tables["PERCUSSION"][
            convert_table_selection["PERCUSSION"]
        ].items():
            self.m_percussion_notes_table_propertyGrid11.Append(
                pg.StringProperty(
                    Musicreater.MIDI_PERCUSSION_NOTE_NAME_TABLE[midi_inst + 1][0],
                    "percussion_inst_{}".format(midi_inst),
                    mc_inst_patern[0],
                )
            )

        setting_page3_box_sizer.Add(
            self.m_percussion_notes_table_propertyGrid11,
            1,
            wx.ALL | wx.EXPAND,
            5,
        )

        self.setting_page3.SetSizer(setting_page3_box_sizer)
        self.setting_page3.Layout()
        setting_page3_box_sizer.Fit(self.setting_page3)
        self.setting_notebook.AddPage(self.setting_page3, "打击乐器对照表", False)

        setting_page_sizer.Add(self.setting_notebook, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(setting_page_sizer)
        self.Layout()

        # Connect Events

        self.m_BasicProgressBarStyleEntering_textCtrl4.Bind(
            wx.EVT_TEXT, self.onProgressbarBasicStyleUpdating
        )
        self.m_unplayedProgressbarStyleEntering_textCtrl5.Bind(
            wx.EVT_TEXT, self.onProgressbarUnplayedStyleUpdating
        )
        self.m_playedProgressbarStyleEntering_textCtrl5.Bind(
            wx.EVT_TEXT, self.onProgressbarPlayedStyleUpdating
        )
        self.m_enable_experiment_checkBox.Bind(
            wx.EVT_CHECKBOX, self.onExperimentEnableUpdating
        )
        self.experiment_type_choice.Bind(wx.EVT_CHOICE, self.onConvertMethodUpdating)
        self.m_ignore_midi_error_checkBox.Bind(
            wx.EVT_CHECKBOX, self.onMidiFaultIgnoranceChecking
        )
        self.m_pitched_instrument_table_choice.Bind(
            wx.EVT_CHOICE, self.onPitchedInstListChanging
        )
        self.m_pitched_notes_table_propertyGrid1.Bind(
            pg.EVT_PG_CHANGED, self.onPitchedInstTableChanged
        )
        self.m_pitched_notes_table_propertyGrid1.Bind(
            pg.EVT_PG_CHANGING, self.onPitchedInstTableChanging
        )
        self.m_percussion_instrument_table_choice1.Bind(
            wx.EVT_CHOICE, self.onPercussionInstListChanging
        )
        self.m_percussion_notes_table_propertyGrid11.Bind(
            pg.EVT_PG_CHANGED, self.onPercussionInstTableChanged
        )
        self.m_percussion_notes_table_propertyGrid11.Bind(
            pg.EVT_PG_CHANGING, self.onPercussionInstTableChanging
        )

        # 设置初始状态

        self.m_ignore_midi_error_checkBox.Enable(False)
        self.experiment_type_choice.Enable(False)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def onProgressbarBasicStyleUpdating(self, event):
        pgb_style.set_base_style(
            self.m_BasicProgressBarStyleEntering_textCtrl4.GetValue()
        )

    def onProgressbarUnplayedStyleUpdating(self, event):
        pgb_style.set_to_play_style(
            self.m_unplayedProgressbarStyleEntering_textCtrl5.GetValue()
        )

    def onProgressbarPlayedStyleUpdating(self, event):
        pgb_style.set_played_style(
            self.m_playedProgressbarStyleEntering_textCtrl5.GetValue()
        )

    def onExperimentEnableUpdating(self, event):
        if self.m_enable_experiment_checkBox.GetValue():
            self.m_ignore_midi_error_checkBox.Enable(True)
            self.experiment_type_choice.Enable(True)
        else:
            self.m_ignore_midi_error_checkBox.Enable(False)
            self.experiment_type_choice.Enable(False)

    def onConvertMethodUpdating(self, event):
        global ConvertClass
        #  0  "常规转换",  1 "长音插值",  2 "同刻偏移"
        match self.experiment_type_choice.GetSelection():
            case 0:
                ConvertClass = (Musicreater.MidiConvert, "常规转换")
            case 1:
                ConvertClass = (Musicreater.experiment.FutureMidiConvertM4, "长音插值")
            case 2:
                ConvertClass = (Musicreater.experiment.FutureMidiConvertM5, "同刻偏移")

    def onMidiFaultIgnoranceChecking(self, event):
        global ignore_midi_mismatch_error
        ignore_midi_mismatch_error = self.m_ignore_midi_error_checkBox.GetValue()

    def onPitchedInstListChanging(self, event):
        global convert_table_selection
        convert_table_selection["PITCHED"] = (
            self.m_pitched_instrument_table_choice.GetStringSelection()
        )
        self.m_pitched_notes_table_propertyGrid1.SetPropertyValues(
            dict(
                [
                    ("pitched_inst_{}".format(midi_inst), mc_inst_patern[0])
                    for midi_inst, mc_inst_patern in convert_tables["PITCHED"][
                        convert_table_selection["PITCHED"]
                    ].items()
                ]
            )
        )
        # logger.info()

    def onPitchedInstTableChanged(self, event):
        global convert_table_selection, convert_tables
        convert_tables["PITCHED"]["自定义对照表"] = dict(
            [
                (i, j)
                for i, j in convert_tables["PITCHED"][
                    convert_table_selection["PITCHED"]
                ].items()
            ]
        )
        convert_table_selection["PITCHED"] = "自定义对照表"
        to_change_id = int(event.GetProperty().GetName().split("_")[-1])
        to_change_value = (
            event.GetProperty().GetValue(),
            Musicreater.MM_INSTRUMENT_DEVIATION_TABLE.get(
                event.GetProperty().GetValue(), -1
            ),
        )
        convert_tables["PITCHED"]["自定义对照表"][to_change_id] = to_change_value
        logger.info(
            "自定义乐音乐器对照表第 {} 项已更新为：{}".format(
                to_change_id, to_change_value
            )
        )
        if "自定义对照表" not in self.m_pitched_instrument_table_choice.Items:
            self.m_pitched_instrument_table_choice.Append("自定义对照表")
            self.m_pitched_instrument_table_choice.SetSelection(2)

    def onPitchedInstTableChanging(self, event):
        event.Skip()
        # event.GetPropertyName()
        # self.m_pitched_notes_table_propertyGrid1

    def onPercussionInstListChanging(self, event):
        global convert_table_selection
        convert_table_selection["PERCUSSION"] = (
            self.m_percussion_instrument_table_choice1.GetStringSelection()
        )
        self.m_percussion_notes_table_propertyGrid11.SetPropertyValues(
            dict(
                [
                    ("percussion_inst_{}".format(midi_inst), mc_inst_patern[0])
                    for midi_inst, mc_inst_patern in convert_tables["PERCUSSION"][
                        convert_table_selection["PERCUSSION"]
                    ].items()
                ]
            )
        )

    def onPercussionInstTableChanged(self, event):
        global convert_table_selection, convert_tables
        convert_tables["PERCUSSION"]["自定义对照表"] = dict(
            [
                (i, j)
                for i, j in convert_tables["PERCUSSION"][
                    convert_table_selection["PERCUSSION"]
                ].items()
            ]
        )
        convert_table_selection["PERCUSSION"] = "自定义对照表"
        to_change_id = int(event.GetProperty().GetName().split("_")[-1])
        to_change_value = (
            event.GetProperty().GetValue(),
            Musicreater.MM_INSTRUMENT_DEVIATION_TABLE.get(
                event.GetProperty().GetValue(), -1
            ),
        )
        convert_tables["PERCUSSION"]["自定义对照表"][to_change_id] = to_change_value
        logger.info(
            "自定义打击乐器对照表第 {} 项已更新为：{}".format(
                to_change_id, to_change_value
            )
        )
        if "自定义对照表" not in self.m_percussion_instrument_table_choice1.Items:
            self.m_percussion_instrument_table_choice1.Append("自定义对照表")
            self.m_percussion_instrument_table_choice1.SetSelection(2)

    def onPercussionInstTableChanging(self, event):
        event.Skip()


logger.info("执行应用。")

# 启动应用程序
if __name__ == "__main__":
    logger.info("检查更新：")

    check_update(
        __appname__,
        "https://gitee.com/TriM-Organization/Linglun-Converter/raw/master/llc_win_wxPython.py",
        __version__,
        lambda text: wx.MessageDialog(
            None,
            text,
            "软件更新",
            wx.ICON_INFORMATION | wx.YES_DEFAULT,
        ).ShowModal(),
        logger,
        __zhver__,
    )

    logger.info("开启窗口")

    app = LinglunConverterApp()

    app.MainLoop()

    if on_exit_saving:
        enpack_llc_pack(
            (
                pgb_style,
                on_exit_saving,
                ignore_midi_mismatch_error,
                convert_tables,
                convert_table_selection,
                ConvertClass,
            ),
            "save.llc.config",
        )
    else:
        for path, dir_list, file_list in os.walk(r"./"):
            for file_name in file_list:
                if file_name.endswith(".llc.config"):
                    os.remove(
                        os.path.join(path, file_name),
                    )
    # input("按下回车退出……")
