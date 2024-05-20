import wx
from lib.utils import make_qrcode
from .panel_address import AddressPanel

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

        # self.txt_addr = wx.TextCtrl(self, value=address,
        #                             style=wx.TE_MULTILINE | wx.TE_READONLY,
        #                             size=(500, -1))

        copy_bmp = wx.ArtProvider.GetBitmapBundle(wx.ART_COPY,
                                                  wx.ART_TOOLBAR, (24, 24))
        lbl_copied = wx.StaticText(self, label="", size=(20, -1),
                                   style=wx.ALIGN_RIGHT)
        self.lbl_copied = lbl_copied

        self.btn_bitmap = wx.BitmapButton(
            self, wx.ID_ANY,
            copy_bmp)

        self.btn_bitmap.SetSize(self.btn_bitmap.GetBestSize())

        self.btn_close = wx.Button(self, wx.ID_CLOSE)

        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.btn_bitmap, 0, wx.LEFT, 8)
        sizer_2.Add(lbl_copied, 1, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 4)
        self.sizer_2 = sizer_2

        sizer_3 = wx.StdDialogButtonSizer()
        sizer_3.AddButton(self.btn_close)
        sizer_3.Realize()

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(bmp_qrcode, 0, wx.EXPAND | wx.TOP, 4)
        # sizer_1.Add(self.txt_addr, 1, wx.EXPAND | wx.ALL, 8)
        sizer_1.Add(sizer_2, 0,
                    wx.EXPAND | wx.RIGHT | wx.BOTTOM, 12)
        sizer_1.Add(self.pan_address, 1, wx.EXPAND | wx.TOP, 4)
        sizer_1.Add(sizer_3, 0, wx.ALIGN_RIGHT | wx.BOTTOM, 12)
        self.SetSizer(sizer_1)

        self.SetEscapeId(self.btn_close.GetId())

        self.btn_bitmap.Bind(wx.EVT_BUTTON, self.on_btn_copy)

    def on_btn_copy(self, evt):
        data = wx.TextDataObject()
        text = self.address
        data.SetText(text)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(data)
            wx.TheClipboard.Close()
            self.btn_bitmap.Disable()
            self.lbl_copied.SetLabel(_('Copied'))
            wx.CallLater(500, self.btn_bitmap.Enable)
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
