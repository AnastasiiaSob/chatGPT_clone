import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.helpers import openai_chat
from src.utils.connection_manager import ConnectionManager

router = APIRouter()
manager = ConnectionManager()


@router.get("/health")
def health():
    """Return a basic liveness signal for container/orchestrator checks."""
    return {"ok": True}


def _extract_user_message(raw_payload: str) -> str:
    """Parse incoming WebSocket payload and return the user's message text."""
    try:
        data = json.loads(raw_payload)
        if isinstance(data, dict):
            return str(data.get("message", "")).strip()
    except json.JSONDecodeError:
        return raw_payload.strip()
    return ""


@router.websocket("/ws")
async def chat_websocket(websocket: WebSocket) -> None:
    """Handle chat requests over WebSocket and return one AI response per message."""
    await manager.connect(websocket)
    await manager.send_json(websocket, {"type": "status", "message": "connected"})

    try:
        while True:
            raw_payload = await websocket.receive_text()
            user_message = _extract_user_message(raw_payload)

            if not user_message:
                await manager.send_json(
                    websocket,
                    {"type": "error", "message": "Message cannot be empty."},
                )
                continue
            
            if len(user_message) > 1000:
                await manager.send_json(
                    websocket,
                    {"type": "error", "message": "Message cannot be longer than 1000 characters."},
                )
                continue

            await manager.send_json(
                websocket,
                {"type": "user_message_received", "message": user_message},
            )
            try:
                ai_response = await openai_chat.generate_chat_response(user_message)
            except Exception:
                print("Failed to generate AI response for message: ", user_message)
                await manager.send_json(
                    websocket,
                    {"type": "error", "message": "Failed to generate AI response."},
                )
                continue

            await manager.send_json(
                websocket,
                {"type": "ai_response", "message": ai_response},
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)

