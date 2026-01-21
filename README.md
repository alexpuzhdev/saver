# Saver

Telegram bot + FastAPI service for downloading videos from supported platforms.

## Requirements
- Python 3.12.10
- Poetry

## Setup
```bash
poetry install
cp .env_example .env
```

Configure `config.toml` with your bot token and storage directories.

## Run API
```bash
poetry run uvicorn saver.presentation.api.main:app --reload
```

## Run bot
```bash
poetry run python -m saver.presentation.bot.main
```
