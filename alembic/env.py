# alembic/env.py
from logging.config import fileConfig
import asyncio
import os
import sys

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# --- Pfad so setzen, dass 'app' importierbar ist ---
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# --- App-Imports ---
from app.core.config import settings
from app.db.base import Base  # enthält alle Modelle (Item)

# Alembic Config-Objekt
config = context.config

# Logging-Konfig übernehmen
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Ziel-Metadaten (für Autogenerate)
target_metadata = Base.metadata

def run_migrations_offline():
    """Offline-Modus: reine SQL-Ausgabe."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Online-Modus: echte DB-Verbindung (async)."""
    connectable = async_engine_from_config(
        {"sqlalchemy.url": settings.DATABASE_URL},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
