from pathlib import Path 
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]


ENV_PATH = BASE_DIR / ".env"
if not ENV_PATH.exists():
    raise FileNotFoundError(f".env file not found: {ENV_PATH}")

load_dotenv(ENV_PATH)

def required_env(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError as exc:
        raise RuntimeError(f"Required environment variable missing: {name}") from exc


TG_BOT_API_KEY = required_env("TELEGRAM_KEY")
AI_API_KEY = required_env("API_KEY")
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MODEL_TEMPERATURE: float = 0.8
LOGS_PATH = BASE_DIR / "logs"
RESOURCES_DIR = BASE_DIR / "resources"

if not RESOURCES_DIR.is_dir():
    raise NotADirectoryError(f"Resources directory missing: {RESOURCES_DIR}")

