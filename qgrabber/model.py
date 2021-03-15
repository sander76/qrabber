import asyncio
import logging
from typing import Optional

from PIL.Image import Image
from pyzbar.pyzbar import decode
from VideoCapture import Device

_LOGGER = logging.getLogger(__name__)


class ScannerModel:
    """Scanner model managing the webcam.

    Use the start function to start scanning with callbacks carrying results.
    Use the async scan function to start scanning a wait for a scanned result.
    """

    def __init__(self):
        self._graph = None
        self._camera_callback = None
        self._camera = None
        self._stop_scan = False

    async def scan(self, camera_callback, crop_x=None, crop_y=None) -> Optional[str]:
        self._camera_callback = camera_callback

        self._camera = Device(devnum=0, showVideoWindow=0)

        self._stop_scan = False
        code = None
        try:
            while not self._stop_scan:
                buffer = self._camera.getImage()
                buffer = crop(buffer, crop_x, crop_y)
                self._camera_callback(buffer)
                code = decode(buffer)
                if code:
                    break
                await asyncio.sleep(0.1)
        finally:
            del self._camera

        return code

    def stop(self):
        """Stop the webcam."""
        self._stop_scan = True
        # if self._camera:
        #     del self._camera


def crop(data: Image, crop_x, crop_y):
    x, y = data.size
    return data.crop(
        ((x - crop_x) // 2, (y - crop_y) // 2, (x + crop_x) // 2, (y + crop_y) // 2)
    )
