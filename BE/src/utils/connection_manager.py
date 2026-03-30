from collections.abc import Iterable
from typing import Optional

from fastapi import WebSocket


class ConnectionManager:
    """Track active WebSocket connections and provide shared send helpers."""

    def __init__(self) -> None:
        """Initialize an in-memory container for active sockets."""
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket) -> None:
        """Accept and register a newly connected client."""
        await websocket.accept()
        self.active_connections.add(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        """Remove a disconnected client from the active registry."""
        self.active_connections.discard(websocket)

    async def send_json(self, websocket: WebSocket, payload: dict) -> None:
        """Send a JSON payload to a single connected client."""
        await websocket.send_json(payload)

    async def broadcast_json(self, payload: dict, targets: Optional[Iterable[WebSocket]] = None) -> None:
        """Broadcast a JSON payload to all active clients or an optional target subset."""
        target_sockets = targets if targets is not None else self.active_connections
        for socket in target_sockets:
            await socket.send_json(payload)

