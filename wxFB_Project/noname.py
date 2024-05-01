# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.propgrid as pg

###########################################################################
## Class LingLunMainFrame
###########################################################################


class LingLunMainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            pos=wx.DefaultPosition,
            size=wx.Size(660, 723),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
            name="LingLunConverter",
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
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOWTEXT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

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

        self.EditMenu = wx.Menu()
        self.play_via_websocket = wx.MenuItem(
            self.EditMenu,
            wx.ID_ANY,
            "启用WebSocket播放",
            "在指定端口上开启WebSocket播放服务器",
            wx.ITEM_NORMAL,
        )
        self.EditMenu.Append(self.play_via_websocket)

        self.m_menubar1.Append(self.EditMenu, "编辑")

        self.AboutMenu = wx.Menu()
        self.m_author_info_menuItem4 = wx.MenuItem(
            self.AboutMenu, wx.ID_ANY, "作者信息", "查看关于信息", wx.ITEM_NORMAL
        )
        self.AboutMenu.Append(self.m_author_info_menuItem4)

        self.m_menubar1.Append(self.AboutMenu, "关于")

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

        self.convert_page = wx.Panel(
            self.mian_notebook,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        self.mian_notebook.AddPage(self.convert_page, "开始转换", True)
        self.setting_page = wx.Panel(
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
        self.Bind(
            wx.EVT_MENU,
            self.onWebSocketPlayButtonPressed,
            id=self.play_via_websocket.GetId(),
        )
        self.Bind(
            wx.EVT_MENU,
            self.on_author_button_pressed,
            id=self.m_author_info_menuItem4.GetId(),
        )
        self.m_LinglunWords_staticText1.Bind(wx.EVT_LEFT_DCLICK, self.onYanlunDClicked)
        self.m_LinglunWords_staticText1.Bind(wx.EVT_MOUSEWHEEL, self.onYanlunWheeled)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def onResetSettingButtonSelection(self, event):
        event.Skip()

    def onExitButtonPressed(self, event):
        event.Skip()

    def onWebSocketPlayButtonPressed(self, event):
        event.Skip()

    def on_author_button_pressed(self, event):
        event.Skip()

    def onYanlunDClicked(self, event):
        event.Skip()

    def onYanlunWheeled(self, event):
        event.Skip()


###########################################################################
## Class ConvertPagePanel
###########################################################################


class ConvertPagePanel(wx.Panel):

    def __init__(
        self,
        parent,
        id=wx.ID_ANY,
        pos=wx.DefaultPosition,
        size=wx.Size(652, 588),
        style=wx.TAB_TRAVERSAL,
        name=wx.EmptyString,
    ):
        wx.Panel.__init__(
            self, parent, id=id, pos=pos, size=size, style=style, name=name
        )

        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        main_page_sizer = wx.BoxSizer(wx.VERTICAL)

        s_midiChooseSizer = wx.BoxSizer(wx.HORIZONTAL)

        MidiChooser_Delete_and_Tips_bSizer15 = wx.BoxSizer(wx.VERTICAL)

        self.m_ChooseMidiTips_staticText3 = wx.StaticText(
            self,
            wx.ID_ANY,
            "MIDI文件列\n（双击移除）",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL,
        )
        self.m_ChooseMidiTips_staticText3.Wrap(-1)

        MidiChooser_Delete_and_Tips_bSizer15.Add(
            self.m_ChooseMidiTips_staticText3, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5
        )

        self.m_done_then_remove_checkBox6 = wx.CheckBox(
            self, wx.ID_ANY, "完成后移出", wx.DefaultPosition, wx.DefaultSize, 0
        )
        MidiChooser_Delete_and_Tips_bSizer15.Add(
            self.m_done_then_remove_checkBox6, 0, wx.ALL, 5
        )

        s_midiChooseSizer.Add(
            MidiChooser_Delete_and_Tips_bSizer15, 0, wx.SHAPED | wx.EXPAND, 0
        )

        ss_MidiChooserSizer_bSizer9 = wx.BoxSizer(wx.VERTICAL)

        m_midiFilesList_listBox2Choices = []
        self.m_midiFilesList_listBox2 = wx.ListBox(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            m_midiFilesList_listBox2Choices,
            wx.LB_HSCROLL | wx.LB_SORT,
        )
        ss_MidiChooserSizer_bSizer9.Add(self.m_midiFilesList_listBox2, 1, wx.EXPAND, 0)

        s_midiChooseSizer.Add(ss_MidiChooserSizer_bSizer9, 1, wx.EXPAND, 5)

        MidiChooser_Open_and_Clear_Buttons_bSizer16 = wx.BoxSizer(wx.VERTICAL)

        self.m_midiBroseButton_button21 = wx.Button(
            self, wx.ID_ANY, "打开…", wx.DefaultPosition, wx.DefaultSize, 0
        )
        MidiChooser_Open_and_Clear_Buttons_bSizer16.Add(
            self.m_midiBroseButton_button21, 0, wx.ALL | wx.EXPAND, 5
        )

        self.m_midiChooser_Clear_button3 = wx.Button(
            self, wx.ID_ANY, "清空列表", wx.DefaultPosition, wx.DefaultSize, 0
        )
        MidiChooser_Open_and_Clear_Buttons_bSizer16.Add(
            self.m_midiChooser_Clear_button3, 0, wx.ALL | wx.EXPAND, 5
        )

        s_midiChooseSizer.Add(
            MidiChooser_Open_and_Clear_Buttons_bSizer16, 0, wx.SHAPED, 5
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

        m_playerChoice_choice2Choices = ["计分控制", "命令延时", "红石中继"]
        self.m_playerChoice_choice2 = wx.Choice(
            ss_playerChooseSizer.GetStaticBox(),
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            m_playerChoice_choice2Choices,
            0,
        )
        self.m_playerChoice_choice2.SetSelection(1)
        ss_playerChooseSizer.Add(self.m_playerChoice_choice2, 0, wx.ALL | wx.EXPAND, 5)

        s_formatChooseSizer.Add(ss_playerChooseSizer, 1, wx.ALL | wx.EXPAND, 5)

        main_page_sizer.Add(s_formatChooseSizer, 0, wx.EXPAND, 5)

        s_promptSizer = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "转换参数"), wx.VERTICAL
        )

        ss_regularPromoptsEnteringSizer1 = wx.BoxSizer(wx.HORIZONTAL)

        sss_VolumnPersentageEnteringSizer = wx.StaticBoxSizer(
            wx.StaticBox(s_promptSizer.GetStaticBox(), wx.ID_ANY, "最小音量"),
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
            "0.1",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL | wx.SP_ARROW_KEYS | wx.TE_PROCESS_ENTER,
            0,
            1,
            0.100000,
            0.001,
        )
        self.m_volumn_spinCtrlDouble1.SetDigits(3)
        sss_VolumnPersentageEnteringSizer.Add(
            self.m_volumn_spinCtrlDouble1, 0, wx.ALL, 5
        )

        ss_regularPromoptsEnteringSizer1.Add(
            sss_VolumnPersentageEnteringSizer, 0, wx.ALL | wx.EXPAND, 5
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
            sss_SpeedEnteringSizer, 0, wx.ALL | wx.EXPAND, 5
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
            "Yourself",
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

        main_page_sizer.Add(s_promptSizer, 0, wx.ALL | wx.EXPAND | wx.SHAPED, 5)

        s_StartSizer_sbSizer18 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, "开始转换"), wx.HORIZONTAL
        )

        s_StartSizer_sbSizer18.SetMinSize(wx.Size(-1, 100))
        ss_Midi_Convert_distPath_bSizer17 = wx.BoxSizer(wx.VERTICAL)

        ss_Dest_chooser_Sizer_in_bSizer18 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_tip_Change_Dest_staticText7 = wx.StaticText(
            s_StartSizer_sbSizer18.GetStaticBox(),
            wx.ID_ANY,
            "指定输出路径",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_tip_Change_Dest_staticText7.Wrap(-1)

        ss_Dest_chooser_Sizer_in_bSizer18.Add(
            self.m_tip_Change_Dest_staticText7, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5
        )

        self.m_Convertion_Destination_Picker_dirPicker1 = wx.DirPickerCtrl(
            s_StartSizer_sbSizer18.GetStaticBox(),
            wx.ID_ANY,
            "./",
            "选择目标目录",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.DIRP_DEFAULT_STYLE,
        )
        ss_Dest_chooser_Sizer_in_bSizer18.Add(
            self.m_Convertion_Destination_Picker_dirPicker1, 1, wx.ALL | wx.EXPAND, 5
        )

        ss_Midi_Convert_distPath_bSizer17.Add(
            ss_Dest_chooser_Sizer_in_bSizer18, 0, wx.ALL | wx.EXPAND, 5
        )

        self.m_Check_Every_Their_Path_checkBox7 = wx.CheckBox(
            s_StartSizer_sbSizer18.GetStaticBox(),
            wx.ID_ANY,
            "输出到每个文件所在目录",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_Check_Every_Their_Path_checkBox7.SetValue(True)
        ss_Midi_Convert_distPath_bSizer17.Add(
            self.m_Check_Every_Their_Path_checkBox7, 0, wx.ALL, 5
        )

        s_StartSizer_sbSizer18.Add(ss_Midi_Convert_distPath_bSizer17, 1, wx.EXPAND, 5)

        self.m_start_button2 = wx.Button(
            s_StartSizer_sbSizer18.GetStaticBox(),
            wx.ID_ANY,
            "开始转换",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        s_StartSizer_sbSizer18.Add(self.m_start_button2, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        main_page_sizer.Add(s_StartSizer_sbSizer18, 1, wx.ALL | wx.EXPAND, 5)

        self.SetSizer(main_page_sizer)
        self.Layout()

        # Connect Events
        self.m_ChooseMidiTips_staticText3.Bind(wx.EVT_LEFT_DCLICK, self.MidiEasterEgg)
        self.m_done_then_remove_checkBox6.Bind(
            wx.EVT_CHECKBOX, self.on_Done_Then_Remove_Clicked
        )
        self.m_midiFilesList_listBox2.Bind(wx.EVT_LISTBOX, self.onFileListUpdated)
        self.m_midiFilesList_listBox2.Bind(
            wx.EVT_LISTBOX_DCLICK, self.onFileDoubleClicked
        )
        self.m_midiBroseButton_button21.Bind(wx.EVT_BUTTON, self.openFile)
        self.m_midiChooser_Clear_button3.Bind(
            wx.EVT_BUTTON, self.on_Chooer_Clear_Button_Pressed
        )
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
        self.m_tip_Change_Dest_staticText7.Bind(
            wx.EVT_LEFT_DCLICK, self.on_Change_to_Default_Path
        )
        self.m_Convertion_Destination_Picker_dirPicker1.Bind(
            wx.EVT_DIRPICKER_CHANGED, self.on_Convert_Dest_Changed
        )
        self.m_Check_Every_Their_Path_checkBox7.Bind(
            wx.EVT_CHECKBOX, self.On_Their_Path_Checked
        )
        self.m_start_button2.Bind(wx.EVT_BUTTON, self.onStartButtonPressed)

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def MidiEasterEgg(self, event):
        event.Skip()

    def on_Done_Then_Remove_Clicked(self, event):
        event.Skip()

    def onFileListUpdated(self, event):
        event.Skip()

    def onFileDoubleClicked(self, event):
        event.Skip()

    def openFile(self, event):
        event.Skip()

    def on_Chooer_Clear_Button_Pressed(self, event):
        event.Skip()

    def onOutputFormatChosen(self, event):
        event.Skip()

    def onPlayerChosen(self, event):
        event.Skip()

    def onVolumeScrolling(self, event):
        event.Skip()

    def onVolumeSpinChanged(self, event):
        event.Skip()

    def onSpeedScrolling(self, event):
        event.Skip()

    def onSpeedSpinChanged(self, event):
        event.Skip()

    def onProgressbarChecked(self, event):
        event.Skip()

    def onScoreboredNameUpdating(self, event):
        event.Skip()

    def onAutoResetScoreboardChecked(self, event):
        event.Skip()

    def onPlayerSelectorUpdating(self, event):
        event.Skip()

    def onStructureMaxHeightScrolling(self, event):
        event.Skip()

    def onStructureMaxHeightSpinChanged(self, event):
        event.Skip()

    def onBDXfileSignNameUpdating(self, event):
        event.Skip()

    def on_Change_to_Default_Path(self, event):
        event.Skip()

    def on_Convert_Dest_Changed(self, event):
        event.Skip()

    def On_Their_Path_Checked(self, event):
        event.Skip()

    def onStartButtonPressed(self, event):
        event.Skip()


###########################################################################
## Class SettingPagePannel
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
            "▶ %%N [ %%s/%^s %%% __________ %%t|%^t ]",
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
            "§7=§r",
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
            "§e=§r",
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
            self.m_enable_experiment_checkBox, 1, wx.ALL | wx.EXPAND, 5
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
        self.experiment_type_choice.SetSelection(0)
        setting_page1_experiment_style.Add(
            self.experiment_type_choice, 2, wx.ALL | wx.EXPAND, 5
        )

        self.m_ignore_midi_error_checkBox = wx.CheckBox(
            setting_page1_experiment_style.GetStaticBox(),
            wx.ID_ANY,
            "忽略MIDI错误",
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        self.m_ignore_midi_error_checkBox.SetValue(True)
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
        self.setting_notebook.AddPage(self.setting_page1, "基本信息", False)
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

        m_pitched_instrument_table_choiceChoices = ["“偷吃”的对照表", "“经典”对照表"]
        self.m_pitched_instrument_table_choice = wx.Choice(
            self.setting_page2,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            m_pitched_instrument_table_choiceChoices,
            0,
        )
        self.m_pitched_instrument_table_choice.SetSelection(0)
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
            self.m_pitched_instrument_table_choice, 0, wx.ALL | wx.EXPAND, 5
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

        self.m_propertyGridItem1 = self.m_pitched_notes_table_propertyGrid1.Append(
            pg.StringProperty("乐音乐器1", "乐音乐器1")
        )
        self.m_propertyGridItem2 = self.m_pitched_notes_table_propertyGrid1.Append(
            pg.StringProperty("乐音乐器2", "乐音乐器2")
        )
        setting_page2_box_sizer.Add(
            self.m_pitched_notes_table_propertyGrid1, 1, wx.ALL | wx.EXPAND, 5
        )

        self.setting_page2.SetSizer(setting_page2_box_sizer)
        self.setting_page2.Layout()
        setting_page2_box_sizer.Fit(self.setting_page2)
        self.setting_notebook.AddPage(self.setting_page2, "乐音乐器对照表", True)
        self.setting_page3 = wx.Panel(
            self.setting_notebook,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        setting_page3_box_sizer = wx.BoxSizer(wx.VERTICAL)

        m_percussion_instrument_table_choice1Choices = [
            "“偷吃”的对照表",
            "“经典”对照表",
        ]
        self.m_percussion_instrument_table_choice1 = wx.Choice(
            self.setting_page3,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            m_percussion_instrument_table_choice1Choices,
            0,
        )
        self.m_percussion_instrument_table_choice1.SetSelection(0)
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
            self.m_percussion_instrument_table_choice1, 0, wx.ALL | wx.EXPAND, 5
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

        self.m_propertyGridItem11 = self.m_percussion_notes_table_propertyGrid11.Append(
            pg.StringProperty("打击乐器1", "打击乐器1")
        )
        self.m_propertyGridItem21 = self.m_percussion_notes_table_propertyGrid11.Append(
            pg.StringProperty("打击乐器2", "打击乐器2")
        )
        setting_page3_box_sizer.Add(
            self.m_percussion_notes_table_propertyGrid11, 1, wx.ALL | wx.EXPAND, 5
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

    def __del__(self):
        pass

    # Virtual event handlers, override them in your derived class
    def onProgressbarBasicStyleUpdating(self, event):
        event.Skip()

    def onProgressbarUnplayedStyleUpdating(self, event):
        event.Skip()

    def onProgressbarPlayedStyleUpdating(self, event):
        event.Skip()

    def onExperimentEnableUpdating(self, event):
        event.Skip()

    def onConvertMethodUpdating(self, event):
        event.Skip()

    def onMidiFaultIgnoranceChecking(self, event):
        event.Skip()

    def onPitchedInstListChanging(self, event):
        event.Skip()

    def onPitchedInstTableChanged(self, event):
        event.Skip()

    def onPitchedInstTableChanging(self, event):
        event.Skip()

    def onPercussionInstListChanging(self, event):
        event.Skip()

    def onPercussionInstTableChanged(self, event):
        event.Skip()

    def onPercussionInstTableChanging(self, event):
        event.Skip()
