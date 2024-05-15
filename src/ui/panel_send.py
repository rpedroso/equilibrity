import string
import wx

_ = wx.GetTranslation


class SendPanel(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds['style'] = (wx.DEFAULT_DIALOG_STYLE
                         | wx.RESIZE_BORDER
                         | wx.MAXIMIZE_BOX)
        super().__init__(*args, **kwds)
        self.SetTitle(_("Send"))

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        grid_sizer_1 = wx.FlexGridSizer(4, 2, 4, 4)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND | wx.ALL, 12)

        label_1 = wx.StaticText(self, wx.ID_ANY, _("To:"))
        grid_sizer_1.Add(label_1, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        self.txt_to = wx.TextCtrl(self, wx.ID_ANY, "")
        grid_sizer_1.Add(self.txt_to, 1, wx.EXPAND, 0)

        label_2 = wx.StaticText(self, wx.ID_ANY, _("Amount:"))
        grid_sizer_1.Add(label_2, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        self.txt_amount = wx.TextCtrl(self)
        self.btn_amount_max = wx.Button(self, label=_("max"))

        sizer_2.Add(self.txt_amount, 1, wx.EXPAND, 0)
        sizer_2.Add(self.btn_amount_max, 0, wx.EXPAND, 0)

        grid_sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)

        self.ch_priority = wx.Choice(
            self, choices=['Default', 'Low', 'Medium', 'High']
        )
        self.ch_priority.Selection = 0
        label_4 = wx.StaticText(self, wx.ID_ANY, _("Priority:"))
        grid_sizer_1.Add(label_4, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT, 0)
        grid_sizer_1.Add(self.ch_priority, 0, wx.EXPAND, 0)

        label_3 = wx.StaticText(self, wx.ID_ANY, _("Note:"))
        grid_sizer_1.Add(label_3, 0, wx.ALIGN_RIGHT, 0)

        self.txt_note = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        grid_sizer_1.Add(self.txt_note, 0, wx.EXPAND, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 0)

        self.btn_send = wx.Button(self, wx.ID_OK, "Send")
        self.btn_send.SetDefault()
        sizer_2.AddButton(self.btn_send)

        self.btn_cancel = wx.Button(self, wx.ID_CANCEL)
        sizer_2.AddButton(self.btn_cancel)

        sizer_2.Realize()

        sizer_1.Add((1, 1), 0, wx.TOP, 12)

        grid_sizer_1.AddGrowableRow(3)
        grid_sizer_1.AddGrowableCol(1)

        self.SetSizer(sizer_1)

        self.SetAffirmativeId(self.btn_send.GetId())
        self.SetEscapeId(self.btn_cancel.GetId())

        self.txt_amount.Bind(wx.EVT_CHAR, self.on_char)

    def on_char(self, event):
        keycode = event.GetKeyCode()
        obj = event.GetEventObject()
        val = obj.GetValue()
        # filter unicode characters
        if keycode == wx.WXK_NONE:
            pass
        # allow digits
        elif chr(keycode) in string.digits:
            event.Skip()
        # allow special, non-printable keycodes
        elif chr(keycode) not in string.printable:
            event.Skip()  # allow all other special keycode
        # # allow '-' for negative numbers
        # elif chr(keycode) == '-':
        #     if val[0] == '-':
        #         obj.SetValue(val[1:])
        #     else:
        #         obj.SetValue('-' + val)
        # allow '.' for float numbers
        elif chr(keycode) == '.' and '.' not in val:
            event.Skip()
        elif keycode == wx.WXK_TAB:
            event.Skip()


if __name__ == "__main__":
    class MyApp(wx.App):
        def OnInit(self):
            self.dialog = SendPanel(None, wx.ID_ANY, "", size=(400, 400))
            self.SetTopWindow(self.dialog)
            self.dialog.ShowModal()
            self.dialog.Destroy()
            return True

    app = MyApp(0)
    app.MainLoop()
