from openai import AsyncOpenAI
import logging
from settings import config

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=config.AI_API_KEY)

async def generate_text(system_text: str,user_text:str) -> str:

    try:

        response = await client.chat.completions.create(
            model = config.OPENAI_MODEL,
            messages = [
                {"role":"system", "content": system_text},
                {"role":"user", "content":user_text}
            ],
            temperature = config.OPENAI_MODEL_TEMPERATURE
        )
        return response.choices[0].message.content

    except Exception:
        logger.exception("OpenAI request failed!")
        return "OpenAI request failed. Please try again later."

