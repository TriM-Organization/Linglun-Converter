# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.media

###########################################################################
## Class LingLunAuthorPageFrame
###########################################################################


class LingLunAuthorPageFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=wx.EmptyString,
            pos=wx.DefaultPosition,
            size=wx.Size(610, 560),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        mian_sizer = wx.BoxSizer(wx.VERTICAL)

        self.m_listbook1 = wx.Listbook(
            self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_RIGHT
        )
        self.trim_pannel = wx.Panel(
            self.m_listbook1,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        what_we_called_trim_org = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_TriMO_Theme_mediaCtrl1 = wx.media.MediaCtrl(
            self.trim_pannel,
            wx.ID_ANY,
            wx.EmptyString,
            wx.DefaultPosition,
            wx.DefaultSize,
        )
        self.m_TriMO_Theme_mediaCtrl1.Load("TriMO_Theme.mp4")
        self.m_TriMO_Theme_mediaCtrl1.SetPlaybackRate(1)
        self.m_TriMO_Theme_mediaCtrl1.SetVolume(1)
        self.m_TriMO_Theme_mediaCtrl1.ShowPlayerControls(
            wx.media.MEDIACTRLPLAYERCONTROLS_VOLUME
        )

        self.m_TriMO_Theme_mediaCtrl1.Play()
        bSizer2.Add(self.m_TriMO_Theme_mediaCtrl1, 1, wx.ALL | wx.EXPAND, 5)

        self.m_staticText1 = wx.StaticText(
            self.trim_pannel, wx.ID_ANY, "™", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText1.Wrap(-1)

        bSizer2.Add(self.m_staticText1, 0, wx.ALL, 5)

        what_we_called_trim_org.Add(bSizer2, 1, wx.EXPAND, 5)

        self.m_staticText2 = wx.StaticText(
            self.trim_pannel,
            wx.ID_ANY,
            "睿乐 - 我的世界多媒体组织\nTriM Org - Minecraft Muti-Media Organization ",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL,
        )
        self.m_staticText2.Wrap(-1)

        what_we_called_trim_org.Add(self.m_staticText2, 0, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl1 = wx.TextCtrl(
            self.trim_pannel,
            wx.ID_ANY,
            "\t嗨~\n\t我们是 睿乐组织（TriMO, 全称 Minecraft Muti-Media Organization），意为“我的世界多媒体组织”。\n\t我们组织的主要活动是一些有关我的世界与多媒体相关的程序项目，例如伶伦（我的世界数字音频工作站），我的世界视频播放制作器（MVP）等。\n\t我们组织也会尝试开发一些跟人工智能、音乐、数字音频工作站（DAW）等相关的内容，不仅限于我的世界相关内容的开发。\n\t我们欢迎任何有相关兴趣的同志加入组织或者提交你的PR、创建你的issues、提出意见和建议！\n\n电邮：mailto:TriM-Organization@hotmail.com\nQ群：861684859 https://jq.qq.com/?_wv=1027&k=hpeRxrYr",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_AUTO_URL | wx.TE_BESTWRAP | wx.TE_MULTILINE | wx.TE_READONLY,
        )
        what_we_called_trim_org.Add(self.m_textCtrl1, 0, wx.ALL | wx.EXPAND, 5)

        self.trim_pannel.SetSizer(what_we_called_trim_org)
        self.trim_pannel.Layout()
        what_we_called_trim_org.Fit(self.trim_pannel)
        self.m_listbook1.AddPage(self.trim_pannel, "睿乐组织", True)
        self.eilles_pannel = wx.Panel(
            self.m_listbook1,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_bitmap1 = wx.StaticBitmap(
            self.eilles_pannel,
            wx.ID_ANY,
            wx.Bitmap("../resources/金羿ELSV5.png", wx.BITMAP_TYPE_ANY),
            wx.DefaultPosition,
            wx.DefaultSize,
            0,
        )
        bSizer4.Add(self.m_bitmap1, 1, wx.ALL, 5)

        self.m_staticText21 = wx.StaticText(
            self.eilles_pannel,
            wx.ID_ANY,
            "金羿ELS\nEilles ",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL,
        )
        self.m_staticText21.Wrap(-1)

        bSizer4.Add(self.m_staticText21, 0, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl11 = wx.TextCtrl(
            self.eilles_pannel,
            wx.ID_ANY,
            "我的世界基岩版指令作者，个人开发者，B 站不知名 UP 主……",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_AUTO_URL | wx.TE_BESTWRAP | wx.TE_READONLY,
        )
        bSizer4.Add(self.m_textCtrl11, 0, wx.ALL | wx.EXPAND, 5)

        bSizer3.Add(bSizer4, 1, wx.EXPAND, 5)

        self.m_staticText11 = wx.StaticText(
            self.eilles_pannel, wx.ID_ANY, "™", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText11.Wrap(-1)

        bSizer3.Add(self.m_staticText11, 0, wx.ALL | wx.EXPAND, 5)

        self.eilles_pannel.SetSizer(bSizer3)
        self.eilles_pannel.Layout()
        bSizer3.Fit(self.eilles_pannel)
        self.m_listbook1.AddPage(self.eilles_pannel, "金羿ELS", False)
        self.bgarray_pannel = wx.Panel(
            self.m_listbook1,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TAB_TRAVERSAL,
        )
        bSizer31 = wx.BoxSizer(wx.HORIZONTAL)

        bSizer41 = wx.BoxSizer(wx.VERTICAL)

        bSizer41.Add((0, 0), 1, wx.EXPAND, 5)

        self.m_staticText211 = wx.StaticText(
            self.bgarray_pannel,
            wx.ID_ANY,
            "诸葛亮与八卦阵\nBgArray",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL,
        )
        self.m_staticText211.Wrap(-1)

        bSizer41.Add(self.m_staticText211, 0, wx.ALL | wx.EXPAND, 5)

        self.m_textCtrl111 = wx.TextCtrl(
            self.bgarray_pannel,
            wx.ID_ANY,
            "我的世界基岩版玩家，喜欢编程和音乐。",
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.TE_AUTO_URL | wx.TE_BESTWRAP | wx.TE_READONLY,
        )
        bSizer41.Add(self.m_textCtrl111, 0, wx.ALL | wx.EXPAND, 5)

        bSizer31.Add(bSizer41, 1, wx.EXPAND, 5)

        self.m_staticText111 = wx.StaticText(
            self.bgarray_pannel, wx.ID_ANY, "™", wx.DefaultPosition, wx.DefaultSize, 0
        )
        self.m_staticText111.Wrap(-1)

        bSizer31.Add(self.m_staticText111, 0, wx.ALL | wx.EXPAND, 5)

        self.bgarray_pannel.SetSizer(bSizer31)
        self.bgarray_pannel.Layout()
        bSizer31.Fit(self.bgarray_pannel)
        self.m_listbook1.AddPage(self.bgarray_pannel, "诸葛八卦", False)

        mian_sizer.Add(self.m_listbook1, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(mian_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

    def __del__(self):
        pass
