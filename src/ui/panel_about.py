import wx
import wx.adv
from wx.lib.wordwrap import wordwrap

_ = wx.GetTranslation
licenseText = """MIT License

Copyright (c) 2024 R.Pedroso

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class AboutPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        info = wx.adv.AboutDialogInfo()
        info.Name = wx.GetApp().GetAppName()
        info.Version = "0.99.3"
        info.Copyright = "(c) 2024 R.Pedroso"
        info.Description = wordwrap(
            "A lightweight wallet for Equilibria network",
            500, wx.ClientDC(self))
        info.WebSite = ("http://github.com/rmdpedroso", "website")
        info.Developers = ["R.Pedroso",]
        info.License = wordwrap(licenseText, 500, wx.ClientDC(self))

        wx.adv.AboutBox(info, self)


if __name__ == "__main__":
    app = wx.App()
    frame = wx.Frame(None)
    AboutPanel(frame)
    frame.Show()
    app.MainLoop()
