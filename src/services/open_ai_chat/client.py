import logging
from pathlib import Path
from openai import OpenAIError, AsyncOpenAI
from settings import config

logging.basicConfig(
        filename="/Users/danialmalaiev/proj_ai_bot/logs/logs.log",
        encoding="utf-8", level=logging.INFO,
        filemode="a", format="%(asctime)s %(levelname)s %(message)s")

logger = logging.getLogger(__name__)


class OpenAIClient:

    def __init__(self):
        self._client = AsyncOpenAI(api_key=config.AI_API_KEY)

    async def ask(self,
                  user_message: str,
                  system_prompt: str | None = None):
        try:
            if system_prompt:
                prompt = Path(system_prompt).read_text(encoding="utf-8")
            else:
                prompt = "You are a helpful AI assistant."

            response = await self._client.chat.completions.create(
                model=config.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": user_message}
                ]
            )

            answer = response.choices[0].message.content
            logger.info("Successful response!")
            return answer
        except OpenAIError as error:
            logger.error(f"Error creating response: {error}")
            raise
