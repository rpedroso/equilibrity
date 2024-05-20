import wx
import wx.dataview as dv
from lib.wallet import Wallet
from pydispatch import dispatcher

_ = wx.GetTranslation


class AddressPanel(wx.Panel):
    AP_COPY_ADDR_ID = wx.NewIdRef()
    AP_COPY_LABEL_ID = wx.NewIdRef()
    def __init__(self, parent, size=(-1, -1)):
        super().__init__(parent, size=size)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)

        self.lst_address = dv.DataViewListCtrl(self)
        self.col1 = self.lst_address.AppendTextColumn(_('address'), width=260)
        self.col2 = self.lst_address.AppendTextColumn(
            _('label'), width=100, mode=dv.DATAVIEW_CELL_EDITABLE
        )
        self.lst_address.AppendTextColumn(_('used?'))  # , width=100)

        add_bmp = wx.ArtProvider.GetBitmapBundle(wx.ART_PLUS,
                                                 wx.ART_TOOLBAR, (24, 24))
        self.btn_add = wx.BitmapButton(self, wx.ID_ADD, add_bmp)
        self.btn_add.ToolTip = _('Add subaddress (label can be edited in the '
                                 'list)')
        self.btn_add.Disable()

        copy_bmp = wx.ArtProvider.GetBitmapBundle(wx.ART_COPY,
                                                  wx.ART_TOOLBAR, (24, 24))
        self.btn_copy = wx.BitmapButton(self, wx.ID_ANY, copy_bmp)
        self.btn_copy.ToolTip = _('Copy selected address')
        self.btn_copy.SetSize(self.btn_copy.GetBestSize())

        sizer_2.Add(self.btn_add, 0, 0, 0)
        sizer_2.Add(self.btn_copy, 0, 0, 0)

        sizer_1.Add(self.lst_address, 1, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)

        self.SetSizer(sizer_1)

        self.btn_add.Bind(wx.EVT_BUTTON, self.on_btn_add)
        self.lst_address.Bind(dv.EVT_DATAVIEW_ITEM_EDITING_DONE,
                              self.on_lst_edit_done)

        self.lst_address.Bind(wx.EVT_MOUSE_EVENTS, self.on_lst_mouse_events)

        # wx.CallAfter(self.init)
        self.init()

    def init(self):
        self._update()
        self.lst_address.SelectRow(0)
        self.btn_add.Enable()
        self.col1.Width = 260
        self.col2.Width = 100

    def on_btn_add(self, evt):
        addr_count = Wallet.num_subaddresses(0)
        Wallet.add_subaddress(0, 'sub address %d' % addr_count)
        self._update()

    def on_lst_edit_done(self, evt):
        if evt.Value is None and 'wxGTK' in wx.PlatformInfo:
            return

        lst = evt.EventObject
        col = 1
        row = lst.SelectedRow

        def __(o, row, col):
            value = o.GetValue(row, col)
            Wallet.set_subaddress_label(0, row, value)
        wx.CallAfter(__, evt.EventObject, row, col)

    def on_lst_mouse_events(self, evt):
        if not evt.RightUp():
            evt.Skip()
            return

        menu = wx.Menu()
        menu.Append(AddressPanel.AP_COPY_ADDR_ID, _("Copy address"))
        menu.Append(AddressPanel.AP_COPY_LABEL_ID, _("Copy label"))
        self.PopupMenu(menu)
        menu.Destroy()

    def _update(self):
        self.lst_address.DeleteAllItems()

        h = Wallet.history(refresh=False)

        subaddress_set = set()
        for tx in h.get_all():
            idx = tx.subaddr_index()
            subaddress_set.update(idx)

        addr_count = Wallet.num_subaddresses(0)
        for n in range(addr_count):
            addr = Wallet.address(0, n)
            label = Wallet.get_subaddress_label(0, n)
            self.lst_address.AppendItem(
                (addr, label, 'used' if n in subaddress_set else 'not used')
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
