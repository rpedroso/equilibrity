import wx

_ = wx.GetTranslation


class BalancePanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        bmp = wx.Bitmap("images/equilibria.png", wx.BITMAP_TYPE_ANY)
        bmp_logo = wx.GenericStaticBitmap(self, wx.ID_ANY)
        bmp_logo.SetMinSize((100, 100))
        bmp_logo.SetScaleMode(bmp_logo.Scale_AspectFit)
        bmp_logo.SetBitmap(bmp)
        sizer.Add(bmp_logo, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        sizer.Add((20, 20), 1, wx.ALL | wx.EXPAND, 0)

        gsizer = wx.FlexGridSizer(2, 2, 12, 12)

        label_1 = wx.StaticText(self, wx.ID_ANY, _("Balance"))
        label_1.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_NORMAL, 0, ""))
        gsizer.Add(label_1, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.txt_balance = wx.TextCtrl(
            self, wx.ID_ANY, "",
            style=wx.BORDER_NONE | wx.TE_READONLY | wx.TE_RIGHT
        )
        self.txt_balance.SetFont(wx.Font(12,
                                         wx.FONTFAMILY_DEFAULT,
                                         wx.FONTSTYLE_NORMAL,
                                         wx.FONTWEIGHT_NORMAL, 0, ""))
        gsizer.Add(self.txt_balance, 1, wx.EXPAND, 3)

        label_2 = wx.StaticText(self, wx.ID_ANY, _("Unlocked"))
        label_2.SetFont(wx.Font(14,
                                wx.FONTFAMILY_DEFAULT,
                                wx.FONTSTYLE_NORMAL,
                                wx.FONTWEIGHT_NORMAL, 0, ""))
        gsizer.Add(label_2, 0, wx.ALIGN_CENTER_VERTICAL, 0)

        self.txt_unlocked_balance = wx.TextCtrl(
            self,
            wx.ID_ANY, "",
            style=wx.BORDER_NONE | wx.TE_READONLY | wx.TE_RIGHT
        )
        self.txt_unlocked_balance.SetFont(wx.Font(12,
                                                  wx.FONTFAMILY_DEFAULT,
                                                  wx.FONTSTYLE_NORMAL,
                                                  wx.FONTWEIGHT_NORMAL,
                                                  0, ""))
        gsizer.Add(self.txt_unlocked_balance, 1, wx.EXPAND, 0)

        gsizer.AddGrowableCol(1)
        sizer.Add(gsizer, 3, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 0)

        self.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App(False)
    f = wx.Frame(None)
    BalancePanel(f)
    f.Show()
    app.MainLoop()
