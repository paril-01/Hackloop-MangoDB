"""Privacy-first screenshot capture service (stub).
This service captures screenshots in memory, processes them with a stub classifier,
and does not persist raw images.
"""
import threading
import time
from typing import Callable, Optional

class ScreenshotCaptureService:
    def __init__(self, interval: float = 10.0, callback: Optional[Callable]=None):
        self.interval = interval
        self._stop_event = threading.Event()
        self._thread = None
        self.callback = callback

    def _capture_loop(self):
        while not self._stop_event.is_set():
            # Stub: instead of actual screenshot, produce a fake "image" buffer
            fake_image = b"\x89PNG..."
            # Process with classifier (in-memory)
            result = self._classify(fake_image)
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
