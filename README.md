# Missing Link – Backend (FastAPI) | Dev Setup & How‑To

Willkommen! Diese README erklärt **Architektur, lokale Entwicklung, Datenbank-Setup** und **Tests** für das Backend. Ziel: Mit **einem Befehl** starten und auf jedem Rechner reproduzierbar arbeiten.

---

## 🔭 Überblick

* **Framework:** FastAPI (Python)
* **ORM/DB:** SQLAlchemy + Alembic | PostgreSQL
* **Container:** Docker + docker compose
* **Ports:** API `8000` | Postgres (Host) `5433` → (Container-Port bleibt `5432`)
* **Datenbanken:**

  * **Dev-DB**: `missing_link` (für laufende App)
  * **Test-DB**: `app_testdb` (für Pytests)

---

## 🧱 Architektur & Projektstruktur

```
app/
├─ api/        # FastAPI-Routen (Endpunkte)
├─ core/       # Settings, Security, JWT, Config
├─ db/         # DB-Session, Engine
├─ models/     # SQLAlchemy-Modelle (DB-Tabellen)
├─ schemas/    # Pydantic-Schemas (Request/Response)
├─ services/   # Business-Logik
├─ tests/      # Pytests (API & Services)
└─ main.py     # FastAPI entry point

alembic/       # Migrations (Schema-Versionierung)
Dockerfile     # Build-Anleitung für API-Image
docker-compose.yml  # Startet API + Postgres
Makefile       # Komfort-Befehle (make up, reset, …)
.env.example   # Beispiel-ENV (ohne Secrets)
```

**Datenfluss:** Frontend → `api/` (Routen) → `services/` (Logik) → `models/` (DB) | Ein-/Ausgabeformate über `schemas/`. **Alembic** passt die echte DB-Struktur an die Models an.

---

## ✅ Voraussetzungen

* Docker Desktop / Docker Engine
* `docker compose` CLI
* `make` (Linux/Mac: vorhanden; Windows: WSL empfohlen)
* Python 3.12 (nur wenn du lokal Alembic/pytest außerhalb des Containers ausführen willst)

---

## ⚡ TL;DR (Schnellstart)

```bash
# 1) Repo klonen und ins Projekt gehen
git clone <repo-url>
cd missing-link-backend

# 2) .env aus Vorlage anlegen
cp .env.example .env

# 3) Alles hochfahren (DB + API + Migrationen)
make up
# → API: http://localhost:8000  (Docs: http://localhost:8000/docs)

# 4) Test-DB erstellen & migrieren
docker exec -it ml-postgres psql -U ml_user -d postgres -c "CREATE DATABASE app_testdb OWNER app;" || true
env DATABASE_URL="postgresql+asyncpg://app:app@localhost:5433/app_testdb" alembic upgrade head

# 5) Tests ausführen
env TEST_DATABASE_URL="postgresql+asyncpg://app:app@localhost:5433/app_testdb" pytest -q
```

---

## 🧩 Environment-Variablen

### `.env.example` (kopieren zu `.env`)

```ini
# Postgres (nur für den DB-Container)
POSTGRES_DB=missing_link
POSTGRES_USER=ml_user
POSTGRES_PASSWORD=ml_pass

# App-URL (lokal; Host-Port 5433, asyncpg für die App/Testtools)
DATABASE_URL=postgresql+asyncpg://app:app@localhost:5433/missing_link
```

> **Hinweis:** Für die laufende API injiziert `docker-compose.yml` explizit nur `DATABASE_URL`. Die `POSTGRES_*`-Variablen sind ausschließlich für den **DB-Container**.

Zusätzlich für **Tests** (nicht in `.env`, sondern beim Aufruf setzen):

```bash
TEST_DATABASE_URL="postgresql+asyncpg://app:app@localhost:5433/app_testdb"
```

---

## 🐳 Docker-Services

* **db (ml-postgres)**

  * Image: `postgres:16`
  * Ports: Host `5433` → Container `5432`
  * Healthcheck: `pg_isready`
  * Daten: lokales Volume `./.docker/pgdata` (nicht im Git)

* **api (ml-api)**

  * Build aus `Dockerfile`
  * Port: `8000`
  * Startkommando führt **Migrationen** (Alembic) und danach Uvicorn aus

---

## 🛠️ Makefile-Kommandos

```make
make up       # Startet DB + API (Migrationen laufen beim Start)
make down     # Stoppt & entfernt Container
make logs     # Verfolgt Container-Logs
make reset    # Hard-Reset: löscht Container + Volumes, frischer Start
make db-shell # psql-Shell im DB-Container
make api-shell# bash in den API-Container
make ps       # Compose-Status
```

> Unter Windows ggf. via WSL oder `mingw32-make` verwenden.

---

## 🚀 Detailliertes Setup (Schritt für Schritt)

1. **Konfig kopieren**

   ```bash
   cp .env.example .env
   ```

2. **Container hochfahren**

   ```bash
   make up
   ```

   * Postgres ist erreichbar auf **`localhost:5433`**
   * API läuft auf **`http://localhost:8000`** (Docs: `/docs`)

3. **User `app` existiert mit Passwort `app`** (wird im Setup erwartet). Falls nötig, anlegen:

   ```bash
   docker exec -it ml-postgres psql -U ml_user -d postgres -v ON_ERROR_STOP=1 -c "
   DO $$
   BEGIN
     IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'app') THEN
       CREATE ROLE app WITH LOGIN PASSWORD 'app';
     ELSE
       ALTER ROLE app WITH LOGIN PASSWORD 'app';
     END IF;
   END
   $$;"
   ```

4. **Test-DB anlegen & Schema migrieren**

   ```bash
   docker exec -it ml-postgres psql -U ml_user -d postgres -c "CREATE DATABASE app_testdb OWNER app;" || true
   env DATABASE_URL="postgresql+asyncpg://app:app@localhost:5433/app_testdb" alembic upgrade head
   ```

5. **Tests ausführen**

   ```bash
   env TEST_DATABASE_URL="postgresql+asyncpg://app:app@localhost:5433/app_testdb" pytest -q
   ```

---

## 🧪 Test-Strategie (warum separate DB?)

* Die Tests laufen gegen **`app_testdb`**, getrennt von der Dev-DB `missing_link` → saubere, reproduzierbare Läufe.
* `app/tests/conftest.py` liest **`TEST_DATABASE_URL`**. Ohne diese Variable würde ein Default (falsche URL) greifen.

---

## 🔍 Troubleshooting

**Problem:** `failed to bind host port 5432: address already in use`
**Ursache:** Host-Port 5432 belegt.
**Fix:** In `docker-compose.yml` mappen wir auf **5433:5432** (bereits so konfiguriert). Verbinde dich lokal immer mit Port **5433**.

**Problem:** Browser kann `http://localhost:8000` nicht erreichen
**Check:**

* `docker compose ps` → zeigt `0.0.0.0:8000->8000` bei `ml-api`?
* `docker compose logs -f ml-api` → startet Uvicorn oder crasht Alembic?
* Testweise im Container starten: `docker exec -it ml-api bash` → `uvicorn app.main:app --host 0.0.0.0 --port 8000`

**Problem:** `InvalidPasswordError: user "app"` bei Tests
**Ursache:** User/Passwort oder Port falsch.
**Fix:**

* User anlegen (siehe Setup Schritt 3)
* **Port 5433** benutzen
* `TEST_DATABASE_URL` korrekt setzen

**Problem:** `ProgrammingError: relation "..." does not exist`
**Ursache:** Migrationen nicht auf Test-DB angewendet.
**Fix:** `env DATABASE_URL=...app_testdb alembic upgrade head`

**Problem:** `ModuleNotFoundError: No module named 'psycopg'` (bei lokalen Alembic-Läufen)
**Fix:**

```bash
pip install "psycopg[binary]" asyncpg
```

**Problem:** `Extra inputs are not permitted … postgres_user` (Pydantic Settings)
**Ursache:** API-Container bekam ungenutzte `POSTGRES_*` Variablen.
**Fix:** In `docker-compose.yml` **nur** `DATABASE_URL` an `api` übergeben (kein `env_file` mit allen Variablen).

---

## 🧹 Reset / sauberer Neustart

```bash
make down
docker compose down -v      # löscht Container + Volumes
rm -rf ./.docker/pgdata || true
make up
```

> Achtung: Damit sind lokale DB-Daten weg (nur Dev/Test).

---

## ❓FAQ

**Warum getrennte URLs für App und Tests?**
Tests sollen die Laufzeitdaten nicht beeinflussen. Separate DB hält Runs deterministisch.

**Muss ich Seeds benutzen?**
Aktuell nein. Du kannst später ein `scripts/seed.py` ergänzen und im `api`-Startkommando aufrufen.

**Kann ich statt 5433 → 5432 nutzen?**
Ja, wenn auf deinem Host nichts auf 5432 läuft. Dann Mapping in `docker-compose.yml` auf `"5432:5432"` ändern **und** alle URLs anpassen.

---

## 📎 Nützliche Befehle

```bash
# API-Logs live ansehen
make logs

# In die DB reinschauen (Host)
PGPASSWORD=app psql -h localhost -p 5433 -U app -d missing_link -c 'select 1;'

# Alembic Migrations (gegen Dev-DB)
alembic current && alembic upgrade head

# Alembic gegen Test-DB laufen lassen
env DATABASE_URL="postgresql+asyncpg://app:app@localhost:5433/app_testdb" alembic upgrade head
```

---

Happy hacking! ✨ Wenn etwas unklar ist, bitte hier ergänzen – diese README ist dafür da, dass **jede:r** in Minuten loslegen kann.
