import wx

_ = wx.GetTranslation


class PageSeed(wx.adv.WizardPage):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY, _("Your new wallet"))
        label_1.SetFont(wx.Font(12,
                                wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_BOLD, 0, "")
                        )
        sizer_1.Add(label_1, 0, wx.ALL | wx.EXPAND, 20)

        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.BOTTOM | wx.EXPAND, 10)

        label_2 = wx.StaticText(
            self, wx.ID_ANY,
            _("This is your new wallet's seed phrase.\n"
              "The seed prase is the only way to restore the wallet.\n\n"
              "if you forget the seed phrase, THERE IS NO WAY TO RESTORE \n"
              "YOUT WALLET AND THE FUNDS in it.\n\n"
              "PLEASE BACK IT UP SECURELY.")
        )
        sizer_1.Add(label_2, 0, wx.ALL, 20)

        self.txt_wallet_seed = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY
        )
        sizer_1.Add(self.txt_wallet_seed, 1, wx.ALL | wx.EXPAND, 20)

        self.SetSizer(sizer_1)

        # self.txt_wallet_seed.Disable()

        self.btn_next = self.FindWindowById(wx.ID_FORWARD)
        self.btn_prev = self.FindWindowById(wx.ID_BACKWARD)
        self.btn_cancel = self.FindWindowById(wx.ID_CANCEL)
        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGED, self.on_page_enter)

    def on_page_enter(self, evt):
        self.btn_cancel.Disable()
        self.SetPrev(None)
