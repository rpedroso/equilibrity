import wx
# import wx.lib.mixins.listctrl as listmix
import wx.dataview as dv

_ = wx.GetTranslation


# class ListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
#     def __init__(self, *args, **kwargs):
#         wx.ListCtrl.__init__(self, *args, **kwargs)
#         listmix.ListCtrlAutoWidthMixin.__init__(self)
#         self.data = []
#
#     def set_data(self, data):
#         self.SetItemCount(len(data))
#         self.data = data
#
#     def OnGetItemText(self, item, col):
#         if self.data:
#             return self.data[item][col]


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.search = wx.SearchCtrl(self, size=(-1, 28),
                                    style=wx.TE_PROCESS_ENTER)
        self.search.ShowCancelButton(True)
        sizer.Add(self.search, 0, wx.EXPAND, 0)

        # self.txs = ListCtrl(
        #     self,
        #     style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VIRTUAL | wx.LC_VRULES
        # )
        self.txs = DataViewCtrl(self,
                                style=wx.BORDER_THEME
                                | dv.DV_ROW_LINES
                                # | dv.DV_HORIZ_RULES
                                | dv.DV_VERT_RULES
                                # | dv.DV_MULTIPLE
                                )

        # self.model = TXModel(data)
        # self.dvc.AssociateModel(self.model)

        self.txs.AppendTextColumn(_("Status"), 0, width=120)
        self.txs.AppendTextColumn(_("Hash"), 1, width=140)
        self.txs.AppendTextColumn(_("Date"), 2, width=140)
        self.txs.AppendTextColumn(_("Note"), 3, width=120)
        self.txs.AppendTextColumn(_("Amount"), 4, width=120)

        # self.txs.SetColumnWidth(0, 120)
        # self.txs.SetColumnWidth(1, 140)
        # self.txs.SetColumnWidth(2, 140)
        # self.txs.SetColumnWidth(3, 120)
        # self.txs.SetColumnWidth(4, wx.LIST_AUTOSIZE)

        sizer.Add(self.txs, 1, wx.EXPAND, 0)

        self.SetSizer(sizer)


if __name__ == "__main__":
    app = wx.App(False)
    f = wx.Frame(None)
    TxsPanel(f)
    f.Show()
    app.MainLoop()
