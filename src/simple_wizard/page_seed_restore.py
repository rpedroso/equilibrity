import wx
from wx.lib.intctrl import IntCtrl

_ = wx.GetTranslation


class PageRestoreSeed(wx.adv.WizardPage):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY,
                                _("Restore wallet from seed"))
        label_1.SetFont(
            wx.Font(12,
                    wx.FONTFAMILY_DEFAULT,
                    wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                    0, ""))
        sizer_1.Add(label_1, 0, wx.ALL | wx.EXPAND, 20)

        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.BOTTOM | wx.EXPAND, 10)

        label_2 = wx.StaticText(self, wx.ID_ANY,
                                _("Please enter your seed below"))
        sizer_1.Add(label_2, 0, wx.ALL, 20)

        label_3 = wx.StaticText(self, wx.ID_ANY, _("Wallet Seed"))
        sizer_1.Add(label_3, 0, wx.LEFT, 20)

        self.txt_wallet_seed = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.TE_MULTILINE)
        sizer_1.Add(self.txt_wallet_seed, 1,
                    wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        label_4 = wx.StaticText(self, wx.ID_ANY, _("Wallet birthday"))
        sizer_1.Add(label_4, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        self.txt_wallet_birthday = IntCtrl(self)
        sizer_1.Add(self.txt_wallet_birthday, 0,
                    wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        self.SetSizer(sizer_1)
        self.btn_prev = self.FindWindowById(wx.ID_BACKWARD)
