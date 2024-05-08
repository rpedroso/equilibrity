from lib.wallet import Wallet
from pydispatch import dispatcher


class Balance:
    def __init__(self, controller):
        self.ui = controller.frame.pan_balance
        dispatcher.connect(self.on_wallet_open, 'EVT_WALLET_OPEN')
        dispatcher.connect(self.on_wallet_new_block, 'EVT_WALLET_NEW_BLOCK')

    def on_wallet_open(self, status, reason):
        print('**** Balance.on_wallet_open ***', status)
        if status is True:
            self.balance_update()

    def on_wallet_new_block(self, height):
        print('**** Balance.on_wallet_new_block ***', height)
        self.balance_update()

    def balance_update(self):
        balance = Wallet.balance()
        ubalance = Wallet.unlocked_balance()
        self.ui.txt_balance.SetValue(Wallet.display_amount(balance))
        self.ui.txt_unlocked_balance.SetValue(
            Wallet.display_amount(ubalance)
        )
