from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).parent.parent.parent
PATH_TO_ENV = BASE_DIR / ".env"

load_dotenv(PATH_TO_ENV)

AI_API_KEY = os.environ["API_KEY"]
TG_BOT_API_KEY = os.environ["TELEGRAM_KEY"]
OPENAI_MODEL_TEMPERATURE: float = 0.8
OPENAI_MODEL = "gpt-3.5-turbo"

LOGS_PATH = BASE_DIR / "logs"
PATH_TO_WELCOME_TEXT: Path = BASE_DIR / "resources" / "welcome_text"
PATH_TO_IMAGES: Path = BASE_DIR / "resources" / "images"
PATH_TO_MENUS: Path = BASE_DIR / "resources" / "menus"
PATH_TO_PROMPTS: Path = BASE_DIR / "resources" / "prompts"

print(TG_BOT_API_KEY)
