from .tasks import router as tasks_router
from .agents import router as agents_router
from .events import router as events_router
from .admin import router as admin_router
from .websocket import router as websocket_router

__all__ = [
    "tasks_router",
    "agents_router",
    "events_router",
    "admin_router",
    "websocket_router",
]
