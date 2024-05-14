import sys
import os
import io
import qrcode
from qrcode.image.styledpil import StyledPilImage
import wx


# From https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size  # noqa
def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def make_qrcode(text_data):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(text_data)

    img = qr.make_image(image_factory=StyledPilImage,
                        embeded_image_path=resource_path("images/equilibria.png"))
    data = io.BytesIO()
    img.save(data, ext='png')
    data.seek(0)
    im = wx.Bitmap(wx.Image(data))

    return im


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', '')  # os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    app = wx.App()
    img = make_qrcode('some data')
    # img.save('z.png')
    print(img)
