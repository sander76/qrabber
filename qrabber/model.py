import logging
from typing import List

from pygrabber.dshow_graph import FilterGraph, FilterType
from pygrabber.dshow_ids import MediaTypes, MediaSubtypes
from pyzbar.pyzbar import Decoded
from pyzbar.pyzbar import decode
from qrabber.grabber import WxGrabber

_LOGGER = logging.getLogger(__name__)


def cropper(frame, width, height):
    if width is None:
        return frame
    y, x = frame.shape[:2]
    startx = x // 2 - width // 2
    starty = y // 2 - height // 2
    return frame[starty : starty + height, startx : startx + width].copy(order="C")


class ScannerModel:
    def __init__(self, stop_on_scan=False):
        self._graph = None
        self._crop_x = None
        self._crop_y = None
        self._camera_callback = None
        self._stop_on_scan = stop_on_scan
        self.on_code_scanned = []

    def start(self, camera_callback, on_code_scanned, crop_x=None, crop_y=None):
        """Start the scanner.

        Args:
            camera_callback: Called whenever image data from the camera is received.
            on_code_scanned: Called when a code is detected.
            crop_x: image data crop_x
            crop_y: image data crop_y

        Returns:

        """
        self._camera_callback = camera_callback
        self._crop_x = crop_x
        self._crop_y = crop_y
        self.on_code_scanned.append(on_code_scanned)

        self._graph = FilterGraph()
        self._graph.add_video_input_device(0)
        filter_type = FilterType.sample_grabber
        # assert not (filter_type in self._graph.filters)
        filter = self._graph.filter_factory.build_filter(filter_type, None)
        self._graph.filters[filter_type] = filter
        self._graph.filter_graph.AddFilter(filter.instance, filter.Name)

        sample_grabber = self._graph.filters[FilterType.sample_grabber]
        sample_grabber_cb = WxGrabber(self.call_back)

        sample_grabber.set_callback(sample_grabber_cb, 1)
        sample_grabber.set_media_type(MediaTypes.Video, MediaSubtypes.RGB24)

        self._graph.add_null_render()
        self._graph.prepare_preview_graph()
        self._graph.run()

    def stop(self, result: List["Decoded"]):
        """Stop the webcam."""
        for scanned_callback in self.on_code_scanned:
            scanned_callback(result)

    def decode(self, frame):
        codes = decode(frame)
        if codes:
            _LOGGER.debug(codes)
            self.stop(codes)
            if self._stop_on_scan:
                _LOGGER.debug("Stopping scanner.")
                self._graph.stop()

    def call_back(self, frame):
        frame = cropper(frame, self._crop_x, self._crop_y)
        self.decode(frame)
        self._camera_callback(frame)
