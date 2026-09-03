FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock* /app/

# Установка зависимостей проекта без dev-пакетов
RUN poetry install --no-root --only main

# Копирование исходного кода
COPY . /app/

# Сборка статики Django
RUN python manage.py collectstatic --noinput || true

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]