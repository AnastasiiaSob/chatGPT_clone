from openai import AsyncOpenAI

from src.settings import settings


async def generate_chat_response(user_message: str) -> str:
    """Generate a single assistant response for a user message via OpenAI Chat Completions."""
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured.")

    client = AsyncOpenAI(api_key=settings.openai_api_key)

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a concise, helpful assistant.",
                },
                {
                    "role": "user",
                    "content": user_message,
                },
            ],
            temperature=0.4,
        )
        content = response.choices[0].message.content
        return content.strip() if content else "I could not generate a response."
    except Exception as e:
        print("Failed to generate AI response : {e}")
        return "I could not generate a response due to an internal error."

