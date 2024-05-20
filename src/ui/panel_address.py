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
        self.col1 = self.lst_address.AppendTextColumn(_('address'), width=300)
        self.col2 = self.lst_address.AppendTextColumn(_('balance'), width=100)
        self.col3 = self.lst_address.AppendTextColumn(
            _('label'), width=100, mode=dv.DATAVIEW_CELL_EDITABLE
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

        # wx.CallAfter(self.init)
        self.init()

    def init(self):
        self._update()
        self.lst_address.SelectRow(0)
        self.btn_add.Enable()
        # self.lst_address.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED,
        #                       self.on_lst_item_changed)
        self.col1.Width = 300
        self.col2.Width = 100
        self.col3.Width = 100

    def on_btn_add(self, evt):
        addr_count = Wallet.num_subaddresses(0)
        Wallet.add_subaddress(0, 'sub address %d' % addr_count)
        self._update()

    def on_lst_edit_done(self, evt):
        # print(dir(evt))
        # print(evt.GetValue())
        # print(evt.GetString())
        # print(evt.GetDataBuffer())
        # print(dir(evt.Model))
        # print(evt.Model.GetValue(evt.Item, 1))

        if evt.Value is None and 'wxGTK' in wx.PlatformInfo:
            return

        lst = evt.EventObject
        col = 1
        row = lst.SelectedRow

        def __(o, row, col):
            value = o.GetValue(row, col)
            print(value)
            Wallet.set_subaddress_label(0, row, value)
        wx.CallAfter(__, evt.EventObject, row, col)

        # store = lst.Store
        # val = store.GetValueByRow(row, col)
        # print('editing', row, val)
        # Wallet.set_subaddress_label(0, row, evt.Value)
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

        # subaddress_set = set()
        h = Wallet.history(refresh=False)
        # for n in range(h.count()):
        #     subaddress_set.add(h.transaction(n).subaddr_index().pop())

        # for n in range(addr_count):
        #     addr = Wallet.address(0, n)
        #     label = Wallet.get_subaddress_label(0, n)
        #     self.lst_address.AppendItem(
        #         (addr, label, 'used' if n in subaddress_set else 'not used')
        #     )

        for n in range(addr_count):
            addr = Wallet.address(0, n)
            label = Wallet.get_subaddress_label(0, n)
            used = 'not used'
            balance = 0

            for tx in h.get_all():
                # print(tx)
                if n in tx.subaddr_index():
                    used = 'used'
                    if tx.is_failed():
                        continue
                    factor = -1 if tx.direction() else 1
                    balance += (tx.amount() + tx.fee()) * factor

            # balance = sum((-1 if tx.direction() else 1) * (tx.amount() + tx.fee())
            #               for tx in txs if n in tx.subaddr_index() and not tx.is_failed())

            balance_str = Wallet.display_amount(balance)
            # print(f'{addr[:6]}  {label}  {balance_str} {used}')
            self.lst_address.AppendItem(
                (addr, balance_str, label, used)
            )


if __name__ == "__main__":
    def on_wallet_open():
        add_pan.btn_add.Enable()
        add_pan.init()

    app = wx.App(False)
    # Wallet.daemon = 'localhost:9331'
    Wallet.nettype = 1
    Wallet.kdf_rounds = 1
    Wallet.filename = '/home/rp/.Equilibrity/Equilibrity-1.wallet'
    Wallet.open('')
    f = wx.Dialog(None, size=(500, 500))
    add_pan = AddressPanel(f)  # , size=(500, 500))
    dispatcher.connect(on_wallet_open, 'EVT_WALLET_OPEN')
    f.ShowModal()
    # app.MainLoop()
    Wallet.close()
