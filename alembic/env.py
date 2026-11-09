import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# 1. Import your Declarative Base and Models so Alembic can track metadata
from database import Base
from models import ItemModel  # Import all your models here so Base metadata knows about them!

# This is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 2. Point target_metadata to your application's Base metadata
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def include_object(object, name, type_, reflected, compare_to):
    # Only let Alembic touch the 'items' table and ignore everything else
    if type_ == "table" and name not in ["items", "alembic_version"]:
        return False
    return True

def do_run_migrations(connection) -> None:
    context.configure(
        connection=connection, 
        target_metadata=target_metadata,
        include_object=include_object  # <-- Add this filter here!
    )

    with context.begin_transaction():
        context.run_migrations()
        
async def run_async_migrations() -> None:
    """Run migrations in 'online' mode using the async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}), # <-- Updated here!
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations online."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_online() # Or offline path
else:
    run_migrations_online()