import wx
from ui.panel_view_seed import PanelViewSeed
from lib.wallet import Wallet


class ViewSeed(PanelViewSeed):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)

        wx.CallAfter(self.update)

    def update(self):
        self.txt_wallet_seed.Value = Wallet.seed()
        self.txt_wallet_secret_view.Value = Wallet.secret_view_key()
        self.txt_wallet_public_view.Value = Wallet.public_view_key()
        self.txt_wallet_secret_spent.Value = Wallet.secret_spent_key()
        self.txt_wallet_public_spent.Value = Wallet.public_spent_key()
