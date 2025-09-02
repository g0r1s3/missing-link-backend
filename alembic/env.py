# alembic/env.py
from logging.config import fileConfig
import asyncio
import os
import sys

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# 1) Alembic-Config & Logging
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2) Projektpfad hinzufügen (…/alembic -> …/)
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# 3) App-Imports (in richtiger Reihenfolge!)
from app.core.config import settings
from app.db.base import Base               # definiert Declarative Base
import app.models                          # lädt alle Modelle (Item, User, …)

# 4) Ziel-Metadaten (Autogenerate nutzt das)
target_metadata = Base.metadata

def run_migrations_offline():
    """Offline-Modus: reine SQL-Ausgabe."""
    url = settings.DATABASE_URL
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
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
