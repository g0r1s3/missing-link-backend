FROM python:3.12-slim

WORKDIR /app

# Systemabhängigkeiten für psycopg (falls nötig)
RUN apt-get update && apt-get install -y build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Projekt rein
COPY . .

ENV PYTHONUNBUFFERED=1

# Standard: Uvicorn (wird durch docker-compose command überschrieben – dort laufen erst Migrations & Seeds)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
