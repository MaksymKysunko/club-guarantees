# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UVICORN_WORKERS=2

# системні залежності (якщо треба шрифти/локалі — додаси пізніше)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# залежності
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# код
COPY app ./app
COPY data ./data  # порожня папка для sqlite (буде перекрита томом)
# якщо є інші каталоги (app/api, app/domain — вони вже в /app/app)

EXPOSE 8000
ENV DATABASE_URL=sqlite:///./data/club.db

# uvicorn сервер
CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
