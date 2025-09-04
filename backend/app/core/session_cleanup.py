import asyncio
from datetime import datetime, timezone
from typing import Optional
from .database import SessionLocal
from ..models.session import Session as SessionModel


class SessionCleanupTask:
    def __init__(self, interval_seconds: int = 60):
        self.interval = interval_seconds
        self._task: Optional[asyncio.Task] = None
        self._stop = asyncio.Event()

    async def _run(self):
        while not self._stop.is_set():
            try:
                db = SessionLocal()
                now = datetime.now(timezone.utc)
                expired = db.query(SessionModel).filter(SessionModel.expires_at != None).filter(SessionModel.expires_at < now).all()
                if expired:
                    for s in expired:
                        try:
                            db.delete(s)
                        except Exception:
                            pass
                    db.commit()
                db.close()
            except Exception:
                # swallow errors to keep task alive
                pass
            try:
                await asyncio.wait_for(self._stop.wait(), timeout=self.interval)
            except asyncio.TimeoutError:
                continue

    def start(self, loop: asyncio.AbstractEventLoop):
        if self._task is None or self._task.done():
            self._stop.clear()
            self._task = loop.create_task(self._run())

    async def stop(self):
        self._stop.set()
        if self._task:
            await self._task


session_cleanup = SessionCleanupTask()
