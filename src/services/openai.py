import openai import OpenAi
import logging
from settings import config.OPENAI_MODEL

client = new OpenAi(api_key=OPENAI_MODEL)

async def generate_text(user_text) -> dict:

    try:

        response = await openai.ChatCompletion.acreate(
            model = OPENAI_MODEL,
            messages = [
                {"role":"user", "content":user_text}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        logging.error(e)
