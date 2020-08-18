import logging
from typing import TYPE_CHECKING, Optional


if TYPE_CHECKING:
    from pyzbar.pyzbar import Decoded
    from qrabber.model import ScannerModel
    from qrabber.view import ScannerView

_LOGGER = logging.getLogger(__name__)


class Controller:
    def __init__(self, model: "ScannerModel", view: "ScannerView"):
        self._model = model
        self.view = view

    def start_scan(self):
        self._model.start(
            self.view.set_frame,
            on_code_scanned=self.stop_scan,
            crop_x=self.view.width,
            crop_y=self.view.height,
        )

    def stop_scan(self, result: Optional["Decoded"] = None):
        if result:
            print(result)

