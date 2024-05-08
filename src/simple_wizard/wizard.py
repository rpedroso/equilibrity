import wx
import wx.adv
from wx.adv import Wizard as wiz
from .wiz_password import WizPassword
from .wiz_wallet import WizWallet
from .wiz_seed import WizSeed
from .wiz_seed_restore import WizSeedRestore
from lib.wallet import Wallet

_ = wx.GetTranslation


class Wizard(wiz):
    def __init__(self, parent):

        app = wx.GetApp()
        name = app.GetAppName()
        nettype = Wallet.nettype
        self.options = {
            'wallet_name': f'{name}-{nettype}.wallet',
        }

        bitmaps = [wx.Bitmap('images/wiz.jpg')]
        bb = wx.BitmapBundle.FromBitmaps(bitmaps)

        super().__init__(parent, title=_("Equilibrity Wizard"), bitmap=bb)

        self.page_password = WizPassword(self)
        self.page_wallet = WizWallet(self)
        self.page_seed = WizSeed(self)
        self.page_seed_restore = WizSeedRestore(self)

        # Set the initial order of the pages
        self.page_password.SetNext(self.page_wallet)

        self.page_wallet.SetPrev(self.page_password)
        self.page_wallet.SetNext(None)

        self.page_seed.SetPrev(self.page_wallet)
        self.page_seed.SetNext(None)

        self.page_seed_restore.SetPrev(self.page_wallet)
        self.page_seed_restore.SetNext(None)

        self.GetPageAreaSizer().Add(self.page_password)

    def run(self):
        ret = self.RunWizard(self.page_password)
        if not ret:
            self.options = {}


if __name__ == '__main__':
    app = wx.App()
    app.SetAppName("Equilibrity")

    w = Wizard(None)
    w.run()
