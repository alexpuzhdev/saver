FROM python:3.12.10-slim

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

RUN pip install --no-cache-dir poetry==1.8.4

COPY pyproject.toml README.md ./
COPY src ./src

RUN poetry install --no-root

CMD ["uvicorn", "saver.presentation.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
