import sys
import wx
from simple_wizard.wizard import Wizard
from lib.wallet import Wallet


if __name__ == "__main__":
    app = wx.App()
    app.SetAppName("Equilibrity")

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

    w = Wizard(None)
    w.run()
