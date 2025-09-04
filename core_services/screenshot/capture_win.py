"""Windows screenshot capture using mss; returns PNG bytes (in-memory).
"""
import io
from PIL import Image
import mss


def capture_screen_to_bytes():
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        img = sct.grab(monitor)
        # mss returns raw BGRA; convert to RGB via PIL
        im = Image.frombytes('RGBA', (img.width, img.height), img.rgb)
        buf = io.BytesIO()
        im.save(buf, format='PNG')
        return buf.getvalue()
