import wx
from lib.wallet import Wallet
from ui.panel_txinfo import TxInfoPanel
from pydispatch import dispatcher


class TxInfo:
    def __init__(self, controller, item_hash):
        self.controller = controller
        self.hash = item_hash
        self.ui = TxInfoPanel(controller.frame, size=(-1, 340))

        h = Wallet.history(refresh=False)
        item = h.transaction_from_str(self.hash)
        self.ui.set_data(item)

        dispatcher.connect(self.on_wallet_history, 'EVT_WALLET_HISTORY')
        self.ui.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED, self.on_close)

    def on_close(self, evt):
        print('**** TxInfo.on_close ***')
        evt.Skip()

    def on_wallet_history(self, h):
        print('**** TxInfo.on_wallet_history ***')
        item = h.transaction_from_str(self.hash)
        self.ui.set_data(item)
