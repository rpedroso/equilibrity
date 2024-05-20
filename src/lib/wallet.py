import threading
from equilibria.wallet import WalletManagerFactory, PendingTransaction
import wx
import wx.lib.newevent
from pydispatch import dispatcher


def threaded(fn, *args, **kwargs):
    threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True).start()


def pub_sendMessage(signal, **kwargs):
    wx.CallAfter(dispatcher.send, signal, Wallet, **kwargs)


class Listener:
    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def money_spent(self, tx_id, amount):
        print('money_spent', tx_id, amount)
        pub_sendMessage("EVT_WALLET_MONEY_SPENT", tx_id=tx_id,
                        amount=amount)

    def money_received(self, tx_id, amount):
        print('money_received', tx_id, amount)
        pub_sendMessage("EVT_WALLET_MONEY_RECEIVED", tx_id=tx_id,
                        amount=amount)

    def unconfirmed_money_received(self, tx_id, amount):
        print('unconfirmed_money_received', tx_id, amount)
        pub_sendMessage("EVT_WALLET_UNCONFIRMED_MONEY_RECEIVED", tx_id=tx_id,
                        amount=amount)

    def new_block(self, height):
        # if not Wallet.check_connection():
        #     return
        if height % 9 == 0:
            pub_sendMessage("EVT_WALLET_NEW_BLOCK", height=height)
            return

        if Wallet.synchronized():
            pub_sendMessage("EVT_WALLET_NEW_BLOCK", height=height)

    def updated(self):
        print('updated')

    def refreshed(self):
        if not Wallet.check_connection():
            return
        pub_sendMessage("EVT_WALLET_REFRESHED")


class _Wallet:
    COIN = 10e3
    __wallet = None
    __initialized = False
    is_connected = False

    @property
    def initialized(self):
        return self.__initialized

    @initialized.setter
    def initialized(self, value: bool):
        self.__initialized = value
        pub_sendMessage("EVT_WALLET_INIT")

    def __init__(self):
        super().__init__()
        self.filename = None
        self.language = None
        self.nettype = None
        self.daemon = None
        self.kdf_rounds = None

        self.__history_timer = None

        WalletManagerFactory.set_log_level(WalletManagerFactory.LogLevel.L0)
        self.__wm = WalletManagerFactory.get_wallet_manager()

    def __open(self, filename, passwd, nettype, rounds):  # , listener):
        lt = self.lt = Listener(self)
        self.__wallet = w = self.__wm.open_wallet(filename, passwd,
                                                  nettype, rounds, lt)

        errno, errmsg = w.status_with_error_string()
        if errno:
            pub_sendMessage("EVT_WALLET_OPEN", status=False, reason=errmsg)
        else:
            pub_sendMessage("EVT_WALLET_OPEN", status=True, reason='')

    def open(self, password):
        threaded(self.__open, self.filename, password,
                 self.nettype, self.kdf_rounds)

    def close(self):
        if self.__wallet:
            self.__wm.close_wallet(self.__wallet)
            del self.__wallet
            self._wallet = None

    def __create(self, filename, password, language, nettype, kdf_rounds):
        self.__wallet = w = self.__wm.create_wallet(filename, password,
                                                    language, nettype,
                                                    kdf_rounds)
        errno, errmsg = w.status_with_error_string()
        if errno:
            pub_sendMessage("EVT_WALLET_CREATE", status=False, reason=errmsg)
        else:
            pub_sendMessage("EVT_WALLET_CREATE", status=True, reason='')

    def create(self, password):
        threaded(self.__create, self.filename, password, self.language,
                 self.nettype, self.kdf_rounds)

    def __recover(self, password, mnemonic, restore_height):
        seed_offset = ""
        self.__wallet = w = self.__wm.recovery_wallet(self.filename, password,
                                                      mnemonic,
                                                      self.nettype,
                                                      restore_height,
                                                      self.kdf_rounds,
                                                      seed_offset)
        lt = self.lt = Listener(self)
        w.set_listener(lt)
        errno, errmsg = w.status_with_error_string()
        if errno:
            pub_sendMessage("EVT_WALLET_OPEN", status=False, reason=errmsg)
        else:
            pub_sendMessage("EVT_WALLET_OPEN", status=True, reason='')

    def recover(self, password, mnemonic, restore_height):
        threaded(self.__recover, password, mnemonic, restore_height)

    def __create_from_keys(self, password, restore_height, address,
                           view_key, spend_key):
        self.__wallet = self.__wm.create_wallet_from_keys(
            self.filename, password, self.language, self.nettype,
            restore_height, address, view_key, spend_key, self.kdf_rounds
        )

    def create_from_keys(self, password, restore_height, address,
                         view_key, spend_key=""):
        threaded(self.__create_from_keys, password, restore_height,
                 address, view_key, spend_key)

    def verify_password(self, password):
        no_spend_key = False
        r = self.__wm.verify_wallet_password(self.filename + '.keys',
                                             password, no_spend_key,
                                             self.kdf_rounds)
        return r

    def seed(self):
        return self.__wallet.seed()

    def main_address(self):
        return self.__wallet.main_address()

    def address(self, account_index=0, address_index=0):
        return self.__wallet.address(account_index, address_index)

    def balance(self):
        return self.__wallet.balance_all()

    def account_balance(account_index):
        return self.__wallet.balance(account_index)

    def unlocked_balance(self):
        return self.__wallet.unlocked_balance_all()

    def __history(self):
        h = self.__wallet.history()
        h.refresh()
        pub_sendMessage("EVT_WALLET_HISTORY", h=h)
        return h

    def history(self, refresh=False):
        if not refresh:
            h = self.__wallet.history()
            h.refresh()
            return h

        if self.__history_timer:
            self.__history_timer.Stop()
            self.__history_timer = None

        def __send_event():
            threaded(self.__history)
        self.__history_timer = wx.CallLater(250, __send_event)

    def refresh(self):
        self.__wallet.refresh()

    def store(self):
        def _():
            return self.__wallet.store()
        threaded(_)

    def status(self):
        return self.__wallet.status_with_error_string()

    def __init(self, addr, use_ssl=False):
        r = self.__wallet.init(addr, use_ssl=use_ssl)
        self.__set_daemon(addr)
        self.__wallet.start_refresh()
        self.initialized = r

    def init(self):
        use_ssl = True  # TODO: make configurable
        threaded(self.__init, self.daemon, use_ssl)

    def __set_daemon(self, addr):
        self.__wm.set_daemon_address(addr)
        conn, version = Wallet.daemon_connected()
        Wallet.is_connected = conn
        pub_sendMessage("EVT_WALLET_CONNECT", status=conn,
                        daemon_version=version)

    def set_daemon(self, addr):
        threaded(self.__set_daemon, addr)

    def check_connection(self):
        conn, version = Wallet.daemon_connected()

        if not conn and self.is_connected is True:
            self.is_connected = conn
            pub_sendMessage("EVT_WALLET_CONNECT", status=conn,
                            daemon_version=version)

        elif conn and self.is_connected is False:
            self.is_connected = conn
            pub_sendMessage("EVT_WALLET_CONNECT", status=conn,
                            daemon_version=version)

        if conn:
            return True
        return False

    def connected(self):
        return self.__wallet.connected()

    def daemon_connected(self):
        return self.__wm.connected()

    def exists(self):
        if self.filename is None:
            return False
        return self.__wm.wallet_exists(self.filename)

    def create_transaction(self, dst, amount,
                           priority=PendingTransaction.Priority.Default):
        payment_id = ''
        mixin_count = 15
        suba = 0
        subi = ()
        print(f'sending: "{dst}" "{payment_id}" "{amount}" "{mixin_count}"'
              f'"{priority}" "{suba}" "{subi}"')
        tx = self.__wallet.create_transaction(
                                    dst, payment_id, amount, mixin_count,
                                    priority, suba, subi
                                    )
        return tx

    def create_sweep_unmixable_transaction(self):
        tx = self.__wallet.create_sweep_unmixable_transaction()
        if tx:
            tx.commit()

    def on_daemon_address(self, *args):
        if self.__wallet:
            print(self.__wallet)
            self.deinit()
            self.init()

    def display_amount(self, amount: int):
        return self.__wallet.display_amount(amount)

    def amount_from_string(self, amount):
        return self.__wallet.amount_from_string(amount)

    def blockchain_height(self):
        return self.__wallet.blockchain_height()

    def get_bytes_received(self):
        return self.__wallet.get_bytes_received()

    def get_bytes_sent(self):
        return self.__wallet.get_bytes_sent()

    def status_with_error_string(self):
        if not self.__wallet:
            return None, None
        return self.__wallet.status_with_error_string()

    def set_note(self, txid, note):
        return self.__wallet.set_user_note(txid, note)

    def get_note(self, txid):
        return self.__wallet.get_user_note(txid)

    def synchronized(self):
        if not self.__wallet:
            return False
        return self.__wallet.synchronized()

    def secret_view_key(self):
        return self.__wallet.secret_view_key()

    def public_view_key(self):
        return self.__wallet.public_view_key()

    def secret_spent_key(self):
        return self.__wallet.secret_spent_key()

    def public_spent_key(self):
        return self.__wallet.public_spent_key()

    def max_allowed_amount(self):
        return self.__wallet.maximum_allowed_amount()

    def trusted_daemon(self):
        return self.__wallet.trusted_daemon()

    def daemon_blockchain_height(self):
        return self.__wm.blockchain_height()

    def daemon_blockchain_target_height(self):
        return self.__wm.blockchain_target_height()

    def daemon_network_difficulty(self):
        return self.__wm.network_difficulty()

    def display_nettype(self):
        return {0: 'Mainnet',
                1: 'Testnet',
                2: 'Stagenet',
                }.get(self.__wallet.nettype())

    def display_filename(self):
        return self.__wallet.filename()

    def display_refresh_interval(self):
        return str(self.__wallet.auto_refresh_interval() / 1000)

    def hard_fork_info(self):
        return self.__wallet.hard_fork_info(0)

    def display_mining_hash_rate(self):
        return str(self.__wm.mining_hash_rate())

    def num_subaddress_accounts(self):
        return self.__wallet.num_subaddress_accounts()

    def num_subaddresses(self, account_index):
        return self.__wallet.num_subaddresses(account_index)

    def add_subaddress(self, account_index, label):
        self.__wallet.add_subaddress(account_index, label)

    def get_subaddress_label(self, account_index, address_index):
        return self.__wallet.get_subaddress_label(account_index, address_index)

    def set_subaddress_label(self, account_index, address_index, label):
        self.__wallet.set_subaddress_label(account_index, address_index, label)

Wallet = _Wallet()
