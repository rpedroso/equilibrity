import wx
import wx.dataview as dv
from lib.wallet import Wallet
from pydispatch import dispatcher

_ = wx.GetTranslation


class AddressPanel(wx.Panel):
    def __init__(self, parent, size=(-1, -1)):
        super().__init__(parent, size=size)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.lst_address = dv.DataViewListCtrl(self)
        self.col1 = self.lst_address.AppendTextColumn(_('address'), width=250)
        self.col2 = self.lst_address.AppendTextColumn(
            _('label'), width=150, mode=dv.DATAVIEW_CELL_EDITABLE
        )
        self.lst_address.AppendTextColumn(_('used?'))  # , width=100)

        self.btn_add = wx.Button(self, id=wx.ID_ADD)
        self.btn_add.Disable()

        sizer_1.Add(self.lst_address, 1, wx.EXPAND, 0)
        sizer_1.Add(self.btn_add, 0, 0, 0)

        self.SetSizer(sizer_1)

        self.btn_add.Bind(wx.EVT_BUTTON, self.on_btn_add)
        self.lst_address.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE,
                              self.on_lst_edit_done)

        wx.CallAfter(self.init)
        # self.init()

    def init(self):
        self._update()
        self.lst_address.SelectRow(0)
        self.btn_add.Enable()
        # self.lst_address.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED,
        #                       self.on_lst_item_changed)
        self.col1.Width = 300
        self.col2.Width = 100

    def on_btn_add(self, evt):
        addr_count = Wallet.num_subaddresses(0)
        Wallet.add_subaddress(0, 'sub address %d' % addr_count)
        self._update()

    def on_lst_edit_done(self, evt):
        # print(dir(evt))
        # print(evt.GetValue())
        if evt.Value is None:
            return

        lst = evt.EventObject
        row = lst.SelectedRow
        # col = 0
        # store = lst.Store
        # val = store.GetValueByRow(row, col)
        # print(val)
        Wallet.set_subaddress_label(0, row, evt.Value)
        # evt.Skip()

    # def on_lst_item_changed(self, evt):
    #     print('aqui')

    def _update(self):
        self.lst_address.DeleteAllItems()
        # Wallet.add_subaddress(0, 'sub address 1')
        # acc_count = Wallet.num_subaddress_accounts()
        # print(acc_count)
        addr_count = Wallet.num_subaddresses(0)
        # print(addr_count)
        # print(Wallet.address(0, 0))
        # print(Wallet.address(0, 1))

        subaddress_set = set()
        h = Wallet.history(refresh=False)
        for n in range(h.count()):
            subaddress_set.add(h.transaction(n).subaddr_index().pop())

        for n in range(addr_count):
            addr = Wallet.address(0, n)
            label = Wallet.get_subaddress_label(0, n)
            self.lst_address.AppendItem(
                (addr, label, 'used' if n in subaddress_set else 'not used')
            )


if __name__ == "__main__":
    def on_wallet_open():
        add_pan.btn_add.Enable()
        add_pan._update()

    app = wx.App(False)
    # Wallet.daemon = 'localhost:9331'
    Wallet.nettype = 1
    Wallet.kdf_rounds = 1
    Wallet.filename = '/home/rp/.Equilibrity/Equilibrity-1.wallet'
    Wallet.open('')
    f = wx.Dialog(None, size=(500, 500))
    add_pan = AddressPanel(f)  # , size=(500, 500))
    f.ShowModal()
    dispatcher.connect(on_wallet_open, 'EVT_WALLET_OPEN')
    # app.MainLoop()
    Wallet.close()
