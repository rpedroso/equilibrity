import wx

import gettext



class PageConfirmSeed(wx.Panel):
    def __init__(self, *args, **kwds):
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY, _("Your new wallet"))
        label_1.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_1.Add(label_1, 0, wx.ALL | wx.EXPAND, 20)

        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.BOTTOM | wx.EXPAND, 10)

        label_2 = wx.StaticText(self, wx.ID_ANY, _("This is your new wallet's seed phrase.\nThe seed prase is the only way to restore the wallet.\n\nif you forget the seed phrase, THERE IS NO WAY TO RESTORE YOUT WALLET AND THE FUNDS in it.\n\nPLEASE BACK IT UP SECURELY."))
        sizer_1.Add(label_2, 0, wx.ALL, 20)

        self.text_ctrl_1 = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer_1.Add(self.text_ctrl_1, 1, wx.ALL | wx.EXPAND, 20)

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.Layout()

