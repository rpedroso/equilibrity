import wx


_ = wx.GetTranslation


class ActionPanel(wx.Panel):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        gsizer = wx.BoxSizer(wx.HORIZONTAL)

        gsizer.Add((20, 20), 1, wx.ALL | wx.EXPAND, 0)

        self.btn_receive = wx.Button(self, wx.ID_ANY, _("&Receive"))
        gsizer.Add(self.btn_receive, 0, wx.ALIGN_CENTER, 0)

        self.btn_send = wx.Button(self, wx.ID_ANY, _("&Send"))
        gsizer.Add(self.btn_send, 0, wx.ALIGN_CENTER, 0)

        self.SetSizer(gsizer)

        self.btn_receive.Enable(False)
        self.btn_send.Enable(False)


if __name__ == "__main__":
    app = wx.App(False)
    f = wx.Frame(None)
    ActionPanel(f)
    f.Show()
    app.MainLoop()
