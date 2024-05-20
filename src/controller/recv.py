import wx
import wx.dataview as dv
from lib.wallet import Wallet
from ui.panel_recv import RecvPanel

_ = wx.GetTranslation


class Recv:
    def __init__(self, controller):
        self.controller = controller
        self.ui = RecvPanel(controller.frame, address=Wallet.address(),
                            size=(500, 500))

        # self.ui.btn_send.Bind(wx.EVT_BUTTON, self.on_btn_send)
        # self.ui.btn_amount_max.Bind(wx.EVT_BUTTON, self.on_btn_amount_max)
        self.ui.pan_address.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED,
                                 self.on_pan_address_selection_changed)

    def on_pan_address_selection_changed(self, evt):
        # print('aqui')
        # print(dir(evt))
        # print(evt.GetValue())
        # if evt.Value is None:
        #     return

        lst = evt.EventObject
        row = lst.SelectedRow
        if row < 0:
            return
        col = 0
        store = lst.Store
        val = store.GetValueByRow(row, col)
        print(val)
        self.ui.set_address(val)
        # Wallet.set_subaddress_label(0, row, evt.Value)
        # evt.Skip()
