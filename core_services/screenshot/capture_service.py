"""Privacy-first screenshot capture service (stub).
This service captures screenshots in memory, processes them with a stub classifier,
and does not persist raw images.
"""
import threading
import time
from typing import Callable, Optional
import platform

_HAS_WIN_CAPTURE = False
if platform.system() == 'Windows':
    try:
        from .capture_win import capture_screen_to_bytes
        _HAS_WIN_CAPTURE = True
    except Exception:
        _HAS_WIN_CAPTURE = False

from .ocr_stub import extract_text_from_image
from .clip_stub import classify_image_bytes

class ScreenshotCaptureService:
    def __init__(self, interval: float = 10.0, callback: Optional[Callable]=None):
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None
        self.callback = callback

    def _capture_loop(self):
        while not self._stop_event.is_set():
            # Capture real screen on Windows if available; otherwise use stub
            if _HAS_WIN_CAPTURE:
                try:
                    image_bytes = capture_screen_to_bytes()
                except Exception:
                    image_bytes = b"\x89PNG..."
            else:
                image_bytes = b"\x89PNG..."

            # Process with classifier (in-memory)
            # run OCR and CLIP stub
            text = extract_text_from_image(image_bytes)
            cl = classify_image_bytes(image_bytes)
            result = {"activity_type": cl.get('activity_type'), "confidence": cl.get('confidence'), "text": text}
            if self.callback:
                try:
                    self.callback(result)
                except Exception:
                    pass
            time.sleep(self.interval)

    def _classify(self, image_bytes: bytes):
        # Stub classifier: analyze bytes and return fake classification
        return {"activity_type": "unknown", "confidence": 0.0}

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)

# Simple usage for manual testing
if __name__ == '__main__':
    def cb(res):
        print('captured', res)
    s = ScreenshotCaptureService(interval=2.0, callback=cb)
    s.start()
    try:
        time.sleep(6)
    finally:
        s.stop()
