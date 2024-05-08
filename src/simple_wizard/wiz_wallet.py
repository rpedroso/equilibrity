import wx
from .page_wallet import PageWallet

_ = wx.GetTranslation


class WizWallet(PageWallet):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def GetNext(self):
        if self.rd_wallet_new.GetValue():
            self.next = self.parent.page_seed
            self.next.SetPrev(self)
        else:
            self.next = self.parent.page_seed_restore
            self.next.SetPrev(self)
        return self.next

    def SetNext(self, n):
        self.next = n

    def GetPrev(self):
        return self.prev

    def SetPrev(self, p):
        self.prev = p
