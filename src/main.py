import sys
import os
import logging
import wx
# from pprint import pprint
from wx.adv import SplashScreen as SplashScreen
# from settings import APPNAME
from lib import config
from lib.utils import resource_path

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
opj = os.path.join

APPNAME = 'Equilibrity'
PREFS_FILENAME = 'prefs-%d.ini'


def show_splash():
    # create, show and return the splash screen
    style = wx.adv.SPLASH_CENTRE_ON_SCREEN | wx.adv.SPLASH_NO_TIMEOUT
    bitmap = wx.Bitmap(resource_path('images/splash.png'))
    wx.Bitmap.Rescale(bitmap, (300, 300))
    splash = SplashScreen(bitmap,
                          splashStyle=style,
                          milliseconds=3000,
                          parent=None,
                          )
    wx.SafeYield()
    return splash


class Equilibrity(wx.App):

    def OnInit(self):
        self.SetAppName(APPNAME)

        splash = show_splash()
        self.splash = splash

        self.cfg = None
        self.wallet_filename = None

        wx.CallLater(100, self.imports)
        return True

    def imports(self):
        global Wallet
        # import equilibria.wallet  # noqa
        from controller.main import Controller
        from lib.wallet import Wallet

        args = dict((x, a) for x, a in enumerate(sys.argv))
        arg1 = args.get(1, 0)
        try:
            nettype = int(arg1)
        except ValueError:
            raise SystemExit('Nettype invalid. Must be 0, 1 or 2')

        if nettype == 0:
            Wallet.daemon = 'localhost:9231'
        elif nettype == 1:
            Wallet.daemon = 'localhost:9331'
        elif nettype == 2:
            Wallet.daemon = 'localhost:9431'
        else:
            raise SystemExit('Nettype invalid. Must be 0, 1 or 2')

        Wallet.nettype = nettype
        Wallet.language = 'English'
        Wallet.kdf_rounds = 1

        prefs_filename = PREFS_FILENAME % nettype
        self.cfg = config.get_config(prefs_filename)
        if not config.exists(prefs_filename):
            config.mkdir()
            options = self.run_wizard()
        else:
            options = {}
            self.read_config_file()

        Controller(self, options)

    def read_config_file(self):
        cfg = self.cfg

        Wallet.filename = cfg.Read('wallet/file')
        Wallet.nettype = cfg.ReadInt('wallet/nettype')
        Wallet.daemon = cfg.Read('wallet/daemon')

    def save_config_file(self, options):
        cfg = self.cfg
        cfg.Write('wallet/file', Wallet.filename)
        cfg.WriteInt('wallet/nettype', Wallet.nettype)
        cfg.Write('wallet/daemon', Wallet.daemon)
        cfg.Flush()

    def run_wizard(self):
        from simple_wizard import wizard
        wiz = wizard.Wizard(None)
        self.splash.Destroy()
        wiz.run()
        options = wiz.options.copy()
        wiz.Destroy()
        if not options:
            raise SystemExit
        return options


def main():
    app = Equilibrity(False)
    app.MainLoop()


if __name__ == '__main__':
    main()
