import wx
from lib.wallet import Wallet
from ui.panel_send import SendPanel

_ = wx.GetTranslation


class Send:
    def __init__(self, controller):
        self.controller = controller
        self.ui = SendPanel(controller.frame, size=(-1, 340))
        self.ui.CenterOnParent()

        self.ui.btn_send.Bind(wx.EVT_BUTTON, self.on_btn_send)
        self.ui.btn_amount_max.Bind(wx.EVT_BUTTON, self.on_btn_amount_max)

    def on_btn_send(self, evt):
        try:
            amount = Wallet.amount_from_string(self.ui.txt_amount.Value)
        except ValueError:
            amount = 0
        to = self.ui.txt_to.GetValue()
        note = self.ui.txt_note.GetValue()
        priority = self.ui.ch_priority.Selection
        tx = Wallet.create_transaction(to, amount, priority)
        if tx.status():
            wx.MessageBox(tx.error_string(), _('Error'), parent=self.ui,
                          style=wx.ICON_ERROR)
            return
        text = (f"""Send to: {to}
Amount: {Wallet.display_amount(amount)}
Fee: {Wallet.display_amount(tx.fee())}
TxId: {tx.tx_id()}
""")
        dlg = wx.MessageDialog(self.ui, text,
                               _('Confirm transaction'),
                               wx.YES_NO
                               | wx.NO_DEFAULT
                               | wx.ICON_INFORMATION
                               )
        ret = dlg.ShowModal()
        if ret == wx.ID_YES:
            Wallet.set_note(tx.tx_id()[0], note)
            tx.commit()
            # evt.Skip()
            dlg.Destroy()
            self.ui.Destroy()
            Wallet.history(refresh=True)

    def on_btn_amount_max(self, evt):
        self.ui.txt_amount.Value = Wallet.display_amount(Wallet.balance())
