import os
import wx
from .page_seed_restore import PageRestoreSeed
from lib.wallet import Wallet
from lib import config

_ = wx.GetTranslation


class WizSeedRestore(PageRestoreSeed):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGED, self.on_enter)
        self.Bind(wx.adv.EVT_WIZARD_BEFORE_PAGE_CHANGED, self.on_leave)

    def GetNext(self):
        return None

    def SetNext(self, n):
        self.next = n

    def GetPrev(self):
        return self.prev

    def SetPrev(self, p):
        self.prev = p
        if p is None:
            self.btn_prev.Disable()

    def on_leave(self, evt):
        seed = self.txt_wallet_seed.Value
        self.parent.options['seed'] = seed
        self.parent.options['restore_height'] = self.txt_wallet_birthday.Value
        self.parent.options['open_type'] = 'recover'

    def on_enter(self, evt):
        filename = os.path.join(config.get_data_dir(),
                                self.parent.options['wallet_name'])
        Wallet.filename = filename

        self.SetPrev(None)
