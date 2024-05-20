import wx
from lib.utils import make_qrcode
from ui.panel_address import AddressPanel

_ = wx.GetTranslation


class QRCode(wx.GenericStaticBitmap):
    def __init__(self, *args, **kwargs):
        address = kwargs.pop('address')
        super().__init__(*args, **kwargs)
        bmp = make_qrcode(address)
        self.SetScaleMode(2)
        self.SetBitmap(bmp)


class RecvPanel(wx.Dialog):
    def __init__(self, *args, **kwds):
        address = kwds.pop('address')
        self.address = address
        kwds['title'] = _('Receive')
        style = wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX
        kwds['style'] = style
        super().__init__(*args, **kwds)

        self.pan_address = AddressPanel(self)

        bmp_qrcode = QRCode(self, address=address, size=(200, 200))
        self.bmp_qrcode = bmp_qrcode

        self.btn_close = wx.Button(self, wx.ID_CLOSE)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(bmp_qrcode, 0, wx.EXPAND | wx.LEFT | wx.ALIGN_TOP, 4)
        sizer_2.Add((1, 1), 1, wx.EXPAND | wx.LEFT | wx.ALIGN_TOP, 4)

        sizer_3 = wx.StdDialogButtonSizer()
        sizer_3.AddButton(self.btn_close)
        sizer_3.Realize()

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.pan_address, 1, wx.EXPAND | wx.RIGHT, 4)
        sizer_4.Add(sizer_2, 0, wx.EXPAND | wx.RIGHT, 4)


        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_4, 1, wx.EXPAND | wx.TOP, 0)
        sizer_1.Add(sizer_3, 0, wx.ALIGN_RIGHT | wx.BOTTOM, 12)

        self.SetSizer(sizer_1)

        self.SetEscapeId(self.btn_close.GetId())

        self.pan_address.btn_copy.Bind(wx.EVT_BUTTON, self.on_btn_copy_addr)
        self.pan_address.Bind(wx.EVT_MENU, self.on_btn_copy_addr,
                              id=AddressPanel.AP_COPY_ADDR_ID)
        self.pan_address.Bind(wx.EVT_MENU, self.on_btn_copy_label,
                              id=AddressPanel.AP_COPY_LABEL_ID)

    def on_btn_copy_addr(self, evt):
        data = wx.TextDataObject()
        text = self.address
        data.SetText(text)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
            # self.btn_bitmap.Disable()
            # self.lbl_copied.SetLabel(_('Copied'))
            # wx.CallLater(500, self.btn_bitmap.Enable)
        else:
            wx.MessageBox(_("Unable to open the clipboard"), _("Error"))

    def on_btn_copy_label(self, evt):
        row = self.pan_address.lst_address.GetSelectedRow()
        label = self.pan_address.lst_address.GetValue(row, 1)
        data = wx.TextDataObject()
        data.SetText(label)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
            # self.btn_bitmap.Disable()
            # self.lbl_copied.SetLabel(_('Copied'))
            # wx.CallLater(500, self.btn_bitmap.Enable)
        else:
            wx.MessageBox(_("Unable to open the clipboard"), _("Error"))

    def set_address(self, address):
        self.address = address
        bmp = make_qrcode(address)
        self.bmp_qrcode.SetBitmap(bmp)
        self.bmp_qrcode.SetSize((200, 200))


if __name__ == "__main__":
    def on_button(evt):
        address = (
            "XT2qTBGgPTbY1i3cMdNQTabb5Mm2XpN6KbMqgrseHzyDfhjHdK5PBS7B9Wvr"
            "WhgEQWHWxB38obBASZaAUvQuy3Dd2iRasdYCn")
        p = RecvPanel(None, address=address, size=(500, 480))
        p.ShowModal()
        p.Destroy()

    app = wx.App()
    f = wx.Frame(None)
    b = wx.Button(f, label="open")
    b.Bind(wx.EVT_BUTTON, on_button)
    f.Show()
    app.MainLoop()
