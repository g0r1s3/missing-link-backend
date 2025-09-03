## Dev Quickstart
# 1) DB starten (Docker)
docker start ml-postgres

# 2) venv aktivieren
source .venv/bin/activate

# 3) API starten
uvicorn app.main:app --reload
# Docs: http://127.0.0.1:8000/docs

