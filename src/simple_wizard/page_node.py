import wx
import wx.adv

_ = wx.GetTranslation


class PageNode(wx.adv.WizardPageSimple):
    LOCALS = {
        0: 'localhost:9231',
        1: 'localhost:9331',
        2: 'localhost:9431',
    }

    REMOTES = {
        0: ['154.38.165.93:9231',
            '38.242.135.157:9231',
            '213.155.160.222:9231',
            '194.233.64.43:9231',
            '207.244.249.105:9231',
            '161.97.102.172:9231',
            '62.171.181.142:9231',
            ],
        1: [],
        2: [],
    }

    def __init__(self, parent):
        # kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        super().__init__(parent)
        self.parent = parent

        bold = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                       wx.FONTWEIGHT_BOLD, 0, "")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        lbl_info = wx.StaticText(self, wx.ID_ANY, _(
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
            "do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
            "Ut enim ad minim veniam, quis nostrud exercitation ullamco "
            "laboris nisi ut aliquip ex ea commodo consequat. Duis aute "
            "irure dolor in reprehenderit in voluptate velit esse cillum "
            "dolore eu fugiat nulla pariatur. Excepteur sint occaecat "
            "cupidatat non proident, sunt in culpa qui officia deserunt "
            "mollit anim id est laborum."
        ))
        lbl_info.Wrap(500)
        sizer_1.Add(lbl_info, 0, wx.ALL | wx.EXPAND, 20)

        sizer_1.Add((1, 1), 0, wx.TOP | wx.BOTTOM, 5)

        label_0 = wx.StaticText(self, wx.ID_ANY, _("Network type"))
        label_0.SetFont(bold)
        self.ch_nettype = wx.Choice(self, wx.ID_ANY, choices=['Mainnet',
                                                              'Testnet',
                                                              'Stagenet'])
        self.ch_nettype.Select(0)
        sizer_1.Add(label_0, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        sizer_1.Add(self.ch_nettype, 0,
                    wx.BOTTOM | wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        label_2 = wx.StaticText(self, wx.ID_ANY, _("Node type:"))
        label_2.SetFont(bold)
        sizer_1.Add(label_2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        self.rd_node_local = wx.RadioButton(self, wx.ID_ANY, _("Local"))
        sizer_1.Add(self.rd_node_local, 0, wx.ALL, 20)

        self.rd_node_remote = wx.RadioButton(self, wx.ID_ANY, _("Remote"))
        sizer_1.Add(self.rd_node_remote, 0, wx.LEFT, 20)

        self.lst_node = wx.ListBox(self, wx.ID_ANY, choices=[_("choice 1")])
        sizer_1.Add(self.lst_node, 1, wx.ALL | wx.EXPAND, 20)

        self.SetSizer(sizer_1)
        # sizer_1.Fit(self)

        self.Layout()

        self.btn_next = self.FindWindowById(wx.ID_FORWARD)
        self.btn_cancel = self.FindWindowById(wx.ID_CANCEL)

        self.Bind(wx.EVT_CLOSE, self.on_wizard_close)
        self.Bind(wx.adv.EVT_WIZARD_PAGE_CHANGED, self.on_page_enter)
        self.Bind(wx.adv.EVT_WIZARD_CANCEL, self.on_wizard_cancel)
        self.Bind(wx.EVT_RADIOBUTTON, self.on_rd_nodetype)
        self.ch_nettype.Bind(wx.EVT_CHOICE, self.on_choice_nettype)
        self.lst_node.Bind(wx.EVT_LISTBOX, self.on_listbox_node)

        self._display_remotes(0)
        self.lst_node.Disable()
        # self.btn_cancel.Hide()

    def on_page_enter(self, evt):
        self.on_rd_nodetype(evt)

    def update_ui(self):
        self.btn_next.Disable()
        self.lst_node.Disable()

        if self.rd_node_local.Value:
            self.btn_next.Enable()
        elif self.lst_node.Selection > -1:
            self.btn_next.Enable()

        if self.rd_node_remote.Value:
            self.lst_node.Enable()

    def on_wizard_close(self, evt):
        wx.MessageBox(_("Cannot cancel at this stage."), _("Sorry"))
        evt.Veto()

    def on_wizard_cancel(self, evt):
        page = evt.GetPage()
        if page is self:
            self.on_wizard_close(evt)

    def on_rd_nodetype(self, evt):
        self.lst_node.Enable(evt.EventObject is self.rd_node_remote)
        # if evt.EventObject is self.rd_node_local:
        self.update_ui()
        evt.Skip()

    def on_choice_nettype(self, evt):
        self._display_remotes(evt.Selection)
        self.update_ui()
        evt.Skip()

    def on_listbox_node(self, evt):
        self.btn_next.Enable()

    def _display_remotes(self, nettype):
        self.lst_node.Set(PageNode.REMOTES.get(nettype))

    def get_nettype(self):
        return self.ch_nettype.Selection

    def get_daemon_addr(self):
        if self.rd_node_local.Value:
            return WizNodePanel.LOCALS.get(self.get_nettype())
        return self.lst_node.StringSelection

if __name__ == "__main__":
    from wx.adv import Wizard
    app = wx.App()

    w = Wizard(None)
    p = WizNodePanel(w)
    w.GetPageAreaSizer().Add(p)
    w.RunWizard(p)
