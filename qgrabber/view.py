import logging

import wx
from PIL import Image

_LOGGER = logging.getLogger(__name__)


class ScannerView(wx.Panel):
    """Panel on which the webcam data is painted."""

    def __init__(
        self,
        parent,
        controller,
        mirror_x=True,
        mirror_y=True,
        width=800,
        height=600,
        style=wx.NO_BORDER,
    ):
        """

        Args:
            parent: wx parent.
            mirror_x: Flip image on its x axis.
            mirror_y: Flip image on its y axis.
            width: width of this panel.
            height: height of this panel.
            style: a style.
        """

        wx.Panel.__init__(self, parent, size=(width, height), style=style)

        self.width = width
        self.height = height

        # self.buffer = wx.NullBitmap

        self._mirror_x = mirror_x
        self._mirror_y = mirror_y

        self._controller = controller
        self._controller.subscribe_to_frame_data(self.set_frame)

    def set_frame(self, image):
        """Populate the image with raw data.

        Args:
            image: A Pillow image.

        """
        # _LOGGER.debug("Incomgin frame date")
        if self._mirror_y:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        frame = image.tobytes()

        buffer = wx.Bitmap.FromBuffer(self.width, self.height, frame)
        dc = wx.BufferedDC(wx.ClientDC(self), wx.NullBitmap, wx.BUFFER_VIRTUAL_AREA)
        dc.Clear()
        dc.DrawBitmap(buffer, 0, 0)
