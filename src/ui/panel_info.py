import wx


_ = wx.GetTranslation


class Status(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.StaticText(self, label='')
        sizer.Add(self.text, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 0)

        self.SetSizer(sizer)

    def wallet_opening(self):
        self.text.SetLabel(_('Opening wallet...'))

    def wallet_connecting(self):
        self.text.SetLabel(_('Connecting to daemon...'))

    def wallet_connected(self, synced):
        if synced:
            self.text.SetLabel(_('Connected'))
        else:
            self.text.SetLabel(_('Syncing...'))

    def wallet_error(self, msg):
        self.text.SetLabel(msg)


class InfoPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sizer = wx.BoxSizer(wx.VERTICAL)

        indicator_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.status = Status(self)
        self.bytes = wx.StaticText(self, label='R: 0 / S: 0',
                                   style=wx.ALIGN_CENTER)
        self.bytes.SetToolTip('Received / Sent bytes')
        self.height = wx.StaticText(self, label='Block: 0',
                                    style=wx.ALIGN_RIGHT)
        indicator_sizer.Add(self.status, 0,
                            wx.LEFT | wx.ALIGN_CENTER_VERTICAL,
                            0)
        indicator_sizer.Add(self.bytes, 1, wx.ALIGN_CENTER_VERTICAL)
        indicator_sizer.Add(self.height, 0,
                            wx.ALIGN_CENTER_VERTICAL, 0)

        sizer.Add(indicator_sizer, 0, wx.EXPAND, 0)
        self.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App(False)
    f = wx.Frame(None)
    InfoPanel(f)
    f.Show()
    app.MainLoop()
