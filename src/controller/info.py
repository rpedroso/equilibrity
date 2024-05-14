import logging
import wx
from lib.wallet import Wallet
from lib import utils
from pydispatch import dispatcher

_ = wx.GetTranslation


class Info:
    def __init__(self, controller):
        self.ui = controller.frame.pan_info
        controller.frame.Bind(wx.EVT_CLOSE, self.on_frame_close)
        dispatcher.connect(self.on_wallet_open, 'EVT_WALLET_OPEN')
        dispatcher.connect(self.on_wallet_refreshed, 'EVT_WALLET_REFRESHED')
        dispatcher.connect(self.on_wallet_new_block, 'EVT_WALLET_NEW_BLOCK')
        dispatcher.connect(self.on_wallet_connect, 'EVT_WALLET_CONNECT')

    def on_frame_close(self, evt):
        logging.debug('Info.on_frame_close')
        evt.Skip()

    def on_wallet_open(self, status, reason):
        logging.debug('Info.on_wallet_open')
        if status is True:
            self.ui.status.wallet_connecting()
            height = Wallet.blockchain_height()
            self.ui.height.SetLabel(_(f'Block: {height}'))
            self.ui.Layout()

    def on_wallet_connect(self, status, daemon_version):
        logging.debug('Info.on_wallet_connect %r %r ', status, daemon_version)
        if status is True:
            self.ui.status.wallet_connected(Wallet.synchronized())
            self.ui.Layout()
        else:
            errno, errmsg = Wallet.status_with_error_string()
            if not errmsg:
                errmsg = _('Failed to connect to daemon')
            self.ui.status.wallet_error(errmsg)
            self.ui.Layout()

    def on_wallet_new_block(self, height):
        self.ui.height.SetLabel(_(f'Block: {height + 1}'))
        # if not Wallet.synchronized() and height % 100 == 0:
        #     self.__bytes_count()
        self.__bytes_count()
        self.ui.Layout()

    def on_wallet_refreshed(self):
        self.ui.status.wallet_connected(Wallet.synchronized())
        height = Wallet.blockchain_height()
        self.ui.height.SetLabel(_(f'Block: {height}'))
        self.__bytes_count()
        self.ui.Layout()

    def __bytes_count(self):
        recv = Wallet.get_bytes_received()
        sent = Wallet.get_bytes_sent()
        recv = utils.sizeof_fmt(recv)
        sent = utils.sizeof_fmt(sent)
        self.ui.bytes.SetLabel(_(f'R: {recv} / S: {sent}'))
