import wx
import wx.lib.mixins.listctrl as listmix

_ = wx.GetTranslation


class ListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.data = []

    def set_data(self, data):
        self.SetItemCount(len(data))
        self.data = data

    def OnGetItemText(self, item, col):
        if self.data:
            return self.data[item][col]


class TxsPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.search = wx.SearchCtrl(self, size=(-1, 28),
                                    style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        sizer.Add(self.search, 0, wx.EXPAND, 0)

        self.txs = ListCtrl(
            self,
            style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_VRULES
        )
        self.txs.AppendColumn(_("Status"), wx.LIST_FORMAT_LEFT)
        self.txs.AppendColumn(_("Hash"), wx.LIST_FORMAT_LEFT)
        self.txs.AppendColumn(_("Date"), wx.LIST_FORMAT_LEFT)
        self.txs.AppendColumn(_("Note"), wx.LIST_FORMAT_LEFT)
        self.txs.AppendColumn(_("Amount"), wx.LIST_FORMAT_LEFT)

        self.txs.SetColumnWidth(0, 120)
        self.txs.SetColumnWidth(1, 140)
        self.txs.SetColumnWidth(2, 140)
        self.txs.SetColumnWidth(3, 120)
        self.txs.SetColumnWidth(4, wx.LIST_AUTOSIZE)

        sizer.Add(self.txs, 1, wx.EXPAND, 0)

        self.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App(False)
    f = wx.Frame(None)
    TxsPanel(f)
    f.Show()
    app.MainLoop()
