# GPT Bot for Telegram

Learning project built with Python + aiogram and OpenAI integration.

## Features
- /start: main menu.
- /random: random fact from OpenAI with an image.
- /gpt: free-form question to ChatGPT.
- /talk: dialogue with a chosen personality (persona prompts).
- /quiz: topic quiz with score tracking.
- /translator: translate text to a selected language.

## Quick Start
1) Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate
```

2) Install dependencies:
```
pip install -r requirements.txt
```

3) Create .env from the example:
```
cp .env.example .env
```
Fill in:
- `API_KEY` — OpenAI API key.
- `TELEGRAM_KEY` — Telegram bot token.

4) Run the bot:
```
PYTHONPATH=src python -m main.run
```

## Resources
The project uses files under `resources/`:
- `resources/images/` — command images.
- `resources/prompts/` — system prompts for OpenAI.
- `resources/welcome_text/` — welcome text.

## Logging
Logs are printed to the console via `logging.basicConfig` in `src/main/run.py`.

## Project Structure
```
src/
  handlers/    # command/state handlers
  services/    # OpenAI integration
  state/       # FSM states
  settings/    # config and env
  ui/          # keyboards
resources/
  images/
  prompts/
  welcome_text/
```

## Commands
- `/start` — main menu.
- `/random` — random fact.
- `/gpt` — free-form question to GPT.
- `/talk` — personality selection and dialogue.
- `/quiz` — topic quiz.
- `/translator` — translate text.
