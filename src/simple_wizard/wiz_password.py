import wx
from .page_password import PagePassword
from lib.wallet import Wallet

_ = wx.GetTranslation


class WizPassword(PagePassword):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGED, self.on_enter)
        self.Bind(wx.adv.EVT_WIZARD_BEFORE_PAGE_CHANGED, self.on_leave)

        return None

    def on_leave(self, evt):
        self.parent.options['password'] = self.txt_password.Value
        # self.SetPrev(None)

    def on_enter(self, evt):
        if Wallet.exists():
            self.SetPrev(None)
        evt.Skip()
