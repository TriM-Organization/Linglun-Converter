# -*- coding: utf-8 -*-

"""
伶伦转换器 HTML页组件
Linglun Converter HTML Component

版权所有 © 2025 金羿
Copyright © 2025 EillesWan

开源相关声明请见 仓库根目录下的 License.md
Terms & Conditions: License.md in the root directory
"""


import wx
import wx.html


class HTMLFrame(wx.Frame):
    """桌面程序主窗口类"""

    def __init__(
        self,
        parent,
        tip_text,
        web_text,
        window_title: str = "新版本已发布",
        bg_colour: tuple | wx.Colour = (0, 0, 0),
        window_size: tuple = (800, 480),
    ):
        """构造函数"""

        wx.Frame.__init__(
            self,
            parent,
            id=wx.ID_ANY,
            title=window_title,
            pos=wx.DefaultPosition,
            size=wx.Size(*window_size),
            style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL,
        )

        # self.SetIcon(wx.Icon('', wx.BITMAP_TYPE_ICO))
        self.SetBackgroundColour(wx.Colour(bg_colour))
        self.Center()

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.m_staticText1 = wx.StaticText(
            self,
            wx.ID_ANY,
            tip_text,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.ALIGN_CENTER_HORIZONTAL,
        )
        self.m_staticText1.Wrap(-1)

        self.m_staticText1.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize() * 2,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans M",
            )
        )

        bSizer1.Add(self.m_staticText1, 3, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)

        self.m_htmlWin1 = wx.html.HtmlWindow(
            self,
            wx.ID_ANY,
            wx.DefaultPosition,
            wx.DefaultSize,
            wx.html.HW_SCROLLBAR_AUTO,
        )
        self.m_htmlWin1.SetFont(
            wx.Font(
                wx.NORMAL_FONT.GetPointSize(),
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_NORMAL,
                False,
                "OPPOSans R",
            )
        )
        self.m_htmlWin1.SetStandardFonts(normal_face="OPPOSans R")

        bSizer1.Add(self.m_htmlWin1, 5, wx.EXPAND | wx.RESERVE_SPACE_EVEN_IF_HIDDEN, 5)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_button1 = wx.Button(
            self, wx.ID_ANY, "取消", wx.DefaultPosition, wx.DefaultSize, 0
        )
        bSizer2.Add(self.m_button1, 0, wx.ALL, 5)

        self.m_button2 = wx.Button(
            self, wx.ID_ANY, "更新", wx.DefaultPosition, wx.DefaultSize, 0
        )
        bSizer2.Add(self.m_button2, 0, wx.ALL, 5)

        bSizer1.Add(bSizer2, 0, wx.ALIGN_RIGHT, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        self.m_htmlWin1.SetPage(web_text)

        # Connect Events
        self.m_button1.Bind(wx.EVT_BUTTON, self.on_Cancel_Click)
        self.m_button2.Bind(wx.EVT_BUTTON, self.on_Update_Click)

        self.ok = False

    def __del__(self):
        # return self.ok
        pass

    def getok(self) -> bool:
        return self.ok

    # Virtual event handlers, override them in your derived class
    def on_Cancel_Click(self, event):
        self.ok = False
        self.Destroy()

    def on_Update_Click(self, event):
        self.ok = True
        self.Destroy()


def go_update_tip(tip_text: str, html_context: str) -> bool:
    app = wx.App()
    frame = HTMLFrame(
        None,
        tip_text,
        html_context,
        bg_colour=wx.SystemSettings.GetColour(wx.SYS_COLOUR_MENU),
    )
    frame.Show()
    app.MainLoop()
    return frame.getok()


if __name__ == "__main__":
    go_update_tip(
        "！有新版本！\n最新的 {app} 已经是 {latest} 版本，当前您正在使用的仍是 {current} 版本，是否更新？",
        '<ol>\n<li>\n<strong>[修复]</strong> 完成<ahref="https://gitee.com/TriM-Organization/Linglun-Converter/issues/I8YN22" rel="nofollow noreferrer noopener"target="_blank">#I8YN22</a>问题的修复，解决转换错误的问题</li>\n<li>\n<strong>[新增]</strong>支持选择自定的乐器对照表</li>\n<li>\n<strong>[新增]</strong>支持自选距离音量算法</li>\n<li>\n<strong>[新增]</strong>使用Packer以打包发行版（详情如下方说明）</li>\n<li>\n<strong>[优化]</strong>提高调用效率，优化代码结构</li>\n<li>\n<strong>[优化]</strong>提升部分注释可读性</li>\n</ol>\n',
    )

    go_update_tip(
        "！有新版本！\n最新的 音·创 已经是 1.7.3 版本，当前您正在使用的仍是 1.7.0 版本，是否更新？",
        '<ol>\n<li>\n<strong>[修复]</strong> 完成<a href="https://gitee.com/TriM-Organization/Linglun-Converter/issues/I8YN22" rel="nofollow noreferrer noopener" target="_blank">#I8YN22</a>问题的修复，解决转换错误的问题</li>\n<li>\n<strong>[新增]</strong> 支持选择自定的乐器对照表</li>\n<li>\n<strong>[新增]</strong> 支持自选距离音量算法</li>\n<li>\n<strong>[新增]</strong> 使用Packer以打包发行版（详情如下方说明）</li>\n<li>\n<strong>[优化]</strong> 提高调用效率，优 化代码结构</li>\n<li>\n<strong>[优化]</strong> 提升部分注释可读性</li>\n</ol>\n<h2>打包文件结构</h2>\n<p>我们使用Python库 <code>dill</code> 和 <code>Brotli</code> 对整个库的包体进行打包，方式如下：</p>\n<div class="markdown-code-block">\n<pre lang="python" class="python"><code>packing_bytes = brotli.compress(dill.dumps(sth,))\n</code></pre>\n<div class="markdown-code-block-copy-btn"></div>\n</div>\n<p>每个包中的内容为：</p>\n<div class="markdown-code-block">\n<pre lang="python" class="python"><code>MSCT_MAIN = (\n    Musicreater,\n    Musicreater.experiment,\n    Musicreater.previous,\n)\n\nMSCT_PLUGIN = (Musicreater.plugin,)\n\nMSCT_PLUGIN_FUNCTION = (\n    to_addon_pack_in_delay,\n    to_addon_pack_in_repeater,\n    to_addon_pack_in_score,\n    to_mcstructure_file_in_delay,\n    to_mcstructure_file_in_repeater,\n    to_mcstructure_file_in_score,\n    to_BDX_file_in_delay,\n    to_BDX_file_in_score,\n)\n</code></pre>\n<div class="markdown-code-block-copy-btn"></div>\n</div>',
    )
