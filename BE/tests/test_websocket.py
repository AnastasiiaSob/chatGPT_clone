from fastapi.testclient import TestClient

from src.main import app
from src.routes.v1 import endpoints


def test_websocket_success_flow(monkeypatch):
    """Ensure a user message gets an AI response over WebSocket."""

    async def mock_generate_chat_response(user_message: str) -> str:
        return f"echo:{user_message}"

    monkeypatch.setattr(endpoints.openai_chat, "generate_chat_response", mock_generate_chat_response)

    client = TestClient(app)
    with client.websocket_connect("/api/v1/ws") as websocket:
        connected = websocket.receive_json()
        assert connected["type"] == "status"

        websocket.send_json({"message": "Hello"})
        ack = websocket.receive_json()
        assert ack == {"type": "user_message_received", "message": "Hello"}

        ai = websocket.receive_json()
        assert ai == {"type": "ai_response", "message": "echo:Hello"}


def test_websocket_empty_message_validation(monkeypatch):
    """Ensure empty messages return validation error and keep connection alive."""

    async def mock_generate_chat_response(user_message: str) -> str:
        return f"echo:{user_message}"

    monkeypatch.setattr(endpoints.openai_chat, "generate_chat_response", mock_generate_chat_response)

    client = TestClient(app)
    with client.websocket_connect("/api/v1/ws") as websocket:
        websocket.receive_json()  # initial status event

        websocket.send_json({"message": "   "})
        error = websocket.receive_json()
        assert error == {"type": "error", "message": "Message cannot be empty."}

        websocket.send_json({"message": "Still connected"})
        websocket.receive_json()  # ack
        ai = websocket.receive_json()
        assert ai["type"] == "ai_response"


def test_websocket_generation_failure(monkeypatch):
    """Ensure upstream generation failures are reported as WebSocket errors."""

    async def mock_generate_chat_response(_user_message: str) -> str:
        raise RuntimeError("upstream failed")

    monkeypatch.setattr(endpoints.openai_chat, "generate_chat_response", mock_generate_chat_response)

    client = TestClient(app)
    with client.websocket_connect("/api/v1/ws") as websocket:
        websocket.receive_json()  # initial status event
        websocket.send_json({"message": "Hi"})

        websocket.receive_json()  # ack
        error = websocket.receive_json()
        assert error == {"type": "error", "message": "Failed to generate AI response."}

