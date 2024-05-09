import os
import logging
import wx
from .page_seed import PageSeed
from lib.wallet import Wallet
from lib import config
from pydispatch import dispatcher

_ = wx.GetTranslation


class WizSeed(PageSeed):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.Disable()
        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGED, self.on_enter)
        dispatcher.connect(self.on_wallet_create, 'EVT_WALLET_CREATE')


    def GetNext(self):
        return self.next

    def SetNext(self, n):
        self.next = n

    def GetPrev(self):
        return self.prev

    def SetPrev(self, p):
        if p is None:
            self.btn_prev.Disable()
        self.prev = p

    def on_enter(self, evt):
        filename = os.path.join(config.get_data_dir(),
                                self.parent.options['wallet_name'])
        self.SetPrev(None)
        self.btn_next.Disable()
        self.txt_wallet_seed.SetValue(_('Generating seed... Please wait.'))
        Wallet.filename = filename
        # print(Wallet.filename)
        password = self.parent.options['password']
        Wallet.create(password)

    def on_wallet_create(self, status, reason):
        logging.debug('WizSeed.on_wallet_create')
        if status is True:
            self.Enable()
            self.btn_next.Enable()
            self.btn_cancel.Disable()
            self.txt_wallet_seed.SetValue(Wallet.seed())
        else:
            self.btn_cancel.Enable()
            wx.MessageBox(reason, _("Error"),
                          parent=self, style=wx.ICON_ERROR)
            raise SystemExit
