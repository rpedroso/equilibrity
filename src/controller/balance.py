import logging
from lib.wallet import Wallet
from pydispatch import dispatcher


class Balance:
    def __init__(self, controller):
        self.ui = controller.frame.pan_balance
        dispatcher.connect(self.on_wallet_open, 'EVT_WALLET_OPEN')
        dispatcher.connect(self.on_wallet_history, 'EVT_WALLET_HISTORY')
        dispatcher.connect(self.on_wallet_unconfirmed_money_received,
                           'EVT_WALLET_UNCONFIRMED_MONEY_RECEIVED')

    def on_wallet_open(self, status, reason):
        logging.debug('Balance.on_wallet_open %r', status)
        if status is True:
            self.balance_update()

    def on_wallet_history(self):
        logging.debug('Balance.on_wallet_history')
        self.balance_update()

    def on_wallet_unconfirmed_money_received(self, tx_id, amount):
        logging.debug('Balance.on_unconfirmed_money_received')
        self.balance_update()

    def balance_update(self):
        balance = Wallet.balance()
        ubalance = Wallet.unlocked_balance()
        self.ui.txt_balance.SetValue(Wallet.display_amount(balance))
        self.ui.txt_unlocked_balance.SetValue(
            Wallet.display_amount(ubalance)
        )
