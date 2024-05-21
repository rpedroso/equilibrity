import wx
# import wx.lib.mixins.listctrl as listmix
import wx.dataview as dv
from lib.wallet import Wallet

_ = wx.GetTranslation


class TXModel(dv.DataViewIndexListModel):
    def __init__(self, data):
        dv.DataViewIndexListModel.__init__(self, len(data))
        self.data = data

    # All of our columns are strings.  If the model or the renderers
    # in the view are other types then that should be reflected here.
    def GetColumnType(self, col):
        return "string"

    def GetValueByRow(self, row, col):
        return self.data[row][col]

    def GetCount(self):
        # self.log.write('GetCount')
        return len(self.data)

    def GetAttrByRow(self, row, col, attr):
        return False

    def AddRow(self, value):
        # update data structure
        self.data.append(value)
        # notify views
        self.RowAppended()


class DataViewCtrl(dv.DataViewCtrl):
    def set_data(self, data):
        self.model = TXModel(data)
        self.AssociateModel(self.model)


class TxsPanel(wx.Panel):
    TP_OPEN_EXPLORER_ID = wx.NewIdRef()
    TP_TX_INFO = wx.NewIdRef()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.search = wx.SearchCtrl(self, size=(-1, 28),
                                    style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        sizer.Add(self.search, 0, wx.EXPAND, 0)

        self.txs = DataViewCtrl(self, style=dv.DV_ROW_LINES)

        self.txs.AppendTextColumn(_("Status"), 0, width=120)
        self.txs.AppendTextColumn(_("Hash"), 1, width=140)
        self.txs.AppendTextColumn(_("Date"), 2, width=140)
        self.txs.AppendTextColumn(_("Note"), 3, width=120)
        self.txs.AppendTextColumn(_("Amount"), 4, width=120)

        sizer.Add(self.txs, 1, wx.EXPAND, 0)

        self.SetSizer(sizer)

        self.txs.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU,
                      self.on_lst_item_context_menu)

        if Wallet.nettype == 0:
            self.Bind(wx.EVT_MENU, self.on_open_explorer,
                      id=self.TP_OPEN_EXPLORER_ID)

    def on_lst_item_context_menu(self, evt):
        item = self.txs.GetSelection()
        menu = wx.Menu()
        mitem = menu.Append(self.TP_OPEN_EXPLORER_ID, _("Open in explorer"))
        mitem.Enable(False if item.ID is None or Wallet.nettype != 0 else True)
        mitem = menu.Append(self.TP_TX_INFO, _("Tx info"))
        mitem.Enable(False if item.ID is None else True)
        self.PopupMenu(menu)
        menu.Destroy()

    def on_open_explorer(self, evt):
        import webbrowser
        item = self.txs.GetSelection()
        if item.ID is None:
            # This should never happen because we disable
            # the menu items when there is no selection
            dlg = wx.MessageDialog(self, "Please select a transaction",
                                   "Error", wx.CLOSE | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        model = self.txs.Model
        _hash = model.GetValue(item, 1)
        # print(_hash)
        url = f'https://explorer.equilibriacc.com/tx/{_hash}'
        webbrowser.open(url)


if __name__ == "__main__":
    app = wx.App(False)
    f = wx.Frame(None)
    TxsPanel(f)
    f.Show()
    app.MainLoop()
