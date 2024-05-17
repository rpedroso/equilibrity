import wx
from .page_node import PageNode
# from lib import config
from lib.wallet import Wallet


class WizNode(PageNode):
    def __init__(self, *args, **kw):
        super().__init__(*args, *kw)
        # self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGED, self.on_page_changed)
        self.set_nettype(Wallet.nettype)

        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGING, self.on_page_leave)

    def on_page_leave(self, evt):
        Wallet.nettype = self.get_nettype()
        Wallet.daemon = self.get_daemon_addr()
        evt.Skip()

    # def on_page_enter(self, evt):
    #     print('Wiz3.on_page_changed')
    #     super().on_page_enter(evt)
    #     evt.Skip()

    # def on_page_leave(self, evt):
    #     print('WizNode.on_page_leave')
    #     print(self.get_nettype())
    #     print(self.get_daemon_addr())
    #     print
    #     nettype = self.get_nettype()
    #     addr = self.get_daemon_addr()
    #     cfg_wallet = wx.GetApp().cfg_wallet
    #     config.write_wallet_nettype(cfg_wallet, nettype)
    #     config.write_wallet_daemon(cfg_wallet, addr)
    #     evt.Skip()
