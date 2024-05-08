import wx
from ui.panel_properties import PanelProperties
from lib.wallet import Wallet
from pydispatch import dispatcher


class Properties(PanelProperties):
    def __init__(self, parent):
        super().__init__(parent)
        wx.CallAfter(self.update)

        dispatcher.connect(self.on_wallet_new_block, 'EVT_WALLET_NEW_BLOCK')
        dispatcher.connect(self.on_wallet_refreshed, 'EVT_WALLET_REFRESHED')

    def update(self):
        self.txt_wallet_network.Value = Wallet.display_nettype()
        self.txt_wallet_filename.Value = Wallet.display_filename()
        self.txt_wallet_height.Value = str(Wallet.blockchain_height())
        self.txt_wallet_sync.Value = str(Wallet.synchronized())
        self.txt_wallet_txs_count.Value = str(Wallet.history(False).count())
        self.txt_wallet_refresh_interval.Value = \
            Wallet.display_refresh_interval()
        self.txt_wallet_max_allowed_amount.Value = \
            str(Wallet.max_allowed_amount())

        self.txt_daemon_trusted.Value = str(Wallet.trusted_daemon())
        self.txt_daemon_address.Value = str(Wallet.daemon)
        self.txt_daemon_hardfork_info.Value = \
            str(Wallet.hard_fork_info())
        self.txt_daemon_mining_hash_rate.Value = \
            Wallet.display_mining_hash_rate()
        self.txt_daemon_blockchain_height.Value = \
            str(Wallet.daemon_blockchain_height())
        self.txt_daemon_blockchain_target_height.Value = \
            str(Wallet.daemon_blockchain_target_height())
        self.txt_daemon_network_difficulty.Value = \
            str(Wallet.daemon_network_difficulty())
        ver = Wallet.daemon_connected()[1]
        self.txt_core_rpc_version.Value = "%d.%d" % (ver >> 16,
                                                     ver >> 16 & ver)

    def on_wallet_new_block(self, height):
        print('*** Properties.on_wallet_new_block ***')
        self.txt_wallet_height.Value = str(Wallet.blockchain_height())
        self.txt_wallet_txs_count.Value = str(Wallet.history(False).count())

        self.txt_daemon_blockchain_height.Value = \
            str(Wallet.daemon_blockchain_height())
        self.txt_daemon_network_difficulty.Value = \
            str(Wallet.daemon_network_difficulty())
        self.txt_daemon_blockchain_target_height.Value = \
            str(Wallet.daemon_blockchain_target_height())

    def on_wallet_refreshed(self):
        print('*** Properties.on_wallet_refreshed ***')
        self.txt_wallet_sync.Value = str(Wallet.synchronized())

        ver = Wallet.daemon_connected()[1]
        self.txt_core_rpc_version.Value = "%d.%d" % (ver >> 16,
                                                     ver >> 16 & ver)
