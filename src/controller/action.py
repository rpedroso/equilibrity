import wx
from lib.wallet import Wallet
from ui.panel_recv import RecvPanel
from controller.send import Send
from pydispatch import dispatcher


class Action:
    def __init__(self, controller):
        self.ui = controller.frame.pan_action
        self.frame = controller.frame
        self.ui.btn_receive.Bind(wx.EVT_BUTTON, self.on_button_recv)
        self.ui.btn_send.Bind(wx.EVT_BUTTON, self.on_button_send)
        dispatcher.connect(self.on_wallet_connect, 'EVT_WALLET_CONNECT')
        dispatcher.connect(self.on_wallet_open, 'EVT_WALLET_OPEN')

    def on_wallet_open(self, status, reason):
        self.ui.btn_receive.Enable(status)

    def on_button_recv(self, evt):
        p = RecvPanel(self.frame, address=Wallet.address(), size=(500, 500))
        p.CenterOnParent()
        p.ShowModal()
        p.Destroy()

    def on_button_send(self, evt):
        p = Send(self)
        p.ui.ShowModal()

    def on_wallet_connect(self, status, daemon_version):
        self.ui.btn_send.Enable(status)
