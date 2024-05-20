import wx
import wx.dataview as dv
from lib.wallet import Wallet
from ui.panel_recv import RecvPanel

_ = wx.GetTranslation


class Recv:
    def __init__(self, controller):
        self.controller = controller
        self.ui = RecvPanel(controller.frame, address=Wallet.address(),
                            size=(640, 400))

        self.ui.pan_address.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED,
                                 self.on_pan_address_selection_changed)

    def on_pan_address_selection_changed(self, evt):
        lst = evt.EventObject
        row = lst.SelectedRow
        if row < 0:
            return
        col = 0
        store = lst.Store
        val = store.GetValueByRow(row, col)
        self.ui.set_address(val)
        evt.Skip()
