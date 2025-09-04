from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from .core.database import init_db
from .core.session_cleanup import session_cleanup
from .core.config import settings

# Routers
from .api.routes.activities import router as activities_router
from .api.routes.automation import router as automation_router
from .api.routes.voice import router as voice_router

app = FastAPI(title="REPLIKA Backend")

# Allow Electron dev server or other origins as needed — tighten in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Health(BaseModel):
    status: str = "ok"


@app.on_event("startup")
def on_startup():
    """Initialize database and other startup tasks."""
    init_db()
    # start session cleanup background task
    try:
        import asyncio
        loop = asyncio.get_event_loop()
        session_cleanup.interval = getattr(settings, 'SESSION_CLEANUP_INTERVAL_SECONDS', 60)
        session_cleanup.start(loop)
    except Exception:
        pass


@app.on_event("shutdown")
async def on_shutdown():
    try:
        await session_cleanup.stop()
    except Exception:
        pass


@app.get("/health", response_model=Health)
async def health():
    """Simple healthcheck"""
    return Health()


@app.get("/api/sample_activity")
async def sample_activity():
    """Sample endpoint returning a fake activity classification"""
    return {
        "activity": "coding",
        "confidence": 0.93,
        "timestamp": "2025-09-04T00:00:00Z",
    }


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    """Echo websocket useful for demoing real-time updates"""
    await ws.accept()
    try:
        while True:
            data = await ws.receive_text()
            await ws.send_text(f"echo: {data}")
    except Exception:
        await ws.close()


# Register API routers
app.include_router(activities_router)
app.include_router(automation_router)
app.include_router(voice_router)
from .api.routes.users import router as users_router
app.include_router(users_router)
from .api.routes.screenshot import router as screenshot_router
app.include_router(screenshot_router)
from .api.routes.auth import router as auth_router
app.include_router(auth_router)
from .models import session  # noqa: F401
# Ensure DB initialized in test/import environments where startup events may not run
init_db()
