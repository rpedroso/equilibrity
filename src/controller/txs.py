import wx
from lib.wallet import Wallet
from controller.txinfo import TxInfo
from datetime import datetime
from pydispatch import dispatcher

_ = wx.GetTranslation


class Txs:
    def __init__(self, controller):
        self.controller = controller
        self.data = []
        self.ui = controller.frame.pan_txs
        self.ui.txs.Bind(wx.EVT_LIST_ITEM_ACTIVATED,
                         self.on_lst_intem_activated)
        dispatcher.connect(self.on_wallet_open, 'EVT_WALLET_OPEN')
        dispatcher.connect(self.on_wallet_new_block, 'EVT_WALLET_NEW_BLOCK')
        dispatcher.connect(self.on_wallet_history, 'EVT_WALLET_HISTORY')

        self.ui.search.Bind(wx.EVT_TEXT_ENTER, self.on_search)
        self.ui.search.Bind(wx.EVT_TEXT, self.on_search)
        self.ui.search.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN,
                            lambda e: self.ui.search.SetValue(''))

    def on_lst_intem_activated(self, evt):
        self.currentItem = idx = evt.Index
        item = self.data[idx][1]
        txinfo = TxInfo(self.controller, item)
        txinfo.ui.ShowModal()
        txinfo.ui.Destroy()

    def on_search(self, evt=None):
        value = self.ui.search.GetValue().lower()
        if not value:
            self.ui.txs.set_data(self.data)
            return

        data = []
        for v in self.data:
            if value in ' '.join(str(s) for s in v).lower():
                data.append(v)

        self.ui.txs.set_data(data)

        if evt:
            evt.Skip()

    def on_wallet_open(self, status, reason):
        print('**** Txs.on_wallet_open ***')
        if status is True:
            Wallet.history(refresh=True)

    def on_wallet_new_block(self, height):
        Wallet.history(refresh=True)

    def on_wallet_history(self, h):
        print('**** Txs.on_wallet_history ***')
        hlist = sorted(h.get_all(), key=lambda x: x.timestamp(), reverse=True)
        data = []
        for item in hlist:
            if item.is_pending():
                status = _('pending')
            elif item.is_failed():
                status = _('failed')
            else:
                n = item.confirmations()
                if n < 10:
                    status = '%d %s' % (10 - n, _('block(s) to unlock'))
                else:
                    status = _('confirmed')
            amount = Wallet.display_amount(item.amount())
            data.append((
                status,
                item.hash(),
                str(datetime.fromtimestamp(item.timestamp())),
                Wallet.get_note(item.hash()),
                f"-{amount}" if item.direction() else f"+{amount}",
                ))

        self.data = data
        self.on_search()
        # self.ui.txs.set_data(data)
