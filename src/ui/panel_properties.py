import wx

_ = wx.GetTranslation


class PanelProperties(wx.Dialog):
    def __init__(self, parent):
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX
        super().__init__(parent, style=style)
        self.SetMinSize((450, 550))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.StaticBoxSizer(
            wx.StaticBox(self, wx.ID_ANY, _("Wallet")), wx.VERTICAL
        )
        sizer_1.Add(sizer_2, 1, wx.ALL | wx.EXPAND, 12)

        grid_sizer_2 = wx.FlexGridSizer(7, 2, 4, 4)
        sizer_2.Add(grid_sizer_2, 1, wx.ALL | wx.EXPAND, 12)

        label_11 = wx.StaticText(self, wx.ID_ANY, _("Network:"))
        grid_sizer_2.Add(label_11, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_wallet_network = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_2.Add(self.txt_wallet_network, 0, wx.EXPAND, 0)

        label_12 = wx.StaticText(self, wx.ID_ANY, _("Filename:"),
                                 style=wx.ALIGN_RIGHT)
        grid_sizer_2.Add(label_12, 0, wx.ALIGN_CENTER_VERTICAL | wx.EXPAND, 0)

        self.txt_wallet_filename = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_2.Add(self.txt_wallet_filename, 0, wx.EXPAND, 0)

        label_13 = wx.StaticText(self, wx.ID_ANY, _("Height:"))
        grid_sizer_2.Add(label_13, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_wallet_height = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_2.Add(self.txt_wallet_height, 0, wx.EXPAND, 0)

        label_14 = wx.StaticText(self, wx.ID_ANY, _("Syncronized:"))
        grid_sizer_2.Add(label_14, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_wallet_sync = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY)
        grid_sizer_2.Add(self.txt_wallet_sync, 0, wx.EXPAND, 0)

        label_15 = wx.StaticText(self, wx.ID_ANY, _("Txs count:"))
        grid_sizer_2.Add(label_15, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_wallet_txs_count = wx.TextCtrl(
            self, wx.ID_ANY, "", style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_2.Add(self.txt_wallet_txs_count, 0, wx.EXPAND, 0)

        label_16 = wx.StaticText(self, wx.ID_ANY, _("Refresh interval:"))
        grid_sizer_2.Add(label_16, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_wallet_refresh_interval = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_2.Add(self.txt_wallet_refresh_interval, 0, wx.EXPAND, 0)

        label_17 = wx.StaticText(self, wx.ID_ANY, _("Max. allowed amount"))
        grid_sizer_2.Add(label_17, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_wallet_max_allowed_amount = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_2.Add(self.txt_wallet_max_allowed_amount, 0, wx.EXPAND, 0)

        sizer_3 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY,
                                                 _("Daemon")), wx.VERTICAL)
        sizer_1.Add(sizer_3, 1, wx.ALL | wx.EXPAND, 12)

        grid_sizer_1 = wx.FlexGridSizer(9, 2, 4, 4)
        sizer_3.Add(grid_sizer_1, 1, wx.ALL | wx.EXPAND, 12)

        label_8 = wx.StaticText(self, wx.ID_ANY, _("Trusted:"))
        grid_sizer_1.Add(label_8, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_daemon_trusted = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_1.Add(self.txt_daemon_trusted, 0, wx.EXPAND, 0)

        label_9 = wx.StaticText(self, wx.ID_ANY, _("Address:"))
        grid_sizer_1.Add(label_9, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_daemon_address = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_1.Add(self.txt_daemon_address, 0, wx.EXPAND, 0)

        label_10 = wx.StaticText(self, wx.ID_ANY, _("Hardfork earliest height:"))
        grid_sizer_1.Add(label_10, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_daemon_hardfork_info = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_1.Add(self.txt_daemon_hardfork_info, 0, wx.EXPAND, 0)

        label_11 = wx.StaticText(self, wx.ID_ANY, _("Mining hash rate:"))
        grid_sizer_1.Add(label_11, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_daemon_mining_hash_rate = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_1.Add(self.txt_daemon_mining_hash_rate, 0, wx.EXPAND, 0)

        label_12 = wx.StaticText(self, wx.ID_ANY, _("Height:"))
        grid_sizer_1.Add(label_12, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_daemon_blockchain_height = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_1.Add(self.txt_daemon_blockchain_height, 0, wx.EXPAND, 0)

        label_13 = wx.StaticText(self, wx.ID_ANY, _("Target Height:"))
        grid_sizer_1.Add(label_13, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_daemon_blockchain_target_height = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_1.Add(self.txt_daemon_blockchain_target_height, 0,
                         wx.EXPAND, 0)

        label_13 = wx.StaticText(self, wx.ID_ANY, _("Network difficulty:"))
        grid_sizer_1.Add(label_13, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_daemon_network_difficulty = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_1.Add(self.txt_daemon_network_difficulty, 0, wx.EXPAND, 0)

        label_14 = wx.StaticText(self, wx.ID_ANY, _("Core RPC Version:"))
        grid_sizer_1.Add(label_14, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_core_rpc_version = wx.TextCtrl(
            self, wx.ID_ANY, style=wx.BORDER_NONE | wx.TE_READONLY
        )
        grid_sizer_1.Add(self.txt_core_rpc_version, 0, wx.EXPAND, 0)

        grid_sizer_1.AddGrowableCol(1)
        grid_sizer_2.AddGrowableCol(1)

        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_CLOSE)
        btn.SetDefault()
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        self.SetEscapeId(btn.GetId())
        btn.SetFocus()

        sizer_1.Add(btnsizer, 0, wx.EXPAND | wx.ALL, 8)

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.Layout()


if __name__ == "__main__":
    app = wx.App()
    PanelProperties(None).ShowModal()
