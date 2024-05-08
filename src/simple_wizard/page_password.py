import wx
import wx.adv
from password_strength import PasswordStats


_ = wx.GetTranslation


class PagePassword(wx.adv.WizardPageSimple):
    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        label_1 = wx.StaticText(self, wx.ID_ANY, _("Wallet password"))
        label_1.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
                    wx.FONTWEIGHT_BOLD, 0, "")
        )
        sizer_1.Add(label_1, 0, wx.ALL | wx.EXPAND, 20)

        static_line_1 = wx.StaticLine(self, wx.ID_ANY)
        sizer_1.Add(static_line_1, 0, wx.BOTTOM | wx.EXPAND, 10)

        label_2 = wx.StaticText(self, wx.ID_ANY,
                                _("Please enter a password below"))
        sizer_1.Add(label_2, 0, wx.ALL, 20)

        label_3 = wx.StaticText(self, wx.ID_ANY, _("Password"))
        sizer_1.Add(label_3, 0, wx.LEFT, 20)

        self.txt_password = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PASSWORD)
        sizer_1.Add(self.txt_password, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        st_password_strength = wx.StaticText(self, wx.ID_ANY, "")
        sizer_1.Add(st_password_strength, 0,
                    wx.BOTTOM | wx.LEFT | wx.RIGHT, 20)
        self.st_password_strength = st_password_strength

        label_4 = wx.StaticText(self, wx.ID_ANY, _("Verify password"))
        sizer_1.Add(label_4, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        self.txt_password2 = wx.TextCtrl(self, wx.ID_ANY, style=wx.TE_PASSWORD)
        sizer_1.Add(self.txt_password2, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)

        st_password_match = wx.StaticText(self, wx.ID_ANY)
        sizer_1.Add(st_password_match, 0, wx.BOTTOM | wx.LEFT | wx.RIGHT, 20)
        self.st_password_match = st_password_match

        self.SetSizer(sizer_1)

        self.btn_next = self.FindWindowById(wx.ID_FORWARD)
        self.txt_password.Bind(wx.EVT_TEXT, self.on_txt_password_text)
        self.txt_password2.Bind(wx.EVT_TEXT, self.on_txt_password2_text)

    def on_txt_password_text(self, evt):
        value = self.txt_password.GetValue()
        if value:
            stats = PasswordStats(value)
            strength = stats.strength()
            if strength < 0.33:
                self.st_password_strength.SetLabel('weak password')
            elif strength < 0.66:
                self.st_password_strength.SetLabel('medium password')
            else:
                self.st_password_strength.SetLabel('strong password')
        else:
            self.st_password_strength.SetLabel('')
        pw = self.__compare_passwords()
        self.__state_forward_button(pw)
        evt.Skip()

    def on_txt_password2_text(self, evt):
        pw = self.__compare_passwords()
        self.__state_forward_button(pw)

    def __state_forward_button(self, password):
        self.btn_next.Enable(True if password else False)

    def __compare_passwords(self):
        value = self.txt_password.GetValue()
        value2 = self.txt_password2.GetValue()
        if not value2 and not value:
            self.st_password_match.SetLabel('')
            return True

        if value == value2:
            self.st_password_match.SetLabel(_("passwords do match"))
            return True

        self.st_password_match.SetLabel(_("passwords do not match"))
        return False
