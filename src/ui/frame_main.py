import wx
from wx.adv import TaskBarIcon as TaskBarIcon
from lib.utils import resource_path

_ = wx.GetTranslation


def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.Append(item)
    return item


class FrameTaskBarIcon(TaskBarIcon):
    def __init__(self, frame, icon):
        self.frame = frame
        super().__init__(wx.adv.TBI_DOCK)
        app_name = wx.GetApp().GetAppName()
        self.SetIcon(icon, app_name)

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_taskbar_activate)

    def CreatePopupMenu(self):
        app_name = wx.GetApp().GetAppName()
        menu = wx.Menu()
        if self.frame.IsShown():
            msg = _("Minimize to tray")
        else:
            msg = "%s %s" % (_('Open'), app_name)
        create_menu_item(menu, msg, self.on_taskbar_activate)
        create_menu_item(menu, "%s %s" % (_("Close"), app_name),
                         self.on_taskbar_exit)
        return menu

    def on_taskbar_activate(self, evt):
        print('on_taskbar_activate', self.frame.IsIconized())
        if not self.frame.IsShown():
            self.frame.Iconize(False)
            self.frame.Show()
        else:
            self.frame.Iconize(True)
        evt.Skip()

    def on_taskbar_exit(self, evt):
        print('on_taskbar_exit')
        self.frame.Close()


class Frame(wx.Frame):
    ID_MENU_WALLET_SEED = wx.NewId()
    ID_MENU_WALLET_PROPERTIES = wx.ID_PROPERTIES
    ID_MENU_WALLET_PREFERENCES = wx.ID_PREFERENCES
    ID_MENU_WALLET_EXIT = wx.ID_EXIT
    ID_MENU_HELP_ABOUT = wx.ID_ABOUT

    def __init__(self, controller, *args, **kwargs):
        from .panel_action import ActionPanel
        from .panel_balance import BalancePanel
        from .panel_info import InfoPanel
        from .panel_txs import TxsPanel

        self.controller = controller
        super().__init__(*args, **kwargs)
        self.SetMinSize((640, 480))
        self.SetSize((640, 480))
        ico_bundle = wx.IconBundle()
        self.ico_bundle = ico_bundle
        ico_bundle.AddIcon(resource_path('images/equilibrity256x256.ico'))
        ico_bundle.AddIcon(resource_path('images/equilibrity128x128.ico'))
        ico_bundle.AddIcon(resource_path('images/equilibrity64x64.ico'))
        ico_bundle.AddIcon(resource_path('images/equilibrity32x32.ico'))
        ico_bundle.AddIcon(resource_path('images/equilibrity16x16.ico'))
        self.SetIcons(ico_bundle)

        self.mnu = menuBar = wx.MenuBar()

        menu1 = wx.Menu()
        self.mni_wallet_seed = menu1.Append(
            Frame.ID_MENU_WALLET_SEED, _("View &Seed/Keys")
        )
        self.mni_wallet_properties = menu1.Append(
            Frame.ID_MENU_WALLET_PROPERTIES, _("View P&roperties")
        )
        # menu1.AppendSeparator()
        # self.mni_wallet_preferences = menu1.Append(
        #     Frame.ID_MENU_WALLET_PREFERENCES, _("&Preferences")
        # )
        menu1.AppendSeparator()
        menu1.Append(self.ID_MENU_WALLET_EXIT, _("E&xit"), _("Exit"))
        menuBar.Append(menu1, "&Wallet")

        menu2 = wx.Menu()
        menu2.Append(Frame.ID_MENU_HELP_ABOUT,
                     _("&About"), _("This the text in the Statusbar"))
        menuBar.Append(menu2, _("&Help"))

        self.SetMenuBar(menuBar)

        sizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)
        self.pan_balance = pan_balance = BalancePanel(panel)
        self.pan_action = pan_action = ActionPanel(panel)
        self.pan_info = pan_info = InfoPanel(panel)
        self.pan_txs = pan_txs = TxsPanel(panel)

        sizer.Add(pan_balance, 0, wx.ALL | wx.EXPAND, 4)
        sizer.Add(pan_action, 0, wx.ALL | wx.EXPAND, 4)
        sizer.Add(pan_txs, 1, wx.ALL | wx.EXPAND, 4)
        sizer.Add(pan_info, 0, wx.ALL | wx.EXPAND, 4)

        panel.SetSizerAndFit(sizer)
        # sizer.Fit(panel)
        # self.Layout()

        self.Bind(wx.EVT_ICONIZE, self.on_minimize)

    def on_minimize(self, evt):
        print('on_minimize', self.IsIconized())
        if self.IsIconized() and TaskBarIcon.IsAvailable():
            if not 'wxMac' in wx.PlatformInfo:
                self.Hide()
