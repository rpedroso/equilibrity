import os
import logging
import wx
from wx.adv import TaskBarIcon as TaskBarIcon
from lib.wallet import Wallet
from ui.frame_main import Frame, FrameTaskBarIcon
from controller.balance import Balance
from controller.action import Action
from controller.txs import Txs
from controller.info import Info
from pydispatch import dispatcher

_ = wx.GetTranslation


class Controller:
    def __init__(self, app, options):
        self.app = app
        self.frame = Frame(self, None)
        self.options = options
        self.frame.Disable()
        self.__upd_title()

        self.should_store = False

        self._balance = Balance(self)
        Action(self)
        Txs(self)
        Info(self)

        self.frame.Bind(wx.EVT_CLOSE, self.on_frame_close)
        self.frame.Bind(wx.EVT_MENU, self.on_menu_wallet_seed,
                        id=Frame.ID_MENU_WALLET_SEED)
        self.frame.Bind(wx.EVT_MENU, self.on_menu_wallet_properties,
                        id=Frame.ID_MENU_WALLET_PROPERTIES)
        # self.frame.Bind(wx.EVT_MENU, self.on_menu_wallet_preferences,
        #                 id=Frame.ID_MENU_WALLET_PREFERENCES)
        self.frame.Bind(wx.EVT_MENU, self.on_menu_wallet_exit,
                        id=Frame.ID_MENU_WALLET_EXIT)
        self.frame.Bind(wx.EVT_MENU, self.on_menu_help_about,
                        id=Frame.ID_MENU_HELP_ABOUT)
        self.frame.Show()

        if app.splash:
            app.splash.Destroy()

        dispatcher.connect(self.on_wallet_open, 'EVT_WALLET_OPEN')
        dispatcher.connect(self.on_wallet_new_block, 'EVT_WALLET_NEW_BLOCK')
        dispatcher.connect(self.on_wallet_refreshed, 'EVT_WALLET_REFRESHED')
        dispatcher.connect(self.on_wallet_init, 'EVT_WALLET_INIT')
        wx.CallLater(200, self.open_wallet)

    def ask_password(self):
        dlg = wx.PasswordEntryDialog(self.frame,
                                     _('Password'), _('Wallet Password'))
        dlg.CentreOnParent()
        password = dlg.GetValue() if dlg.ShowModal() == wx.ID_OK else None
        dlg.Destroy()
        return password

    def on_wallet_open(self, status, reason):
        if status is True:
            self.app.save_config_file(self.options)
            self.frame.mni_wallet_properties.Enable(False)
            self.frame.Enable()
            if TaskBarIcon.IsAvailable():
                self.tbicon = FrameTaskBarIcon(
                    self.frame, self.frame.ico_bundle.GetIcon()
                )

            Wallet.init()
        else:
            def f(reason):
                wx.MessageBox(reason, _('Error'), parent=self.frame,
                              style=wx.ICON_ERROR)
                open_type = self.options.get('open_type')
                if open_type == 'recover':
                    raise SystemExit
                self.open_wallet()
            wx.CallAfter(f, reason)

    def on_wallet_init(self):
        logging.debug('Controller.on_wallet_init')
        self.frame.mni_wallet_properties.Enable(True)

    def on_wallet_new_block(self, height):
        self.should_store = True

    def on_wallet_refreshed(self):
        if self.should_store:
            self.should_store = False
            logging.debug('Storing wallet')
            Wallet.store()

    def on_frame_close(self, evt):
        logging.debug('Controller.on_frame_close')
        self.frame.Disable()
        # Disconnect everything
        dispatcher.connections = {}

        busy = wx.BusyInfo(wx.BusyInfoFlags()  # noqa
                           .Parent(self.frame)
                           .Text(_('Closing wallet'))  # noqa
                           )
        wx.Yield()

        Wallet.close()

        self.tbicon.RemoveIcon()
        self.tbicon.Destroy()
        evt.Skip()

    def on_menu_wallet_exit(self, evt):
        self.frame.Close()
        evt.Skip()

    def on_menu_help_about(self, evt):
        from ui.panel_about import AboutPanel
        AboutPanel(self.frame)
        evt.Skip()

    def __upd_title(self):
        if self.app.wallet_filename is not None:
            wname = os.path.basename(self.app.wallet_filename)
            self.frame.SetTitle('%s - %s' % (self.app.GetAppName(), wname))
        else:
            self.frame.SetTitle('%s' % self.app.GetAppName())

    def open_wallet(self):
        options = self.options
        open_type = options.get('open_type')
        if open_type is None:
            password = self.ask_password()
            if password is None:
                self.frame.Destroy()
                return
            self.__upd_title()
            Wallet.open(password)
        elif open_type == 'recover':
            Wallet.recover(options['password'], options['seed'],
                           options['restore_height'])
        else:
            raise ValueError('Unknown open type')

    def on_menu_wallet_seed(self, evt):
        from .view_seed import ViewSeed
        dlg = ViewSeed(self.frame)
        dlg.CentreOnParent()
        dlg.ShowModal()
        dlg.Destroy()

    def on_menu_wallet_preferences(self, evt):
        pass

    def on_menu_wallet_properties(self, evt):
        from .properties import Properties
        dlg = Properties(self.frame)
        dlg.CentreOnParent()
        dlg.ShowModal()
        dlg.Destroy()
