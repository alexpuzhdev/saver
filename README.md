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
Set `database.dsn` in `config.toml` (or `SAVER_DATABASE__DSN` in `.env`) to point to Postgres.
The bot auto-creates the `download_records` table on startup.

## Run API
```bash
poetry run uvicorn saver.presentation.api.main:app --reload
```

Health endpoint: `GET /health`  
Recent downloads: `GET /downloads?limit=20`

## Run bot
```bash
poetry run python -m saver.presentation.bot.main
```

## Docker
```bash
docker compose up --build
```

## Roadmap (v1)
1. Initialize project scaffold (Poetry, config, environment templates).
2. Add FastAPI service with health endpoint and container entrypoint.
3. Add aiogram bot with link handling and video download pipeline (yt-dlp).
4. Integrate PostgreSQL for persistence (download history, user requests).
5. Add observability and admin endpoints (basic stats/metrics).
6. Harden download pipeline (timeouts, retries, size limits, cleanup).
