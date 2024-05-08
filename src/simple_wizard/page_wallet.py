import wx

_ = wx.GetTranslation


class PageWallet(wx.adv.WizardPage):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY, _("Create or Restore wallet"))
        label_1.SetFont(wx.Font(12, wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_BOLD, 0, ""))
        sizer_1.Add(label_1, 0, wx.ALL | wx.EXPAND, 20)

        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.ALL | wx.EXPAND, 10)

        self.rd_wallet_new = wx.RadioButton(self, wx.ID_ANY,
                                            _(" Create a new wallet"))
        sizer_1.Add(self.rd_wallet_new, 0,
                    wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        sizer_1.Add((1, 1), 0, wx.ALL | wx.EXPAND, 5)

        lbl1 = wx.StaticText(
            self,
            label=_('Create a new wallet with a randomly generated seed.')
        )
        sizer_1.Add(lbl1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        sizer_1.Add((1, 1), 0, wx.ALL | wx.EXPAND, 5)

        self.rd_wallet_restore = wx.RadioButton(self, wx.ID_ANY,
                                                _("Restore wallet from seed"))
        sizer_1.Add(self.rd_wallet_restore, 0,
                    wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 20)

        lbl2 = wx.StaticText(
            self,
            label=_('Restore an existing wallet, using the word seed.')
        )
        sizer_1.Add((1, 1), 0, wx.ALL | wx.EXPAND, 5)
        sizer_1.Add(lbl2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 20)

        self.SetSizer(sizer_1)

        self.btn_next = self.FindWindowById(wx.ID_FORWARD)


if __name__ == "__main__":
    app = wx.App()
    f = wx.Frame(None)
    PageWallet(f)
    f.Show()
    app.MainLoop()
