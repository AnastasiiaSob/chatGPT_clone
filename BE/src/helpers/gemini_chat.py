import logging
from google import genai

from src.settings import settings

logger = logging.getLogger(__name__)


def _build_prompt(user_message: str) -> str:
    """Build a concise prompt that includes role instruction and user text."""
    return (
        "You are a concise, helpful assistant.\n\n"
        f"User message:\n{user_message}"
    )


async def generate_chat_response(user_message: str) -> str:
    """Generate one complete assistant response text using the Gemini API."""
    if not settings.gemini_api_key:
        raise RuntimeError("GEMINI_API_KEY is not configured.")

    client = genai.Client(api_key=settings.gemini_api_key)
    prompt = _build_prompt(user_message)

    try:
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=prompt,
        )
        text = getattr(response, "text", None)
        return text.strip() if text else "I could not generate a response."
    except Exception:
        logger.exception("Failed to generate Gemini response.")
        return "I could not generate a response due to an internal error."
