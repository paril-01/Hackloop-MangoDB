from fastapi import APIRouter
from core_services.screenshot.capture_service import ScreenshotCaptureService

router = APIRouter(prefix="/api/screenshot", tags=["screenshot"])

# For the scaffold, provide an endpoint to start/stop the capture loop (demo only)
SERVICE = ScreenshotCaptureService(interval=5.0)

@router.post('/start')
def start_capture():
    SERVICE.start()
    return {"status": "started"}

@router.post('/stop')
def stop_capture():
    SERVICE.stop()
    return {"status": "stopped"}

@router.get('/status')
def status():
    alive = SERVICE._thread is not None and SERVICE._thread.is_alive()
    return {"running": alive}
