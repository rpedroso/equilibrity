import wx
import wx.lib.mixins.listctrl as listmix


_ = wx.GetTranslation


class ListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    pass


class TxInfoPanel(wx.Dialog):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.SetTitle(_("Tx Info"))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.lst_txinfo = ListCtrl(
            self, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES
        )
        self.lst_txinfo.AppendColumn(_("Name"), wx.LIST_FORMAT_LEFT)
        self.lst_txinfo.AppendColumn(_("Value"), wx.LIST_FORMAT_LEFT)

        sizer_1.Add(self.lst_txinfo, 1, wx.EXPAND, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.TOP | wx.BOTTOM, 4)

        self.btn_close = wx.Button(self, wx.ID_CLOSE)
        sizer_2.AddButton(self.btn_close)

        sizer_2.Realize()

        self.SetSizer(sizer_1)

        self.SetEscapeId(self.btn_close.GetId())

    def set_data(self, data):
        self.lst_txinfo.DeleteAllItems()
        idx = 0
        self.lst_txinfo.InsertItem(idx, 'Block Height')
        self.lst_txinfo.SetItem(idx, 1, str(data.block_height()))

        idx += 1
        self.lst_txinfo.InsertItem(idx, 'Hash')
        self.lst_txinfo.SetItem(idx, 1, data.hash())

        idx += 1
        self.lst_txinfo.InsertItem(idx, 'Timestamp')
        self.lst_txinfo.SetItem(idx, 1, str(data.timestamp()))

        idx += 1
        self.lst_txinfo.InsertItem(idx, _('Confirmations'))
        self.lst_txinfo.SetItem(idx, 1, str(data.confirmations()))

        idx += 1
        self.lst_txinfo.InsertItem(idx, _('Payment Id'))
        self.lst_txinfo.SetItem(idx, 1, data.payment_id())

        idx += 1
        self.lst_txinfo.InsertItem(idx, _('Fee'))
        self.lst_txinfo.SetItem(idx, 1, str(data.fee()))

        idx += 1
        self.lst_txinfo.InsertItem(idx, _('Amount'))
        self.lst_txinfo.SetItem(idx, 1, str(data.amount()))

        idx += 1
        self.lst_txinfo.InsertItem(idx, _('Unlock Time'))
        self.lst_txinfo.SetItem(idx, 1, str(data.unlock_time()))

        idx += 1
        self.lst_txinfo.InsertItem(idx, _('SN reward?'))
        self.lst_txinfo.SetItem(idx, 1, str(data.is_service_node_reward()))

        idx += 1
        self.lst_txinfo.InsertItem(idx, _('Miner reward?'))
        self.lst_txinfo.SetItem(idx, 1, str(data.is_miner_reward()))

        self.lst_txinfo.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        self.lst_txinfo.SetColumnWidth(1, wx.LIST_AUTOSIZE)


if __name__ == "__main__":
    app = wx.App()
    data = [('Name 1', 'Value 1'),
            ('Name 2', 'Value 2')]
    p = TxInfoPanel(None)
    p.set_data(data)
    p.ShowModal()