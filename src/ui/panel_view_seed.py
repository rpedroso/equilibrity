import wx

_ = wx.GetTranslation


class PanelViewSeed(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX
        super().__init__(parent, title=_('Seed & Keys'), style=style)
        # self.SetMinSize((450, 500))
        # self.SetSize((450, 500))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        # static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        # sizer_1.Add(static_line_1, 0, wx.BOTTOM | wx.EXPAND, 10)

        label_2 = wx.StaticText(self, wx.ID_ANY, _("Seed:"), size=(550, -1))
        sizer_1.Add(label_2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        self.txt_wallet_seed = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY
        )
        self.txt_wallet_seed.SetFont(
            wx.Font(10, wx.FONTFAMILY_TELETYPE,
                    wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "")
        )
        sizer_1.Add(self.txt_wallet_seed, 1,
                    wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        label_3 = wx.StaticText(self, wx.ID_ANY, _("Secret view key:"))
        sizer_1.Add(label_3, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        self.txt_wallet_secret_view = wx.TextCtrl(self,
                                                  wx.ID_ANY, "",
                                                  style=wx.TE_READONLY)
        sizer_1.Add(self.txt_wallet_secret_view, 0,
                    wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        label_4 = wx.StaticText(self, wx.ID_ANY, _("Public view key:"))
        sizer_1.Add(label_4, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        self.txt_wallet_public_view = wx.TextCtrl(self, wx.ID_ANY, "",
                                                  style=wx.TE_READONLY)
        sizer_1.Add(self.txt_wallet_public_view, 0,
                    wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        label_5 = wx.StaticText(self, wx.ID_ANY, _("Secret spent key:"))
        sizer_1.Add(label_5, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        self.txt_wallet_secret_spent = wx.TextCtrl(self, wx.ID_ANY, "",
                                                   style=wx.TE_READONLY)
        sizer_1.Add(self.txt_wallet_secret_spent, 0,
                    wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        label_6 = wx.StaticText(self, wx.ID_ANY,
                                _("Public spent key:"))
        sizer_1.Add(label_6, 0,
                    wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        self.txt_wallet_public_spent = wx.TextCtrl(self, wx.ID_ANY, "",
                                                   style=wx.TE_READONLY)
        sizer_1.Add(self.txt_wallet_public_spent, 0,
                    wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_CLOSE)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        self.SetEscapeId(btn.GetId())

        sizer_1.Add(btnsizer, 0, wx.EXPAND | wx.ALL, 8)

        self.SetSizerAndFit(sizer_1)
        # sizer_1.Fit(self)

        self.Layout()


if __name__ == "__main__":
    app = wx.App()
    PanelViewSeed(None).ShowModal()
